import bcrypt


class Hash:
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(str.encode(password), salt)
        return hashed_password.decode()

    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(str.encode(plain_password), str.encode(hashed_password))
