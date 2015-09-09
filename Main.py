__author__ = 'Anna_Lushchik'

import Crawler

url = 'http://epam.com'

to_be_scraped = []
scraped = []
working_links = 0
not_working_links = 0
log = open('Crawler_log.txt', 'w')


crawler = Crawler.Crawler(url)

to_be_scraped.append(url)
working_links, not_working_links = crawler.crawler(working_links, not_working_links, url, to_be_scraped, scraped, log)

log.write('Working links -  %s\n' % (working_links))
log.write('Not working links - %s\n' % (not_working_links))
log.close()