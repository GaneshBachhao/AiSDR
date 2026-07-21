from app.knowledge.catalog_service import CatalogService


service = CatalogService()


def test_get_all_sectors():

    sectors = service.get_all_sectors()

    assert len(sectors) > 0


def test_get_services():

    services = service.get_services(
        "Manufacturing"
    )

    assert len(services) > 0


def test_unknown_sector():

    services = service.get_services(
        "Unknown"
    )

    assert services == []