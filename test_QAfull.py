# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""
import unittest, random, gc
from funkload.FunkLoadTestCase import FunkLoadTestCase
from test_QA import QA


class QA(QA):
    """ This test uses the AnonPlone.conf configuration file
    """

    total = 500

    def _browseURL(self):
        server_url = self.server_url
        all_urls = open('urls.txt', 'r').readlines()

        urls = []
        count = 0
        while len(urls) < self.total:
            url = random.choice(all_urls)
            if url not in urls:
                urls.append(url)

                url = url.split('http://cnx.org', 1)[1].replace('\n','')
                if url:
                    count += 1
                    try:
                        self.get(server_url + url, description="Get %s" % url,
                             ok_codes=[200,204,301,302,304,404,500])
                    except Exception, exc:
                        raise
                    if count > 30:
                        count = 0
                        gc.collect()


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
