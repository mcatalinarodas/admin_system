import hashlib
import re
import os

# Constante para la sal (debería estar en una configuración segura, no hardcodeada)
SALT = b'una_sal_super_secreta'
MIN_PASSWORD_LENGTH = 6

def hashear_contraseña(contraseña: str) -> str:
    """Hashea una contraseña usando SHA256 con una sal."""
    pwd_bytes = contraseña.encode('utf-8')
    salted_pwd = pwd_bytes + SALT
    return hashlib.sha256(salted_pwd).hexdigest()

def verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool:
    """Verifica si una contraseña coincide con su hash almacenado."""
    return hashear_contraseña(contraseña) == hash_almacenado

def validar_contraseña(contraseña: str) -> tuple[bool, str]:
    """Valida que la contraseña cumpla los requisitos."""
    if len(contraseña) < MIN_PASSWORD_LENGTH:
        return False, f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres."
    if not re.search(r'[A-Za-z]', contraseña):
        return False, "La contraseña debe contener al menos una letra."
    if not re.search(r'[0-9]', contraseña):
        return False, "La contraseña debe contener al menos un número."
    return True, "Contraseña válida."

def limpiar_consola():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')
