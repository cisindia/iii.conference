from five import grok
from plone.directives import dexterity, form
from iii.conference.content.participant import IParticipant

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IParticipant)
    grok.require('zope2.View')
    grok.template('participant_view')
    grok.name('view')

