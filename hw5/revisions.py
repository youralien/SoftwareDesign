from wikitools import wiki, api
import networkx as nx
from operator import itemgetter
from collections import Counter
import re, random, datetime, urlparse, urllib2, simplejson, copy
import pandas as pd


# Basic Functions 

def is_ip(ip_string, masked=False):
	# '''
	# Input:
	# ip_string - A string we'd like to check if it matches the pattern of a valid IP address.
	# Output:
	# A boolean value indicating whether the input was a valid IP address.
	# '''
	if not isinstance(ip_string, str) and not isinstance(ip_string, unicode):
		return False
	if masked:
		ip_pattern = re.compile('((([\d]{1,3})|([Xx]{1,3}))\.){3}(([\d]{1,3})|([Xx]{1,3}))', re.UNICODE)
	else:
		ip_pattern = re.compile('([\d]{1,3}\.){3}([\d]{1,3})', re.UNICODE)
	if ip_pattern.match(ip_string):
		return True
	else:
		return False

def convert_to_datetime(string):
    dt = datetime.datetime.strptime(string,'%Y-%m-%dT%H:%M:%SZ')
    return dt
    
def convert_from_datetime(dt):
    string = dt.strftime('%Y%m%d%H%M%S')
    return string

def convert_datetime_to_epoch(dt):
    epochtime = (dt - datetime.datetime(1970,1,1)).total_seconds()
    return epochtime

def wikipedia_query(query_params,lang='en'):
	site = wiki.Wiki(url='http://'+lang+'.wikipedia.org/w/api.php')
	request = api.APIRequest(site, query_params)
	result = request.query()
	return result[query_params['action']]

def short_wikipedia_query(query_params,lang='en'):
	site = wiki.Wiki(url='http://'+lang+'.wikipedia.org/w/api.php')
	request = api.APIRequest(site, query_params)
	# Don't do multiple requests
	result = request.query(querycontinue=False)
	return result[query_params['action']]

def random_string(le, letters=True, numerals=False):
	def rc():
		charset = []
		cr = lambda x,y: range(ord(x), ord(y) + 1)
		if letters:
			charset += cr('a', 'z')
		if numerals:
			charset += cr('0', '9')
		return chr(random.choice(charset))
	def rcs(k):
		return [rc() for i in range(k)]
	return ''.join(rcs(le))

def clean_revision(rev):
	# We must deal with some malformed user/userid values. Some 
	# revisions have the following problems:
	# 1. no 'user' or 'userid' keys and the existence of the 'userhidden' key
	# 2. 'userid'=='0' and 'user'=='Conversion script' and 'anon'==''
	# 3. 'userid'=='0' and 'user'=='66.92.166.xxx' and 'anon'==''
	# 4. 'userid'=='0' and 'user'=='204.55.21.34' and 'anon'==''
	# In these cases, we must substitute a placeholder value
	# for 'userid' to uniquely identify the respective kind
	# of malformed revision as above. 
	revision = rev.copy()
	if 'userhidden' in revision:
		revision['user'] = random_string(15, letters=False, numerals=True)
		revision['userid'] = revision['user']
	elif 'anon' in revision:
		if revision['user']=='Conversion script':
			revision['user'] = random_string(14, letters=False, numerals=True)
			revision['userid'] = revision['user']
		elif is_ip(revision['user']):
			# Just leaving this reflection in for consistency
			revision['user'] = revision['user']
			# The weird stuff about multiplying '0' by a number is to 
			# make sure that IP addresses end up looking like this:
			# 192.168.1.1 -> 192168001001
			# This serves to prevent collisions if the numbers were
			# simply joined by removing the periods:
			# 215.1.67.240 -> 215167240
			# 21.51.67.240 -> 215167240
			# This also results in the number being exactly 12 decimal digits.
			revision['userid'] = ''.join(['0' * (3 - len(octet)) + octet \
											for octet in revision['user'].split('.')])
		elif is_ip(revision['user'], masked=True):
			# Let's distinguish masked IP addresses, like
			# 192.168.1.xxx or 255.XXX.XXX.XXX, by setting 
			# 'user'/'userid' both to a random 13 digit number
			# or 13 character string. 
			# This will probably be unique and easily 
			# distinguished from an IP address (with 12 digits
			# or characters). 
			revision['user'] = random_string(13, letters=False, numerals=True)
			revision['userid'] = revision['user']
	return revision

