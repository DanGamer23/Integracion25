from passlib.hash import bcrypt

def generate_password_hash(password):
    """Genera el hash bcrypt de una contraseña dada."""
    return bcrypt.hash(password)

if __name__ == "__main__":
    passwords_to_hash = [
        "colocolo1",
        "123456",
        "Pikachu23",
        "Chile2015.",
        "56789012-3"
    ]

    print("--- Hashes de Contraseñas ---")
    for pwd in passwords_to_hash:
        hashed_pwd = generate_password_hash(pwd)
        print(f"Contraseña: '{pwd}' -> Hash: '{hashed_pwd}'")
    print("---------------------------")
    print("\nCopia y pega estos hashes directamente en tus scripts SQL.")