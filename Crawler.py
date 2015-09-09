__author__ = 'Anna_Lushchik'

from selenium.common.exceptions import StaleElementReferenceException
import time
import urllib
import re
import Parser

class Crawler():

    def __init__(self, new_url):
        self.url = new_url

    def timer(f):
        def tmp(*args, **kwargs):
            t = float(time.time())
            res = f(*args, **kwargs)
            real_time = float(time.time()-t)
            print("Time: %f" % float(real_time/60), "minutes")
            return res
        return tmp

    @timer
    def crawler(self, working_links, not_working_links, url, to_be_scraped, scraped, log):

        printed_links = set()
        while to_be_scraped:
            site = to_be_scraped.pop(0)

            links = Crawler.scraper(site, url, log, scraped, printed_links)
            for link in links:
                if Crawler.get_status_code(link)//100 == 2 or Crawler.get_status_code(link)//100 == 3:
                    working_links = working_links + 1
                    if link not in printed_links:
                        print(link)
                        printed_links.add(link)
                        to_be_scraped.append(link)
                        continue
                    elif link in scraped:
                        print("%s has already been scraped" % (link))
                        continue
                    elif link in to_be_scraped:
                        print("%s is already on the queue" % (link))
                        continue
                    else:
                        print("adding %s to the queue" % (link))
                        to_be_scraped.append(link)
                else:
                    print(link, "status code - ", Crawler.get_status_code(link))
                    not_working_links = not_working_links + 1
            if scraped in to_be_scraped:
                to_be_scraped.remove(scraped)
        return working_links, not_working_links

    def scraper(site, url, log, scraped, printed_links):
        links = Crawler.get_links(site, url, log)
        scraped.append(site)
        log.write('Done scraping %s\n\n' % (site))
        log.flush()
        return links.difference(printed_links)

    def get_links(site, url, log):
        print("\n Testing %s\n" % (site))
        parser = Parser.Parser(site)
        parser.pars(site)
        links = set()
        page = urllib.request.urlopen(site)
        html = page.read()
        page.close()
        elements = re.findall('.*?href="(.*?)"',str(html))
        for link in elements:
            try:
                if "http" not in link:
                    if "phoenix" in link or "javascript" in link:
                        link = url + "/" + link
                        links.add(link)
                    else:
                        link = url + link
                        links.add(link)
            except StaleElementReferenceException:
                log.write("Stale element reference found!\n")
                log.flush()
        return links

    def get_status_code(link):
        conn = urllib.request.urlopen(link)
        result = conn.getcode()
        conn.close()
        return result