def cast_to_unicode(string):
    if isinstance(string,str):
        try:
            string2 = string.decode('utf8')
        except:
            try:
                string2 = string.decode('latin1')
            except:
                print "Some messed up encoding here"
    elif isinstance(string,unicode):
        string2 = string
    return string2


# User revisions

def get_user_revisions(user,dt_end,lang):
    '''
    Input: 
    user - The name of a wikipedia user with no "User:" prefix, e.g. 'Madcoverboy' 
    dt_end - a datetime object indicating the maximum datetime to return for revisions
    lang - a string (typically two characters) indicating the language version of Wikipedia to crawl

    Output:
    revisions - A list of revisions for the given article, each given as a dictionary. This will
            include all properties as described by revision_properties, and will also include the
            title and id of the source article. 
    '''
    user = cast_to_unicode(user)
    revisions = list()
    dt_end_string = convert_from_datetime(dt_end)
    result = wikipedia_query({'action':'query',
                              'list': 'usercontribs',
                              'ucuser': u"User:"+user,
                              'ucprop': 'ids|title|timestamp|sizediff',
                              #'ucnamespace':'0',
                              'uclimit': '500',
                              'ucend':dt_end_string},lang)
    if result and 'usercontribs' in result.keys():
            r = result['usercontribs']
            r = sorted(r, key=lambda revision: revision['timestamp'])
            for revision in r:
                    # Sometimes the size key is not present, so we'll set it to 0 in those cases
                    revision['sizediff'] = revision.get('sizediff', 0)
                    revision['timestamp'] = convert_to_datetime(revision['timestamp'])
                    revisions.append(revision)
    return revisions

def get_user_properties(user,lang):
    '''
    Input:
    user - a string with no "User:" prefix corresponding to the username ("Madcoverboy"
    lang - a string (usually two digits) for the language version of Wikipedia to query

    Output:
    result - a dictionary containing attrubutes about the user
    '''
    user = cast_to_unicode(user)
    result = wikipedia_query({'action':'query',
                                'list':'users',
                                'usprop':'blockinfo|groups|editcount|registration|gender',
                                'ususers':user},lang)
    return result
    
def make_user_alters(revisions):
    '''
    Input:
    revisions - a list of revisions generated by get_user_revisions

    Output:
    alters - a dictionary keyed by page name that returns a dictionary containing
        the count of how many times the user edited the page, the timestamp of the user's
        earliest edit to the page, the timestamp the user's latest edit to the page, and 
        the namespace of the page itself
    '''
    alters = dict()
    for rev in revisions:
        if rev['title'] not in alters.keys():
            alters[rev['title']] = dict()
            alters[rev['title']]['count'] = 1
            alters[rev['title']]['min_timestamp'] = rev['timestamp']
            alters[rev['title']]['max_timestamp'] = rev['timestamp']
            alters[rev['title']]['ns'] = rev['ns']
        else:
            alters[rev['title']]['count'] += 1
            alters[rev['title']]['max_timestamp'] = rev['timestamp']
    return alters



# Page revisions

def rename_on_redirect(article_title,lang='en'):
    '''
    Input:
    article_title - a string with the name of the article or page that may be redirected to another title
    lang - a string (typically two characters) indicating the language version of Wikipedia to crawl

    Output:
    article_title - a string with the name of the article or page that the redirect resolves to
    '''
    result = wikipedia_query({'titles': article_title,
                                  'prop': 'info',
                                  'action': 'query',
                                  'redirects': 'True'},lang)
    if 'redirects' in result.keys() and 'pages' in result.keys():
        article_title = result['redirects'][0]['to']
    return article_title

