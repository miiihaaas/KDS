/**
 * Dinamičko učitavanje podataka za forme uređaja
 */
document.addEventListener('DOMContentLoaded', function() {
    // Selektori za podtipove uređaja
    const tipSelect = document.getElementById('tip');
    const podtipSelect = document.getElementById('podtip');
    
    // Selektori za hijerarhiju lokacija
    const klijentSelect = document.getElementById('klijent_id');
    const lokacijaSelect = document.getElementById('lokacija_id');
    const objekatSelect = document.getElementById('objekat_id');
    const prostorijaSelect = document.getElementById('prostorija_id');
    
    // Kod za upravljanje toggle funkcionalnosti za dodavanje prostorija je uklonjen jer je uređaj vezan samo za jednu prostoriju
    
    // Inicijalizacija podtipova uređaja
    if (tipSelect && podtipSelect) {
        // Inicijalno postavljamo podtipove prilikom učitavanja stranice
        updatePodtipovi(tipSelect.value);
        
        // Dodajemo event listener za promenu tipa uređaja
        tipSelect.addEventListener('change', function() {
            updatePodtipovi(this.value);
        });
    }
    
    // Inicijalizacija hijerarhije lokacija
    if (klijentSelect) {
        // Postavi početno stanje
        if (klijentSelect.value) {
            updateLokacije(klijentSelect.value);
        }
        
        // Dodaj event listenere
        klijentSelect.addEventListener('change', function() {
            if (this.value) {
                updateLokacije(this.value);
            } else {
                // Resetuj niže nivoe
                resetSelect(lokacijaSelect, 'Odaberite lokaciju', true);
                resetSelect(objekatSelect, 'Prvo odaberite lokaciju', true);
                resetSelect(prostorijaSelect, 'Prvo odaberite objekat', true);
            }
        });
        
        if (lokacijaSelect) {
            lokacijaSelect.addEventListener('change', function() {
                const lokacijaId = this.value;
                const tipLokacije = this.options[this.selectedIndex]?.dataset.tip;
                
                if (lokacijaId && tipLokacije) {
                    updateObjekti(lokacijaId, tipLokacije);
                } else {
                    // Resetuj niže nivoe
                    resetSelect(objekatSelect, 'Prvo odaberite lokaciju', true);
                    resetSelect(prostorijaSelect, 'Prvo odaberite objekat', true);
                }
            });
        }
        
        if (objekatSelect) {
            objekatSelect.addEventListener('change', function() {
                const objekatId = this.value;
                if (objekatId) {
                    updateProstorije(objekatId);
                } else {
                    resetSelect(prostorijaSelect, 'Prvo odaberite objekat', true);
                }
            });
        }
    }
    
    /**
     * Ažurira padajuću listu podtipova na osnovu izabranog tipa
     * @param {string} tip - Izabrani tip uređaja
     */
    /**
     * Resetuje select element na početno stanje
     * @param {HTMLSelectElement} select - Select element koji treba resetovati
     * @param {string} defaultText - Tekst za podrazumevanu opciju
     * @param {boolean} disable - Da li treba onemogućiti select
     */
    function resetSelect(select, defaultText, disable = false) {
        if (!select) return;
        
        select.innerHTML = `<option value="">${defaultText}</option>`;
        select.disabled = disable;
    }
    
    /**
     * Ažurira padajuću listu lokacija na osnovu izabranog klijenta
     * @param {string} klijentId - ID izabranog klijenta
     */
    function updateLokacije(klijentId) {
        if (!klijentId || !lokacijaSelect) return;
        
        // Prikaži loading stanje
        lokacijaSelect.disabled = true;
        lokacijaSelect.innerHTML = '<option value="">Učitavanje lokacija...</option>';
        
        // Resetuj niže nivoe
        if (objekatSelect) resetSelect(objekatSelect, 'Prvo odaberite lokaciju', true);
        if (prostorijaSelect) resetSelect(prostorijaSelect, 'Prvo odaberite objekat', true);
        
        // Poziv API-ja za dobavljanje lokacija (nova ruta koja automatski određuje tip klijenta)
        fetch(`/uredjaji/api/lokacije/${klijentId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Greška pri učitavanju lokacija');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Ažuriranje padajuće liste sa lokacijama
                if (data.length === 0) {
                    resetSelect(lokacijaSelect, 'Nema dostupnih lokacija', false);
                } else {
                    let options = '<option value="">Odaberite lokaciju</option>';
                    data.forEach(lokacija => {
                        options += `<option value="${lokacija.id}" data-tip="${lokacija.tip}">${lokacija.naziv}</option>`;
                    });
                    lokacijaSelect.innerHTML = options;
                    lokacijaSelect.disabled = false;
                }
            })
            .catch(error => {
                console.error('Greška:', error);
                resetSelect(lokacijaSelect, 'Greška pri učitavanju lokacija', false);
            });
    }
    
    /**
     * Ažurira padajuću listu objekata na osnovu izabrane lokacije
     * @param {string} lokacijaId - ID izabrane lokacije
     * @param {string} tipLokacije - Tip lokacije
     */
    function updateObjekti(lokacijaId, tipLokacije) {
        if (!lokacijaId || !objekatSelect) return;
        
        // Prikaži loading stanje
        objekatSelect.disabled = true;
        objekatSelect.innerHTML = '<option value="">Učitavanje objekata...</option>';
        
        // Resetuj niže nivoe
        if (prostorijaSelect) resetSelect(prostorijaSelect, 'Prvo odaberite objekat', true);
        
        // Poziv API-ja za dobavljanje objekata
        fetch(`/uredjaji/api/objekti/${lokacijaId}/${tipLokacije}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Greška pri učitavanju objekata');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Ažuriranje padajuće liste sa objektima
                if (data.length === 0) {
                    resetSelect(objekatSelect, 'Nema dostupnih objekata', false);
                } else {
                    let options = '<option value="">Odaberite objekat</option>';
                    data.forEach(obj => {
                        options += `<option value="${obj.id}">${obj.naziv}</option>`;
                    });
                    objekatSelect.innerHTML = options;
                    objekatSelect.disabled = false;
                }
            })
            .catch(error => {
                console.error('Greška:', error);
                resetSelect(objekatSelect, 'Greška pri učitavanju objekata', false);
            });
    }
    
    /**
     * Ažurira padajuću listu prostorija na osnovu izabranog objekta
     * @param {string} objekatId - ID izabranog objekta
     */
    function updateProstorije(objekatId) {
        if (!objekatId || !prostorijaSelect) return;
        
        // Prikaži loading stanje i obriši sve postojeće opcije
        prostorijaSelect.disabled = true;
        prostorijaSelect.innerHTML = '<option value="">Učitavanje prostorija...</option>';
        
        // Poziv API-ja za dobavljanje prostorija
        fetch(`/uredjaji/api/prostorije/${objekatId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Greška pri učitavanju prostorija');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Prvo potpuno očistimo listu
                prostorijaSelect.innerHTML = '';
                
                // Ažuriranje padajuće liste sa prostorijama
                if (data.length === 0) {
                    prostorijaSelect.innerHTML = '<option value="">Nema dostupnih prostorija</option>';
                } else {
                    // Dodajemo podrazumevanu opciju
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Odaberite prostoriju';
                    prostorijaSelect.appendChild(defaultOption);
                    
                    // Dodajemo opcije prostorija bez dupliranja
                    const addedIds = new Set(); // Pratimo već dodate ID-ove
                    
                    data.forEach(prostorija => {
                        // Proverimo da li smo već dodali ovu prostoriju
                        if (!addedIds.has(prostorija.id)) {
                            const option = document.createElement('option');
                            option.value = prostorija.id;
                            option.textContent = prostorija.naziv;
                            prostorijaSelect.appendChild(option);
                            
                            // Dodajemo ID u set obrađenih
                            addedIds.add(prostorija.id);
                        }
                    });
                }
                
                prostorijaSelect.disabled = false;
            })
            .catch(error => {
                console.error('Greška:', error);
                resetSelect(prostorijaSelect, 'Greška pri učitavanju prostorija', false);
            });
    }
    
    /**
     * Ažurira padajuću listu podtipova na osnovu izabranog tipa
     * @param {string} tip - Izabrani tip uređaja
     */
    function updatePodtipovi(tip) {
        if (!tip) {
            podtipSelect.innerHTML = '<option value="">Prvo izaberite tip uređaja</option>';
            podtipSelect.disabled = true;
            return;
        }
        
        // Prikaži loading stanje
        podtipSelect.disabled = true;
        podtipSelect.innerHTML = '<option value="">Učitavanje podtipova...</option>';
        
        // Poziv API-ja za dobavljanje podtipova
        fetch(`/uredjaji/api/podtipovi-uredjaja/${tip}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Greška pri učitavanju podtipova');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Ažuriranje padajuće liste sa podtipovima
                if (data.length === 0) {
                    podtipSelect.innerHTML = '<option value="">Nema dostupnih podtipova</option>';
                    podtipSelect.disabled = true;
                } else {
                    let options = '<option value="">Odaberite podtip</option>';
                    data.forEach(podtip => {
                        options += `<option value="${podtip.id}">${podtip.naziv}</option>`;
                    });
                    podtipSelect.innerHTML = options;
                    podtipSelect.disabled = false;
                }
            })
            .catch(error => {
                console.error('Greška:', error);
                podtipSelect.innerHTML = '<option value="">Greška pri učitavanju podtipova</option>';
                podtipSelect.disabled = true;
            });
    }
});
