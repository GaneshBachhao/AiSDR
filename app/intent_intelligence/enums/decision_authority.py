from enum import Enum


class DecisionAuthority(str, Enum):
    UNKNOWN = "UNKNOWN"
    INFLUENCER = "INFLUENCER"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    VP = "VP"
    CXO = "CXO"
    OWNER = "OWNER"