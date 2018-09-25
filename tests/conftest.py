import pytest
from prometheus_client.core import CollectorRegistry


@pytest.fixture
def prom_registry():
    """
    Prometheus Registry for plugin tests

    """
    return CollectorRegistry(auto_describe=True)
