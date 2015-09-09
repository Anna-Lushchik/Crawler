__author__ = 'Anna_Lushchik'

import urllib.request
import urllib.parse
import re

class Parser():

    def __init__(self, new_url):
        self.url = new_url

    def pars(self, site):
        values = {'s':'basics', 'submit':'search'}
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(site,data)
        resp = urllib.request.urlopen(req)
        respData = resp.read()

        paragraphs = re.findall(r'<p>(.*?)</p>',str(respData))

        with open("Parser_log.txt", "a") as text_file:
            page = urllib.request.urlopen(site)
            text_file.write("\n" + page.geturl() + "\n\n")
            text_file.flush()
            page.close()
        for eachP in paragraphs:
            with open("Parser_log.txt", "a") as text_file:
                text_file.write(eachP+"\n")
                text_file.flush()

        text_file.close()
        print("\n HTML parsing was produced successfully")
