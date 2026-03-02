import hashlib
from configurations.config import settings

class McpConfigServices:

    @staticmethod
    def getHashedLocalFileSecretToken() -> str:
        token = settings.LOCAL_FILE_SECRET_TOKEN
        if not token:
            # Better to fail loudly with a clear message than a cryptic error
            raise ValueError("LOCAL_FILE_SECRET_TOKEN is not set in environment variables.")
        return hashlib.sha256(token.encode('utf-8')).hexdigest()