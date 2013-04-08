from five import grok
from plone.directives import dexterity, form
from iii.conference.content.conference import IConference

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IConference)
    grok.require('zope2.View')
    grok.template('conference_view')
    grok.name('view')