def get_page_revisions(article_title,dt_start,dt_end,lang):
    '''
    Input: 
    article - A string with the name of the article or page to crawl
    dt_start - A datetime object indicating the minimum datetime to return for revisions
    dt_end - a datetime object indicating the maximum datetime to return for revisions
    lang - a string (typically two characters) indicating the language version of Wikipedia to crawl
    
    Output:
    revisions - A list of revisions for the given article, each given as a dictionary. This will
            include all properties as described by revision_properties, and will also include the
            title and id of the source article. 
    '''
    article_title = rename_on_redirect(article_title)
    dt_start_string = convert_from_datetime(dt_start)
    dt_end_string = convert_from_datetime(dt_end) 
    revisions = list()
    result = wikipedia_query({'titles': article_title,
                              'prop': 'revisions',
                              'rvprop': 'ids|timestamp|user|userid|size',
                              'rvlimit': '5000',
                              'rvstart': dt_start_string,
                              'rvend': dt_end_string,
                              'rvdir': 'newer',
                              'action': 'query'},lang)
    if result and 'pages' in result.keys():
            page_number = result['pages'].keys()[0]
            try:
                r = result['pages'][page_number]['revisions']
                for revision in r:
                        revision['pageid'] = page_number
                        revision['title'] = result['pages'][page_number]['title']
                        # Sometimes the size key is not present, so we'll set it to 0 in those cases
                        revision['size'] = revision.get('size', 0)
                        revision['timestamp'] = convert_to_datetime(revision['timestamp'])
                        revisions.append(revision)
            except KeyError:
                revisions = list()
    return revisions

def make_page_alters(revisions):
    '''
    Input:
    revisions - a list of revisions generated by get_page_revisions

    Output:
    alters - a dictionary keyed by user name that returns a dictionary containing
    the count of how many times the user edited the page, the timestamp of the user's
    earliest edit to the page, the timestamp the user's latest edit to the page, and 
    the namespace of the page itself
    '''
    alters = dict()
    for rev in revisions:
        if rev['user'] not in alters.keys():
            alters[rev['user']] = dict()
            alters[rev['user']]['count'] = 1
            alters[rev['user']]['min_timestamp'] = rev['timestamp']
            alters[rev['user']]['max_timestamp'] = rev['timestamp']
        else:
            alters[rev['user']]['count'] += 1
            alters[rev['user']]['max_timestamp'] = rev['timestamp']
    return alters

def get_page_content(page_title,lang):
    '''
    Input: 
    page_title - A string with the name of the article or page to crawl
    lang - A string (typically two characters) indicating the language version of Wikipedia to crawl

    Output:
    revisions_dict - A dictionary of revisions for the given article keyed by revision ID returning a 
            a dictionary of revision attributes. These attributes include all properties as described 
            by revision_properties, and will also include the title and id of the source article. 
    '''
    article_title = rename_on_redirect(page_title)
    revisions_dict = dict()
    result = wikipedia_query({'titles': page_title,
                              'prop': 'revisions',
                              'rvprop': 'ids|timestamp|user|userid|size|content',
                              'rvlimit': '5000',
                              'action': 'query'},lang)
    if result and 'pages' in result.keys():
        page_number = result['pages'].keys()[0]
        revisions = result['pages'][page_number]['revisions']
        for revision in revisions:
            rev = dict()
            rev['pageid'] = page_number
            rev['title'] = result['pages'][page_number]['title']
            rev['size'] = revision.get('size', 0) # Sometimes the size key is not present, so we'll set it to 0 in those cases
            rev['timestamp'] = convert_to_datetime(revision['timestamp'])
            rev['content'] = revision.get('*',unicode()) # Sometimes content hidden, return with empty unicode string
            rev['links'] = link_finder(rev['content'])
            rev['username'] = revision['user']
            rev['userid'] = revision['userid']
            rev['revid'] = revision['revid']
            revisions_dict[revision['revid']] = rev
    return revisions_dict

