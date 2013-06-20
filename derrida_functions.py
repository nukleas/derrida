# This Python file uses the following encoding: utf-8
import re
import htmlentitydefs
import urlparse
import urllib2
from BeautifulSoup import BeautifulSoup
import codecs


def titleCaseIf_AllCaps(text):
    lowercase_letters = 0
    for letter in text:
        if letter.islower():
            lowercase_letters += 1
    if lowercase_letters == 0:
        print "Egads! All Caps!"
        text = text.title()
        print "Converted to: " + text
    return text


def unescape(text):
# Lifted this off effbot.org,
# it cleans up all those nasty unicode characters.
# Don't ask me how it works, honestly.
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def checkURL(url):
    if not url:
        return 0  # If it's empty, why bother?
    if not urlparse.urlparse(url).scheme:
    # If it doesn't parse, maybe it's just missing a "http://"
        url = "http://" + url
        # so lets add that and try again.
        if not urlparse.urlparse(url).scheme:
            return 0  # Womp womp
        else:
            return url
    else:
        return url


def makeSoup(url):
    try:
        page = urllib2.urlopen(url)  # Generate source from page
    except urllib2.HTTPError, err:
        if err.code == 404:
            print url + " Quoth the server: 404"
        else:
            print url + "didn't parse."
        return 0
    soup = BeautifulSoup(page)  # Start parsing source using BS
    return soup


def openRawFile(filename):
    rawdata = open(filename)  # Open the URL file.
    rawtext = rawdata.read()  # Well, read the URL file.
    rawtext = re.sub('“|”', '\"', rawtext)
    rawtext = re.sub('’|\'', '\'', rawtext)  # Damn those weird quotes!
    return unicode_the_universe(rawtext)


def findType_AddToList(rawtext, type_regex, granulate=0):
    output_list = []
    if granulate != 0:
        rawtext = rawtext.replace(' ', '\n')
    for found in re.finditer(type_regex, rawtext):
        to_append = found.group()
        output_list.append(to_append)
    print output_list
    return output_list


def DOI_Extract(DOI, result_list):
    DOI_URL = "http://dx.doi.org/" + DOI
    soup = makeSoup(DOI_URL)
    if soup == 0:
        print "Couldn't open HTML"
        return 0
    else:
        found_title = soup.head.findAll(attrs={"name": re.compile(r"(dc|article|citation)..itle")})
        DOI_title = found_title[0].get('content')
        if DOI_title == None:
            DOI_title = soup.head.title
        complete_line = DOI_URL + "|" + DOI_title
        print complete_line
        result_list.append(complete_line)
        return 1


def extractFromURL_byHTMLTag(url, tag, prefix="", suffix=""):
    url = prefix + url + suffix
    if checkURL(url) != 0:
        try:
            print checkURL(url)
            url = checkURL(url)
            soup = makeSoup(url)
#            print soup.head.title
            for line in soup.find(tag):
                print line
                page_title = titleCaseIf_AllCaps(unicode_the_universe(line.strip()))
                complete_line = url + "|" + page_title
            print complete_line.encode('utf-8')
            return {'url': url, 'page_title': page_title}
        except:
            return 0
    else:
        print "URL Failed:" + url
        return 0


def extractFromURL_byXMLTag(url, content, prefix="", suffix=""):
    url = prefix + url + suffix
    print url
    print content
    if checkURL(url) != 0:
        try:
            print checkURL(url)
            url = checkURL(url)
            soup = makeSoup(url)
            complete_line = ""
            for line in soup.findAll(attrs={'name' : re.compile(content)}):
                page_title = titleCaseIf_AllCaps(unicode_the_universe(line.get('content').strip()))
                complete_line = url + "|" + page_title
            if not complete_line:
                return 0
            else:
                print complete_line.encode('utf-8')
                return {'url': url, content: page_title}
        except:
            print "Rendering Failed for " + url
            return 0
    else:
        print "URL Failed: " + url
        return 0


def generate_New_Config():
    new_config = open('derrida_config.txt', 'a')
    new_config_list = ["Quote\t[“\"].*?[\"”]", "URL\t(((ht|f)tp(s?))\://)?(www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|mil|net|org|biz|info|name|museum|us|ca|uk)(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\;\?\'\\\+&amp;%\$#\=~_\-]+))*", "DOI\t(10\.(\d)+/([^(\s\>\"\<)])+)"]
    for item in new_config_list:
        new_config.write(item + "\n")
    new_config.close()


def unicode_the_universe(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
        return obj


