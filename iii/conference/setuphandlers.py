from collective.grok import gs
from iii.conference import MessageFactory as _

@gs.importstep(
    name=u'iii.conference', 
    title=_('iii.conference import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('iii.conference.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
