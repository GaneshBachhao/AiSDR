from app.knowledge.sector_matcher import SectorMatcher

matcher = SectorMatcher()


def test_manufacturing():

    result = matcher.match(
        "Industrial automation factory machinery"
    )

    assert result["sector"] == "Manufacturing"


def test_retail():

    result = matcher.match(
        "Online retail ecommerce shopping"
    )

    assert result["sector"] == "Retail"


def test_unknown():

    result = matcher.match(
        "Quantum space propulsion"
    )

    assert result["sector"] == "Unknown"