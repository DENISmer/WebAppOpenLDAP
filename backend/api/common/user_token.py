from dataclasses import dataclass


@dataclass
class UserToken:
    dn: str
    uid: str
    userPassword: bytes
    role: str