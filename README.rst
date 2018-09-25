prometheus-journald-exporter-plugins
====================================

Plugins for prometheus-journald-exporter used at Moccu.

Usage
-----

Example configuration:

.. code-block:: yaml

    plugindirs:
      - /path/to/plugins

    plugins:
      - webfrontcollector.WebfrontCollectorPlugin

    webfrontcollector:
      filters:
        - CONTAINER_TAG: webfront


Development
-----------

.. code-block:: shell

    pipenv install --python 3.6 --dev
    pipenv shell
    pip install -e .
    pytest
