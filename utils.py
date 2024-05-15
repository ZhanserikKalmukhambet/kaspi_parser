import os

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise 'Set the %s environment variable' % name
