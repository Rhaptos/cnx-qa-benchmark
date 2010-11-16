# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""

import unittest
from test_QA import QA

class Prod(QA):
    """ This test uses the Production.conf configuration file
    """

    def setUp(self):
        """Setting up test, in current case just setting the server url."""
        self.logd("setUp")
        self.label = "Anonymous Tests (Production)"
        self.server_url = self.conf_get('main', 'url')


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
