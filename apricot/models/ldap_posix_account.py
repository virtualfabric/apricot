import re

from pydantic import BaseModel, StringConstraints, validator
from typing_extensions import Annotated

LINUX_ID_MIN = 2000
LINUX_ID_MAX = 60000


class LdapPosixAccount(BaseModel):
    cn: str
    gidNumber: int  # noqa: N815
    homeDirectory: Annotated[  # noqa: N815
        str, StringConstraints(strip_whitespace=True, to_lower=True)
    ]
    uid: str
    uidNumber: int  # noqa: N815

    @validator("gidNumber")
    @classmethod
    def validate_gid_number(cls, gid_number: int) -> int:
        """Avoid conflicts with existing users"""
        if not LINUX_ID_MIN <= gid_number <= LINUX_ID_MAX:
            msg = f"Must be in range {LINUX_ID_MIN} to {LINUX_ID_MAX}."
            raise ValueError(msg)
        return gid_number

    @validator("homeDirectory")
    @classmethod
    def validate_home_directory(cls, home_directory: str) -> str:
        return re.sub(r"\s+", "-", home_directory)

    @validator("uidNumber")
    @classmethod
    def validate_uid_number(cls, uid_number: int) -> int:
        """Avoid conflicts with existing users"""
        if not LINUX_ID_MIN <= uid_number <= LINUX_ID_MAX:
            msg = f"Must be in range {LINUX_ID_MIN} to {LINUX_ID_MAX}."
            raise ValueError(msg)
        return uid_number
