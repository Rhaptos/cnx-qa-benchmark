# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""
import unittest, random, gc
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import xmlrpc_get_credential

from base64 import encodestring
from urllib import quote as urlquote
from urlparse import urlparse
from Cookie import Morsel


class QAauth(FunkLoadTestCase):
    """ This test uses the QAauth.conf configuration file
    """
    total = 30

    def setUp(self):
        """Setting up test, in current case just setting the server url."""
        self.logd("setUp")
        self.label = "Authenticated Tests (QAauth)"
        self.server_url = self.conf_get('main', 'url')
        hostname = urlparse(self.server_url)[1].split(':')[0]
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')

        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                           credential_port,
                                                           'members')

        # Set the zope cookie. This is a little evil but avoids having to
        # call the login page.
        morsel = Morsel()
        morsel.key = '__ac'
        morsel.value = morsel.coded_value = urlquote(
            encodestring('%s:%s' % (self.login, self.password)))
        self._browser.cookies = {
            hostname: {
                '/': {
                    '__ac': morsel
                }
            }
        }



    def _browseURL(self):
        server_url = self.server_url
        auth_urls = open('urls-auth.txt', 'r').readlines()
        content_urls = open('urls-short.txt', 'r').readlines()
        get_urls = auth_urls + content_urls

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
