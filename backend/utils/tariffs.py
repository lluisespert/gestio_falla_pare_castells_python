"""
Utilidades para el cálculo de tarifas de pagaments
Migrado desde la función calcular_total() de PHP
"""
import re
import unicodedata


def remove_accents(text):
    """Eliminar acentos de un texto"""
    if not text:
        return ''
    # Normalizar y eliminar acentos
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize(text):
    """Normalizar texto: lowercase, sin acentos, espacios normalizados"""
    if not text:
        return ''
    text = text.lower().strip()
    text = remove_accents(text)
    text = re.sub(r'\s+', ' ', text)
    return text


def calcular_total(grup, edat):
    """
    Calcular el total a pagar según el grupo y la edad
    
    Args:
        grup (str): Grupo del faller
        edat (int): Edad del faller
    
    Returns:
        float: Total a pagar en euros
    """
    if not grup:
        grup = ''
    
    g = normalize(grup)
    grup_original_lower = grup.lower()
    grup_sin_acentos = remove_accents(grup_original_lower)
    
    # ========== PRIORIDAD 1: GRUPOS ESPECIALES (independiente de edad) ==========
    
    # Grup: Fallers/falleres de brussó - siempre 400€
    variaciones_brusso = [
        'brussó', 'brusso', 'brusson', 'brasso', 'bruso', 'brusó',
        'fallers de brussó', 'falleres de brussó', 'fallers de brusso',
        'falleres de brusso', 'fallers/falleres de brussó', 'fallers/falleres de brusso',
        'fallers falleres de brussó', 'fallers falleres de brusso'
    ]
    
    for variacion in variaciones_brusso:
        if (variacion in grup_original_lower or 
            remove_accents(variacion) in grup_sin_acentos or 
            remove_accents(variacion) in g):
            return 400.00
    
    # Detección de emergencia para brussó
    if re.search(r'bru[sç]*', grup, re.IGNORECASE) or re.search(r'bru[sç]*', g, re.IGNORECASE):
        return 400.00
    
    # Grup: Fallers d'honor - siempre 100€
    if "fallers d'honor" in g or 'fallers dhonor' in g:
        return 100.00
    
    # Grup: Familiar de faller/fallera - siempre 300€
    if 'familiar de faller/fallera' in g or 'familiar de faller fallera' in g:
        return 300.00
    
    # ========== PRIORIDAD 2: GRUPOS CON VARIACIÓN POR EDAD ==========
    
    # Grup: Cap dels pares es faller
    if 'cap dels pares es faller' in g or 'cap dels pares es' in g:
        if edat <= 3:
            return 70.00
        if edat <= 10:
            return 100.00
        if edat <= 13:
            return 150.00
    
    # Grup: Un dels pares es faller
    if 'un dels pares es faller' in g:
        if edat <= 3:
            return 40.00
        if edat <= 10:
            return 55.00
        if edat <= 13:
            return 85.00
    
    # Grup: Els dos pares son fallers
    if 'els dos pares son fallers' in g:
        if edat <= 3:
            return 0.00
        if edat <= 10:
            return 35.00
        if edat <= 13:
            return 55.00
    
    # Grup: Cap ascendent faller (14-17 anys)
    if 'cap ascendent faller' in g or 'cap ascendet faller' in g:
        if 14 <= edat <= 17:
            return 250.00
    
    # Grup: 1 ascendent faller (14-17 anys)
    if '1 ascendent faller' in g or '1 ascendet faller' in g:
        if 14 <= edat <= 17:
            return 200.00
    
    # Grup: 2 ascendents fallers (14-17 anys)
    if '2 ascendents fallers' in g or '2 ascendets fallers' in g:
        if 14 <= edat <= 17:
            return 185.00
    
    # ========== PRIORIDAD 3: TARIFA GENERAL POR EDAD (sin grup específico) ==========
    
    # 18-25 anys
    if 18 <= edat <= 25:
        return 425.00
    
    # 26+ anys
    if edat >= 26:
        return 575.00
    
    # Menores de 18 sin grup específico
    if edat < 18:
        return 200.00
    
    # Fallback final
    return 0.00
