import re


# Validação de senha
def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    if not any(c.isalpha() for c in senha):
        return False, "A senha deve conter pelo menos uma letra"
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"


# Validação básica de email
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
