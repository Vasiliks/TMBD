# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import gettext
from os import environ as os_environ
from sys import version_info

plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/TMBD/'
PluginLanguageDomain = 'TMBD'
PluginLanguagePath = plugin_path + 'locale'

try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

def localeInit():
    if isDreamOS:
        lang = language.getLanguage()[:2]
        os_environ['LANGUAGE'] = lang
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

if isDreamOS:
    _ = lambda txt: (gettext.dgettext(PluginLanguageDomain, txt) if txt else '')
    localeInit()
    language.addCallback(localeInit)
else:

    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            return gettext.gettext(txt)

    language.addCallback(localeInit())

# Disable certificate verification on python 2.7.9
sslContext = None
if version_info >= (2, 7, 9):
        try:
                import ssl
                sslContext = ssl._create_unverified_context()
        except:
                pass

