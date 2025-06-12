import secrets
import base64

def generate_secret_key():
    """Generate a random 32-byte key and encode it as base64."""
    return base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

def generate_jwt_secret():
    """Generate a random 32-byte key and encode it as base64."""
    return base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

if __name__ == "__main__":
    print("Generated Security Keys:")
    print("-" * 50)
    print(f"SECRET_KEY={generate_secret_key()}")
    print(f"JWT_SECRET={generate_jwt_secret()}")
    print("-" * 50)
    print("\nIMPORTANT: Keep these keys secure and never share them!") 