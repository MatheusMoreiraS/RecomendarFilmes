def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    if not any(c.isalpha() for c in senha):
        return False, "A senha deve conter pelo menos uma letra"
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"
