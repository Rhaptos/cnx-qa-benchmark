# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""
import unittest, random, gc, requests, json
from funkload.FunkLoadTestCase import FunkLoadTestCase


class Students(FunkLoadTestCase):
    """ This test uses the Students.conf configuration file
    """

    def setUp(self):
        """Setting up test, in current case just setting the server url."""
        self.logd("setUp")
        self.label = "Anonymous Tests (Student)"
        self.server_url = self.conf_get('main', 'url')
        cids = [i.strip() for i in open('collids.txt', 'r').readlines()]
        cidsvers = []
        for id in cids: 
            res = requests.get(self.server_url+'/content/%s/latest/getVersion'% id )
            cidsvers.append((id,res.content))
        modurl_template=self.server_url+'/content/{}/latest/?collection={}/latest'
        pdfurl_template=self.server_url+'/content/{}/{}/pdf'

        self.modurls = []
        self.pdfurls = []
        for c,v in cidsvers:
            self.pdfurls.append(pdfurl_template.format(c,v))
            r = requests.get(self.server_url+'/content/%s/latest/containedModuleIds' % c)
            mids=json.loads(r.content.replace("'",'"'))
            for m in mids:
                self.modurls.append(modurl_template.format(m,c))


    def _browseURL(self):
        server_url = self.server_url

        # Model a student: either download a PDF 10%, or read 3 consecutive pages 
        if random.random() < 0.1:
            urls = [random.choice(self.pdfurls)]
        else:
            start = random.choice(xrange(len(self.modurls)-2))
            urls = self.modurls[start:start+3]
        for url in urls:
            self.get(url, description="Get %s" % url)

    def test_loads(self):
        """Loads some URLs and execute some searches."""
        self._browseURL()

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
