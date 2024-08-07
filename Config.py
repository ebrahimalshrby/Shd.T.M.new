import os


class Config(object):
    TOKEN = os.environ.get("TOKEN", "")

    OID = int(os.environ.get("ID", 21627756))
