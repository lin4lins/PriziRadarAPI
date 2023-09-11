import secrets
import string


def generate_code_verifier(length=128) -> str:
    characters = string.ascii_letters + string.digits + '-._~'
    if length < 43 or length > 128:
        raise ValueError("Code verifier length must be between 43 and 128 characters")

    return ''.join(secrets.choice(characters) for _ in range(length))
