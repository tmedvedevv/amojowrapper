import os


def get_env(key: str, default=None) -> str:
    return os.getenv(key, default)
