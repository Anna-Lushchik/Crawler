__author__ = 'Anna_Lushchik'

from selenium.common.exceptions import StaleElementReferenceException
import requests
import Parser

class Crawler():

    def __init__(self, new_url):
        self.url = new_url

    def crawler(self, working_links, not_working_links, url, full_url, to_be_scraped, scraped, log, driver):
        parser = Parser.Parser(url)
        printed_links = set()
        while to_be_scraped:
            site = to_be_scraped.pop(0)
            parser.pars(driver)
            links = Crawler.scraper(site, full_url, log, scraped, printed_links, driver)
            for link in links:
                if Crawler.get_status_code(driver, link)//100 == 2 or Crawler.get_status_code(driver, link)//100 == 3:
                    working_links = working_links + 1
                    if not link[0:(len(url))] == url:
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
                    not_working_links = not_working_links + 1
            if scraped in to_be_scraped:
                to_be_scraped.remove(scraped)
        return working_links, not_working_links

    def scraper(site, full_url, log, scraped, printed_links, driver):
        links = Crawler.get_links(site, full_url, log, driver)
        scraped.append(site)
        log.write('Done scraping %s\n\n' % (site))
        log.flush()
        return links.difference(printed_links)

    def get_links(site, full_url, log, driver):
        print("\n Testing %s\n" % (site))
        driver.get(site)
        elements = driver.find_elements_by_xpath("//a")
        links = set()
        for link in elements:
            try:
                if str(link.get_attribute("href"))[0:4] == "http" and str(link.get_attribute("href"))[0:19] == full_url:
                    links.add(str(link.get_attribute("href")))
            except StaleElementReferenceException:
                log.write("Stale element reference found!\n")
                log.flush()
        return links

    def get_status_code(driver, link):
        r = requests.head(link)
        return r.status_code