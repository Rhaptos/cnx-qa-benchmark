# -*- coding: utf-8 -*-
""" FunkLoad anonymous tests.
"""
import unittest, random, gc, requests, json
from funkload.FunkLoadTestCase import FunkLoadTestCase
import psycopg2


class Students(FunkLoadTestCase):
    """ This test uses the Students.conf configuration file
    """

    def setUp(self):
        """Setting up test, loading and parsing content ids of various sorts"""
        self.logd("setUp")
        self.label = "Anonymous Tests (Students)"
        self.server_url = self.conf_get('main', 'url')
        self.legacy_server_url = self.conf_get('main', 'legacy_url')
        self.dbconn = self.conf_get('main', 'dbconn')
        conn = psycopg2.connect(self.dbconn)
        cur = conn.cursor()
        cur.execute("select moduleid,version,uuid,concat_ws('.',major_version,minor_version) from latest_modules")
        res=cur.fetchall()
        content_info={}
        for r in res:
            content_info[r[0]] = r
        collids_file_path = self.conf_get('test_loads', 'collid_file')
        cids = [i.strip() for i in open(collids_file_path, 'r').readlines()]
        cidsvers = []
        for id in cids: 
            cidsvers.append(content_info[id])
        
        uuidsvers=[]
        modurl_template=self.server_url+'/content/{}/latest/?collection={}/latest'
        pdfurl_template=self.server_url+'/content/{}/{}/pdf'
        rewrite_url_template=self.server_url+'/contents/{}@{}:{}'
        rewrite_exporturl_template=self.server_url+'/exports/{}@{}.{}'

        self.modurls = []
        self.rewriteurls = []
        self.pdfurls = []
        self.exporturls = []
        for c,v,u,uv in cidsvers:
            self.pdfurls.append(pdfurl_template.format(c,v))
            self.exporturls.append(rewrite_exporturl_template.format(u,uv,'pdf'))
            self.exporturls.append(rewrite_exporturl_template.format(u,uv,'epub'))
            r = requests.get(self.legacy_server_url+'/content/%s/latest/containedModuleIds' % c)
            mids=json.loads(r.content.replace("'",'"'))
            for i,m in enumerate(mids):
                self.modurls.append(modurl_template.format(m,c))
                self.rewriteurls.append(rewrite_url_template.format(u,uv,i))
        with open('rewrite_urls.txt','w') as file:
            file.write('\n'.join(self.rewriteurls))
            file.write('\n')

        with open('export_urls.txt','w') as file:
            file.write('\n'.join(self.exporturls))
            file.write('\n')

        with open (self.conf_get('main','urls_json')) as jsonfile:
            crawled_urls = json.load(jsonfile)['content']
            self.json_pages = {}
            for page in crawled_urls:
                self.json_pages[page['url']] = page
            self.rewriteurls = self.json_pages.keys()
        
    def _extractPageURLs(self,url):
        """takes a top of page URL, returns list of URLs to load"""
        urls = []
        page = self.json_pages[url]
        for key in page.keys():
            if key == 'url':
                urls.append(page[key])
            else:
                urls.extend(page[key])
        return urls
            

    def _browseURL(self):
        server_url = self.server_url

        # Model a student: either download a PDF 10%, or read 3 consecutive pages 
        if random.random() < 0.1:
            url = random.choice(self.exporturls)
            self.get(url, description="Get %s" % url)
        else:
            start = random.choice(xrange(len(self.rewriteurls)-2))
            page_urls = self.rewriteurls[start:start+3]
            for page in page_urls:
                for url in self._extractPageURLs(page):
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
