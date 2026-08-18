"""
Shared pytest configuration.
"""

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.session",
    "tests.fixtures.unit_of_work",
    "tests.fixtures.company",
]
