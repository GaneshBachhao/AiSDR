from enum import Enum


class RecommendationType(str, Enum):
    SERVICE = "SERVICE"
    PRODUCT = "PRODUCT"
    WORKSHOP = "WORKSHOP"
    ASSESSMENT = "ASSESSMENT"
    FOLLOW_UP = "FOLLOW_UP"