# Nova funkcija u utils/helpers.py
def sanitize_search_term(term):
    """
    Sanitizuje string za pretragu uklanjajući potencijalno opasne karaktere
    koji bi mogli biti korišćeni za SQL injection.
    """
    if not term:
        return term
    
    # Ukloni specijalne karaktere i SQL wildcard znakove
    import re
    sanitized = re.sub(r'[;:()"\'\{\}\[\]\\%_=]|--', '', term)
    return sanitized
