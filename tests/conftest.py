#configure unit tests path for importing modules
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client_test():
    with TestClient(app) as client:
        yield client


class DataManagement:
    def __init__(self):
        self.data = {}

    def add(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data[key]

    def delete(self, key):
        del self.data[key]

    def update(self, key, value):
        self.data[key] = value


@pytest.fixture(scope="session")
def data_management():
    return DataManagement()


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in a given order."""
    MODULE_ORDER = [
        "tests/v1/test_health.py",
        "tests/v1/test_users.py",
        "tests/v1/test_candidates.py",
    ]

    for item in items:
        print(item.parent.name)

    items.sort(key=lambda item: MODULE_ORDER.index(item.parent.name))
