from five import grok
from iii.conference.content.participant import IParticipant
from iii.conference.content.conference import IConference
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.error import ErrorViewSnippet
from zope.schema import ValidationError
from zope.component import getMultiAdapter

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from z3c.form import validator

from Products.statusmessages.interfaces import IStatusMessage
from zope.container.interfaces import INameChooser
import time, transaction
from collective.z3cform.norobots.widget import NorobotsFieldWidget
from collective.z3cform.norobots.validator import NorobotsValidator, WrongNorobotsAnswer


class IRegistrationForm(IParticipant):

    form.widget(captcha=NorobotsFieldWidget)
    captcha = schema.TextLine(
        title=u"",
        required=True
    )

@form.validator(field=IRegistrationForm['captcha'])
def validateCaptcha(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    norobots = getMultiAdapter((site, request), name='norobots')

    if not norobots.verify(value):
        raise WrongNorobotsAnswer

    return 

class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IConference)
    grok.require("zope.Public")
    schema = IRegistrationForm

    @property
    def description(self):
        result = u'''
        <span style="font-size:20px">
        Please read <a href="%s/details">event details</a>
        before filling out the following Registration Form
        </span>
        ''' % getSite().absolute_url()
        return result

    def create(self, data):
        title = 'participant'

        tempid = str(time.time())
        obj = _createObjectByType("iii.conference.participant", 
                self.context, tempid)

        del data['captcha']
        for k, v in data.items():
            setattr(obj, k, v)

        transaction.savepoint(optimistic=True)
        oid = INameChooser(self.context).chooseName(u'Participant', obj)

        obj.unindexObject()
        obj._setId(oid)
        self.context._delObject(tempid, suppress_events=True)
        self.context._setObject(oid, obj, set_owner=0, suppress_events=True)

        obj.setTitle('%s %s' % (obj.last_name, obj.first_name))
        obj.reindexObject()
        IStatusMessage(self.request).addStatusMessage(
            'Thank you. Your application has been received.'
        )
        return obj

    def add(self, obj):
        site = getSite()
        self.request.response.redirect(site.absolute_url())
