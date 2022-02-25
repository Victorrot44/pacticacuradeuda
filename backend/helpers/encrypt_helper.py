from werkzeug.security import generate_password_hash, check_password_hash

def encrypt_password(password: str):
  hash = generate_password_hash(password)
  return hash

def valid_password(encrypted_password: str, password: str):
  return check_password_hash(encrypted_password, password)