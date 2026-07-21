import pytest

from app.reply_intelligence.parser.reply_parser import ReplyParser
from app.reply_intelligence.enums.reply_intent import ReplyIntent


VALID_JSON = """
{
    "intent":"INTERESTED",
    "sentiment":"POSITIVE",
    "confidence":0.96,
    "meeting_requested":false,
    "needs_followup":true,
    "reason":"Interested."
}
"""


def test_parse_valid_json():

    result = ReplyParser.parse(
        VALID_JSON,
    )

    assert result.intent == ReplyIntent.INTERESTED
    assert result.confidence == 0.96


def test_parse_markdown():

    text = "```json\n" + VALID_JSON + "\n```"

    result = ReplyParser.parse(text)

    assert result.intent == ReplyIntent.INTERESTED


def test_parse_with_extra_text():

    text = (
        "Here is my answer.\n\n"
        + VALID_JSON
        + "\n\nThank you."
    )

    result = ReplyParser.parse(text)

    assert result.intent == ReplyIntent.INTERESTED


def test_invalid_json():

    with pytest.raises(ValueError):

        ReplyParser.parse(
            "No JSON here",
        )