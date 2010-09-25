#!/usr/bin/python

__author__ = "Nicolas Seriot"
__date__ = "2010-09-25"
__license__ = "GPL"

"""
Download photos from Facebook photo albums.
"""

import re
import urllib
import urllib2
import cookielib
import optparse
from optparse import OptionParser

# parse the command line
parser = optparse.OptionParser("usage: %prog -e EMAIL -p PASSWORD -a ALBUM_URL")
parser.add_option("-e", "--email", dest="email")
parser.add_option("-p", "--password", dest="password")
parser.add_option("-a", "--album_url", dest="album_url")

(options, args) = parser.parse_args()

if not options.email or not options.password or not options.album_url:
    parser.error("-- please fill all options")
    exit(0)

# install an url opener with cookies
cookie_jar = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)

print "-- getting facebook cookies"
urllib2.urlopen('http://www.facebook.com/')

print "-- loggin in"
query_args = { 'email':options.email, 'pass':options.password }
encoded_args = urllib.urlencode(query_args)
url = 'https://login.facebook.com/login.php'
urllib2.urlopen(url, encoded_args)

print "-- reading album page " + url
s = urllib2.urlopen(options.album_url).read()

pattern = "http://www.facebook.com/photo.php\?pid=\d+&amp;id=\d+&amp;ref=fbx_album"
photo_page_urls = re.findall(pattern, s)
photo_page_urls = map(lambda x:x.replace('&amp;','&'), photo_page_urls)

print "-- found %d photos" % len(photo_page_urls)

photos_urls = []
for url in photo_page_urls:
    print "-- reading photo page " + url
    s = urllib2.urlopen(url).read()
    pattern = '<img src="(http://sphotos\.ak\.fbcdn.net/.*?\.jpg)" width="\d+" height="\d+" id="myphoto" />'
    photo_url = re.findall(pattern, s)[0]
    photos_urls.append(photo_url)

count = 0
for url in photos_urls:
    count += 1
    print "-- downloading " + url
    urllib.urlretrieve (url, "%d.jpg" % count)

print "-- finished"
