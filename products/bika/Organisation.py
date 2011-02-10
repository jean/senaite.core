from AccessControl import ClassSecurityInfo
from Products.ATExtensions.ateapi import RecordWidget
from Products.Archetypes.public import *
from Products.bika.CustomFields import AddressField
from Products.bika import PROJECTNAME
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from plone.app.folder.folder import ATFolder, ATFolderSchema

schema = ATFolderSchema.copy() + BaseSchema.copy() + ManagedSchema((
    StringField('Name',
        required = 1,
        searchable = '1'
    ),
    StringField('TaxNumber',
        widget = StringWidget(
            label = 'Tax number',
            label_msgid = 'label_taxnumber',
        ),
    ),
    StringField('Phone',
        widget = StringWidget(
            label = 'Phone',
            label_msgid = 'label_phone',
        ),
    ),
    StringField('Fax',
            widget = StringWidget(
            label = 'Fax',
            label_msgid = 'label_fax',
        ),
    ),
    StringField('EmailAddress',
        schemata = 'Address',
        widget = StringWidget(
            label = 'Email address',
            label_msgid = 'label_emailaddress'
        ),
        validators = ('isEmail',)
    ),
    AddressField('PhysicalAddress',
        schemata = 'Address',
        widget = RecordWidget(
           macro = 'custom_address_widget',
           label = 'Physical address',
           label_msgid = 'label_physical_address',
        ),
    ),
    AddressField('PostalAddress',
        schemata = 'Address',
        widget = RecordWidget(
           macro = 'custom_address_widget',
           label = 'Postal address',
           label_msgid = 'label_postal_address',
        ),
    ),
    AddressField('BillingAddress',
        schemata = 'Address',
        widget = RecordWidget(
           macro = 'custom_address_widget',
           label = 'Billing address',
           label_msgid = 'label_billing_address',
        ),
    ),
    StringField('AccountNumber',
        widget = StringWidget(
            label = 'Account number',
            label_msgid = 'label_accountnumber',
        ),
    ),
),
)

IdField = schema['id']
IdField.widget.visible = {'edit': 'visible', 'view': 'invisible'}
# Don't make title required - it will be computed from the Organisation's
# Name
TitleField = schema['title']
TitleField.required = 0
TitleField.widget.visible = {'edit': 'hidden', 'view': 'invisible'}

class Organisation(VariableSchemaSupport, ATFolder):
    security = ClassSecurityInfo()
    schema = schema

    security.declareProtected(CMFCorePermissions.View, 'getSchema')
    def getSchema(self):
        return self.schema

    def Title(self):
        """ Return the Organisation's Name as its title """
        return self.getField('Name').get(self)

    def getPossibleAddresses(self):
        return ['PhysicalAddress', 'PostalAddress', 'BillingAddress']

registerType(Organisation, PROJECTNAME)
