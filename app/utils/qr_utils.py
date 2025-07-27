"""
Modul za generisanje QR kodova i PDF dokumenata za štampanje.
Koristi qrcode biblioteku za dinamičko generisanje QR kodova i fpdf2 za PDF generisanje.
"""
import os
import io
import tempfile
from datetime import datetime
from pathlib import Path

import qrcode
from PIL import Image
from fpdf import FPDF
from flask import current_app

def generisi_qr_kod_za_uredjaj(uredjaj_id):
    """
    Generiše QR kod za uređaj direktno u memoriji.
    
    Args:
        uredjaj_id: ID uređaja za koji se generiše QR kod
        
    Returns:
        BytesIO objekat sa QR kod slikom
    """
    # Kreiraj QR kod sa ID-jem uređaja
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(str(uredjaj_id))
    qr.make(fit=True)
    
    # Kreiraj sliku QR koda
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Sačuvaj sliku u memoriji
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def generisi_pdf_sa_qr_kodom(uredjaj, broj_kopija=1):
    """
    Generiše PDF dokument sa QR kodom i osnovnim podacima o uređaju.
    PDF je optimizovan za portabl štampače sa nalepnicama dimenzija 57mm x 32mm.
    Koristi DejaVu Sans Condensed font za podršku srpskih karaktera (čćžšđ).
    
    Args:
        uredjaj: Objekat Uredjaj za koji se generiše QR kod
        broj_kopija: Broj kopija QR koda na PDF-u
        
    Returns:
        BytesIO objekat koji sadrži PDF dokument
    """
    # Dimenzije nalepnice u mm (standardna nalepnica za portabl štampače)
    sirina_nalepnice = 57
    visina_nalepnice = 32
    
    try:
        # Kreiraj privremeni QR kod fajl
        temp_qr_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        qr_buffer = generisi_qr_kod_za_uredjaj(uredjaj.id)
        temp_qr_file.write(qr_buffer.getvalue())
        temp_qr_file.close()
        
        # Kreiraj PDF
        pdf = FPDF(orientation="P", unit="mm", format=(sirina_nalepnice, visina_nalepnice))
        pdf.set_margin(0)  # bez margine za maksimalno iskorišćenje prostora
        
        # Dodavanje Unicode fontova za podršku srpskih karaktera
        fonts_path = Path(current_app.root_path) / 'static' / 'fonts'
        pdf.add_font('DejaVu', '', str(fonts_path / 'DejaVuSansCondensed.ttf'), uni=True)
        pdf.add_font('DejaVu', 'B', str(fonts_path / 'DejaVuSansCondensed-Bold.ttf'), uni=True)
        
        # Dodaj kopije na PDF
        for _ in range(broj_kopija):
            pdf.add_page()
            
            # Postavi font za tekst - koristimo manji font zbog ograničenog prostora
            pdf.set_font("DejaVu", size=6)
            
            # Dodaj QR kod u centralni deo nalepnice (malo pomeren prema gore)
            # Prilagođena veličina i pozicija za bolju čitljivost
            qr_sirina = 18
            pdf.image(temp_qr_file.name, x=(sirina_nalepnice-qr_sirina)/2, y=2, w=qr_sirina, h=qr_sirina)
            
            # Dodaj naslov iznad QR koda
            pdf.set_xy(0, 0)
            pdf.set_font("DejaVu", 'B', size=7)
            pdf.cell(sirina_nalepnice, 5, "HVAC UREĐAJ", 0, new_x="LEFT", new_y="NEXT", align="C")
            
            # Dodaj osnovne informacije o uređaju ispod QR koda
            y_pozicija = qr_sirina + 4  # Početak teksta ispod QR koda
            
            # Koristi cell umesto text za bolje pozicioniranje i centriranje
            pdf.set_font("DejaVu", 'B', size=6)
            pdf.set_xy(0, y_pozicija)
            pdf.cell(sirina_nalepnice, 4, f"ID: {uredjaj.id}", 0, new_x="LEFT", new_y="NEXT", align="C")
            
            # Proizvođač i model
            pdf.set_font("DejaVu", size=6)
            model_text = f"{uredjaj.proizvodjac} {uredjaj.model}"
            # Skrati tekst ako je predugačak
            if len(model_text) > 25:
                model_text = model_text[:22] + "..."
            pdf.cell(sirina_nalepnice, 4, model_text, 0, new_x="LEFT", new_y="NEXT", align="C")
            
            # Serijski broj i datum
            pdf.set_font("DejaVu", size=6)
            serijski_text = f"S/N: {uredjaj.serijski_broj}"
            if len(serijski_text) > 25:
                serijski_text = serijski_text[:22] + "..."
            pdf.cell(sirina_nalepnice, 4, serijski_text, 0, new_x="LEFT", new_y="NEXT", align="C")
            
            # Datum generisanja
            pdf.set_font("DejaVu", '', size=5)
            pdf.cell(sirina_nalepnice, 3, datetime.now().strftime("%d.%m.%Y"), 0, new_x="LEFT", new_y="NEXT", align="C")
        
        # Sačuvaj PDF u BytesIO objekat (u memoriji) umesto u fajl na disku
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        return pdf_buffer
    
    finally:
        # Osiguraj da se privremeni fajlovi uvek obrišu, čak i u slučaju greške
        if 'temp_qr_file' in locals():
            try:
                os.unlink(temp_qr_file.name)
            except Exception:
                pass
