# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""
import unittest, random, gc
from funkload.FunkLoadTestCase import FunkLoadTestCase


class QA(FunkLoadTestCase):
    """ This test uses the AnonPlone.conf configuration file
    """
    total = 30

    def setUp(self):
        """Setting up test, in current case just setting the server url."""
        self.logd("setUp")
        self.label = "Anonymous Tests (QA)"
        self.server_url = self.conf_get('main', 'url')

    def _browseURL(self):
        server_url = self.server_url
        get_urls = open('urls-short.txt', 'r').readlines()

        #urls = []
        #while len(urls) < self.total:
        #    url = random.choice(get_urls)
        #    if url not in urls:
        #        urls.append(url)

        count = 0
        for get_url in get_urls:
            get_url = get_url.split('http://cnx.org', 1)[1].replace('\n','')
            if get_url:
                self.get(server_url + get_url,
                         description="Get %s" % get_url)
                count += 1
                if count > 30:
                    gc.collect()
                    count = 0

    def test_loads(self):
        """Loads some URLs and execute some searches."""
        self._browseURL()

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
