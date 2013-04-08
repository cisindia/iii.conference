from five import grok
from iii.conference.content.participant import IParticipant
from iii.conference.content.conference import IConference
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.recaptcha import ReCaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
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

from Products.statusmessages.interfaces import IStatusMessage
from zope.container.interfaces import INameChooser
import time, transaction

class IRegistrationForm(IParticipant):

    form.widget(captcha=ReCaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)


@form.validator(field=IRegistrationForm['captcha'])
def validateCaptcha(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = getMultiAdapter((site, request), name='recaptcha')

    if not captcha.verify():
        raise ValidationError(
        'The code you entered was wrong, please enter the new one.')


class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IConference)
    grok.require("zope.Public")
    schema = IRegistrationForm
    label = u"Register for this event"


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

        self.context.manage_renameObject(tempid, oid)

        obj.reindexObject()
        IStatusMessage(self.request).addStatusMessage(
            'Thank you. You are now registered.'
        )
        return obj

    def add(self, obj):
        pass
