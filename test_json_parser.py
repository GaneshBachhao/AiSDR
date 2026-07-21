from app.common.utils.json_parser import JsonParser


def test_parse_json():

    response = """
    ```json
    {
        "company":"OpenAI",
        "industry":"AI"
    }
    ```
    """

    result = JsonParser.parse(response)

    assert result["company"] == "OpenAI"
    assert result["industry"] == "AI"