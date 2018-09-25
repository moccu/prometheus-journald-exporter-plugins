prometheus-journald-exporter-plugins
====================================

Plugins for prometheus-journald-exporter used at Moccu.

Usage
-----

Installation:

.. code-block:: shell

    pip install https://github.com/moccu/prometheus-journald-exporter-plugins.git#journald_exporter_plugins

Example configuration:

.. code-block:: yaml

    plugins:
      - journald_exporter_plugins.webfrontcollector.WebfrontCollectorPlugin

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
