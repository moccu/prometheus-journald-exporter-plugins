import json
import re

from dateutil.parser import parse
from prometheus_client import Counter


class WebfrontCollectorPlugin:
    type = 'collector'
    filters = {'CONTAINER_TAG': 'webfront', 'PRIORITY': 6}
    regex = re.compile(r'^({.*}) \[(.*?)\]$')

    def __init__(self, prom_registry, config):
        plugin_config = config.get('webfrontcollector', {})
        self.filters = plugin_config.get('filters', self.filters)
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total number of HTTP requests',
            ['method', 'status', 'domain', 'host', 'type'],
            registry=prom_registry)

    async def process(self, entry):
        message = entry.get('MESSAGE', '')
        hostname = entry.get('_HOSTNAME')
        data = self.parse_message(message)
        if not data or not hostname:
            return
        data['hostname'] = hostname
        self.update_http_requests_total(data)

    def parse_message(self, message):
        match = self.regex.search(message)
        if not match:
            return
        try:
            data = json.loads(match.group(1))
        except json.decoder.JSONDecodeError:
            return
        data['uri'] = match.group(2)
        if 'time' in data:
            data['time'] = parse(data['time'])
        return data

    def update_http_requests_total(self, data):
        self.http_requests_total.labels(
            method=data['method'],
            status=data['status'],
            domain=data['host'],
            host=data['hostname'],
            type='webfront',
        ).inc()
