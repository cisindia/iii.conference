from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from iii.conference import MessageFactory as _


# Interface class; used to define content-type schema.

class IParticipant(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True
    )
    
    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True
    )

    address = schema.Text(
            title=_(u'Address'),
            required = True,
            )

    email = schema.TextLine(
        title=_(u'Email'),
        required=True
    )

    website = schema.TextLine(
        title=_(u'Website'),
        required=False
    )

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=True
    )

    gender = schema.Choice(
        title=_(u'Gender'),
        values=['male','female'],
        required=True
    )

    date_of_birth = schema.Date(
        title=_(u'Date of Birth'),
        required=True
    )

    profession = schema.Choice(
        title=_(u'Profession'),
        values=[u'Student/Research Scholar', 'Academician/Scientist',
        'Industrial person', 'Activist'],
        required=True
    )

    discipline = schema.TextLine(
        title=_(u'Discipline'),
        required=True
    )

    organization = schema.TextLine(
        title=_(u'Organization'),
        required=False
    )

    designation = schema.TextLine(
        title=_(u'Designation'),
        required=False
    )

    country = schema.TextLine(
        title=_(u'Country of Residence'),
        required=True
    )

    qualification = schema.TextLine(
        title=_(u'Highest Qualification Achieved'),
        required=True
    )

    writeup = NamedBlobFile(
        title=_(u'Expression of Interest write-up'),
        description=_(u'250-300 words'),
        required=False
    )

    need_scholarship = schema.Choice(
        title=_(u'Do you need scholarship to attend the institute'),
        required=True,
        values=['no', 'yes', 'partly'],
    )
