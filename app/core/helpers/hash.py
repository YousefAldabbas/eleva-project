from passlib.context import CryptContext


class Hash:
    """
    Helper class for hashing password and verifying password
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password) -> bool:
        """
        Verify password
        :param plain_password:
        :param hashed_password:
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        """
        Get palin password and return hashed password
        :param password:
        :return: hashed password
        """
        return self.pwd_context.hash(password)


hash_helper = Hash()
