# -*- coding: UTF-8 -*-
from Components.config import config
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor
import random, locale, re
# https://github.com/wagnerrp/pytmdb3/tree/master/tmdb3
import tmdb3

configs = None

def setLocale(lng):
    global configs
    configs = {}
    configs['locale'] = lng

def getLocale():
    return configs.get('locale')

def cutName(eventName=''):
    '''
    Used to filter out various abbreviations and data
    not involved in the requests to the TMDB API

    :param eventName: The text that needs to be filter out
    :type eventName: str
    :rtype: str
    '''
    if eventName:
        if config.plugins.tmbd.locale.value in ('ru', 'ua', 'by', 'kz'):
            pattern = re.compile(
                               r'[0-9]+\+|'
                               r'([\(\[]).*?([\)\]])|'
                               r'\d{1,3}\-я|'
                               r'(с|С)ерия|'
                               r'\d{1,3}\s(с|C|c|C)\-н|'
                               r'\d{1,3}\s+(с|C|c|C)($|\.|\s+\.)|'
                               r'(с|С)езон\s\d{1,3}|'
                               r'(с|С)езон|'
                               r'(х|Х|м|М|x|X|т|Т|T)/(Ф|ф|С|с|C|c)|'
                               r'(ч|Ч)\.\s+\d{1,3}|'
                               r'(ч|Ч)асть|'
                               r'(\s\-(.*?).*)|'
                               r'\^|\{|\}|\$\|\/|\*|\?|«|»|"|<|\|:|>|,|\|', re.DOTALL)

            return pattern.sub('', eventName).strip()

    return eventName

def decodeCertification(releases, country):
    country = str(country)
    releases = { k:v for (k,v) in releases.items() if v.certification }

    if releases.has_key(country):
        return releases[country].certification

    k, v = random.choice(list(releases.items()))
    cert = releases[k].certification

    if k in ('US', 'NZ', 'IN', 'GB', 'FR', 'DE', 'CA', 'AU'):
    	cert = { 'US': {
			'NR'   : 'VSR-0',
			'G'    : 'VSR-0',
			'PG'   : 'VSR-6',
			'PG-13': 'VSR-12',
			'R'    : 'VSR-16',
			'NC17' : 'VSR-18', },
             'NZ': {
			'G' : 'VSR-6',
			'PG': 'VSR-6',
			'M' : 'VSR-16',
			'13': 'VSR-12',
			'15': 'VSR-16',
			'16': 'VSR-16',
			'18': 'VSR-18',
			'R' : 'VSR-16', },
             'IN': {
			'U' : 'VSR-0',
			'UA': 'VSR-12',
			'A' : 'VSR-18', },
             'GB': {
			'U'  : 'VSR-0',
			'PG' : 'VSR-6',
			'12A': 'VSR-12',
			'12' : 'VSR-12',
			'15' : 'VSR-16',
			'18' : 'VSR-18',
			'18R': 'VSR-18', },
             'FR': {
			'U'  : 'VSR-0',
			'10' : 'VSR-12',
			'12' : 'VSR-12',
			'16' : 'VSR-16',
			'18' : 'VSR-18', },
             'DE' : {
			'0'  : 'VSR-0',
			'6'  : 'VSR-6',
			'12' : 'VSR-12',
			'16' : 'VSR-16',
			'18' : 'VSR-18', },
             'CA': {
			'G'  : 'VSR-0',
			'PG' : 'VSR-6',
			'14A': 'VSR-12',
			'18A': 'VSR-18',
			'R'  : 'VSR-18',
			'A'  : 'VSR-18', },
             'AU': {
			'E'  : 'VSR-6',
			'G'  : 'VSR-0',
			'PG' : 'VSR-6',
			'M'  : 'VSR-6',
			'MA15+': 'VSR-16',
			'R18+' : 'VSR-18',
			'X18+' : 'VSR-18',
			'RC'   : 'VSR-18', },
	   }[k].get(cert, cert)

    if country in ('UK', 'RU', 'BY', 'KZ') and cert:  #  PEGI to RARS
	return '%s+' % (cert[4:] if cert.startswith('VSR') else cert)
    else:
	return cert

def nextImageIndex(movie):
    if len(movie['images']) > 1:
        item = movie['images'].pop(0)
        movie['images'].append(item)

def prevImageIndex(movie):
    if len(movie['images']) > 1:
        item = movie['images'].pop(-1)
        movie['images'].insert(0, item)

def init_tmdb3(alternative_lang=None):
    tmdb3.set_key('1f834eb425728133b9a2c1c0c82980eb')
    tmdb3.set_cache('null')
    lng = alternative_lang or config.plugins.tmbd.locale.value
    try:
        tmdb3.set_locale(lng, lng.upper())
    except:
        tmdb3.set_locale('en', 'GB')
    return tmdb3


def main():
    setLocale('de')
    tmdb3 = init_tmdb3()
    res = tmdb3.searchMovie('F\xc3\xbcr immer Liebe')
    print res
    movie = res[0]
    print movie.title
    print movie.releasedate.year
    print movie.overview
    for p in movie.posters:
        print p

    for p in movie.backdrops:
        print p

    p = movie.poster
    print p
    print p.sizes()
    print p.geturl()
    print p.geturl('w185')
    p = movie.backdrop
    print p
    print p.sizes()
    print p.geturl()
    print p.geturl('w300')
    crew = [ x.name for x in movie.crew if x.job == 'Director' ]
    print crew
    crew = [ x.name for x in movie.crew if x.job == 'Author' ]
    print crew
    crew = [ x.name for x in movie.crew if x.job == 'Producer' ]
    print crew
    crew = [ x.name for x in movie.crew if x.job == 'Director of Photography' ]
    print crew
    crew = [ x.name for x in movie.crew if x.job == 'Editor' ]
    print crew
    crew = [ x.name for x in movie.crew if x.job == 'Production Design' ]
    print crew
    cast = [ x.name for x in movie.cast ]
    print cast
    genres = [ x.name for x in movie.genres ]
    print genres
    studios = [ x.name for x in movie.studios ]
    print studios
    countries = [ x.name for x in movie.countries ]
    print countries


if __name__ == '__main__':
    main()
