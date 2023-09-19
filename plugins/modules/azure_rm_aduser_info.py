#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_aduser_info

version_added: "1.4.0"

short_description: Get Azure Active Directory user info

description:
    - Get Azure Active Directory user info.

options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    object_id:
        description:
            - The object id for the user.
            - returns the user who has this object ID.
            - Mutually exclusive with I(user_principal_name), I(attribute_name), I(odata_filter) and I(all).
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - returns the user who has this principal name.
            - Mutually exclusive with I(object_id), I(attribute_name), I(odata_filter) and I(all).
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If I(attribute_name) is not a collection type it will return users where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will return users where I(attribute_value) is in I(attribute_name).
            - Mutually exclusive with I(object_id), I(user_principal_name), I(odata_filter) and I(all).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If I(attribute_name) is not a collection type it will return users where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will return users where I(attribute_value) is in I(attribute_name).
            - Required together with I(attribute_name).
        type: str
    odata_filter:
        description:
            - Returns users based on the the OData filter passed into this parameter.
            - Mutually exclusive with I(object_id), I(attribute_name), I(user_principal_name) and I(all).
        type: str
    all:
        description:
            - If C(True), will return all users in tenant.
            - If C(False) will return no users.
            - It is recommended that you instead identify a subset of users and use filter.
            - Mutually exclusive with I(object_id), I(attribute_name), I(odata_filter) and I(user_principal_name).
        type: bool
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
    - name: Using user_principal_name
      azure.azcollection.azure_rm_aduser_info:
        user_principal_name: user@contoso.com
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using object_id
      azure.azcollection.azure_rm_aduser_info:
        object_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using attribute mailNickname - not a collection
      azure.azcollection.azure_rm_aduser_info:
        attribute_name: mailNickname
        attribute_value: users_mailNickname
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using attribute proxyAddresses - a collection
      azure.azcollection.azure_rm_aduser_info:
        attribute_name: proxyAddresses
        attribute_value: SMTP:user@contoso.com
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using Filter mailNickname
      azure.azcollection.azure_rm_aduser_info:
        odata_filter: mailNickname eq 'user@contoso.com'
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    - name: Using Filter proxyAddresses
      azure.azcollection.azure_rm_aduser_info:
        odata_filter: proxyAddresses/any(c:c eq 'SMTP:user@contoso.com')
        tenant: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

RETURN = '''
object_id:
    description:
        - The object_id for the user.
    type: str
    returned: always
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
display_name:
    description:
        - The display name of the user.
    returned: always
    type: str
    sample: John Smith
user_principal_name:
    description:
        - The principal name of the user.
    returned: always
    type: str
    sample: jsmith@contoso.com
mail_nickname:
    description:
        - The mail alias for the user.
    returned: always
    type: str
    sample: jsmith
mail:
    description:
        - The primary email address of the user.
    returned: always
    type: str
    sample: John.Smith@contoso.com
account_enabled:
    description:
        - Whether the account is enabled.
    returned: always
    type: bool
    sample: False
user_type:
    description:
        - A string value that can be used to classify user types in your directory.
    returned: always
    type: str
    sample: Member
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase


class AzureRMADUserInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            all=dict(type='bool'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.user_principal_name = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.all = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name', 'all']]

        super(AzureRMADUserInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False,
                                                mutually_exclusive=mutually_exclusive,
                                                required_together=required_together,
                                                required_one_of=required_one_of,
                                                is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        ad_users = []

        try:
            client = self.get_msgraph_client()

            if self.user_principal_name is not None:
                ad_users = [client.get('/users/' + self.user_principal_name).json()]
            elif self.object_id is not None:
                ad_users = [client.get('/users/' + self.object_id).json()]
            elif self.attribute_name is not None and self.attribute_value is not None:
                response = client.get('/users/').json()['value']
                for item in response:
                    if item[self.attribute_name] == self.attribute_value:
                        ms_user.append(item)
            elif self.all:
                ad_user = client.get('/users/').json()['value']
            elif self.all:
                ad_users = list(client.users.list())

            self.results['ad_users'] = [self.to_dict(user) for user in ad_users]

        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        return self.results

    def to_dict(self, object):
        if object is None:
            return

        return dict(
            object_id=object['id'],
            display_name=object['displayName'],
            user_principal_name=object['userPrincipalName'],
            mail=object['mail'],
            given_name=object['givenName'],
            surname=object['surname'],
        )


def main():
    AzureRMADUserInfo()


if __name__ == '__main__':
    main()
