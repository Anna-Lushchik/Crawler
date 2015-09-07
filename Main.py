__author__ = 'Anna_Lushchik'

from selenium import webdriver
import Crawler

url = 'http://epam.com'
full_url = 'http://www.epam.com'

to_be_scraped = []
scraped = []
working_links = 0
not_working_links = 0
log = open('Crawler_log.txt', 'w')


crawler = Crawler.Crawler(url)

to_be_scraped.append(url)
driver = webdriver.Firefox(webdriver.firefox.firefox_profile.FirefoxProfile())
working_links, not_working_links = crawler.crawler(working_links, not_working_links, url, full_url, to_be_scraped, scraped, log, driver)
driver.close()

log.write('Working links -  %s\n' % (working_links))
log.write('Not working links - %s\n' % (not_working_links))
log.close()