from app.integrations.tavily.tavily_client import (
    AgneticTavilyClient,
)


def test_tavily_search():

    client = AgneticTavilyClient()

    results = client.search(
        query="Manufacturing companies in Pune",
        max_results=5,
    )

    assert isinstance(results, list)

    assert len(results) > 0

    print("\n")

    print("=" * 60)

    print(f"Results Found : {len(results)}")

    print("=" * 60)

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")

        print("-" * 60)

        print(
            "Title:",
            result.get(
                "title",
            ),
        )

        print(
            "URL:",
            result.get(
                "url",
            ),
        )

        print(
            "Score:",
            result.get(
                "score",
            ),
        )

        print(
            "Content:",
            result.get(
                "content",
                "",
            )[:300],
        )