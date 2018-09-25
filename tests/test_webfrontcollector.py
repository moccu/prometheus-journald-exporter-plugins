from datetime import datetime

import pytest
from prometheus_client.exposition import generate_latest
from pytz import utc

from journald_exporter_plugins.webfrontcollector import WebfrontCollectorPlugin


message = (
    '{"host":"www.example.com","latency":"15","contenttype":"image/jpeg",'
    '"method":"GET","proto":"HTTP/2.0","size":"72007","status":"200",'
    '"time":"2018-09-20T14:28:24Z","upstream":"http://upstreamserver:80"} '
    '[/path/to/content.jpg]'
)


class TestWebfrontCollectorPlugin:

    def test_init(self, prom_registry):
        config = {
            'webfrontcollector': {'filters': {'foo': 'bar'}}
        }
        plugin = WebfrontCollectorPlugin(prom_registry, config)
        assert plugin.filters == {'foo': 'bar'}

    def test_parse_message_valid(self, prom_registry):
        plugin = WebfrontCollectorPlugin(prom_registry, {})
        message = '{"a":1,"time":"2018-09-20T14:28:24Z"} [/path/to/content.jpg]'
        data = plugin.parse_message(message)
        expected = {
            'a': 1,
            'time': datetime(2018, 9, 20, 14, 28, 24, tzinfo=utc),
            'uri': '/path/to/content.jpg',
        }
        assert data == expected

    def test_parse_message_invalid_json(self, prom_registry):
        plugin = WebfrontCollectorPlugin(prom_registry, {})
        message = '{"a":"1"2"} [/path/to/content.jpg]'
        data = plugin.parse_message(message)
        assert data is None

    def test_update_http_requests_total(self, prom_registry):
        plugin = WebfrontCollectorPlugin(prom_registry, {})
        data = {
            'method': 'GET', 'status': '200',
            'host': 'www.example.com', 'hostname': 'example.com'
        }
        plugin.update_http_requests_total(data)
        metrics = generate_latest(prom_registry)
        assert (
            b'http_requests_total{domain="www.example.com",host="example.com",'
            b'method="GET",status="200",type="webfront"} 1.0'
        ) in metrics

    @pytest.mark.asyncio
    async def test_process(self, prom_registry):
        plugin = WebfrontCollectorPlugin(prom_registry, {})
        entry = {'MESSAGE': message, '_HOSTNAME': 'example.com'}
        await plugin.process(entry)
        metrics = list(plugin.http_requests_total.collect())
        assert len(metrics) == 1
        samples = list(metrics[0].samples)
        assert len(samples) == 1
        sample = samples[0]
        assert sample == (
            'http_requests_total',
            {
                'method': 'GET', 'status': '200', 'domain': 'www.example.com',
                'host': 'example.com', 'type': 'webfront'
            },
            1.0)
