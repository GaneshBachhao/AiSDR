from enum import Enum


class Sentiment(str, Enum):

    POSITIVE = "POSITIVE"

    NEUTRAL = "NEUTRAL"

    NEGATIVE = "NEGATIVE"