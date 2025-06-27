import bcrypt
print(bcrypt.hashpw("Reducto2025*".encode(), bcrypt.gensalt()).decode())
