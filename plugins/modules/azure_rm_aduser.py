#!/usr/bin/python
#
# Copyright (c) 2020 Cole Neubauer, (@coleneubauer)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: azure_rm_aduser

version_added: "1.5.0"

short_description: Modify an Azure Active Directory user

description:
    - Create, delete, and update an Azure Active Directory user.

options:
    tenant:
        description:
            - The tenant ID.
        type: str
        required: True
    state:
        description:
            - State of the ad user. Use C(present) to create or update an ad user and C(absent) to delete an ad user.
        type: str
        default: present
        choices:
            - absent
            - present
    object_id:
        description:
            - The object id for the user.
            - Updates or deletes the user who has this object ID.
            - Mutually exclusive with I(user_principal_name), I(attribute_name), and I(odata_filter).
        type: str
    account_enabled:
        description:
            - A boolean determing whether or not the user account is enabled.
            - Used when either creating or updating a user account.
        type: bool
    display_name:
        description:
            - The display name of the user.
            - Used when either creating or updating a user account.
        type: str
    given_name:
        description:
            - The given name for the user.
            - Used when either creating or updating a user account.
        type: str
    surname:
        description:
            - The surname for the user.
            - Used when either creating or updating a user account.
        type: str
    immutable_id:
        description:
            - The immutable_id of the user.
            - Used when either creating or updating a user account.
        type: str
    mail:
        description:
            - The primary email address of the user.
            - Used when either creating or updating a user account.
        type: str
    mail_nickname:
        description:
            - The mail alias for the user.
            - Used when either creating or updating a user account.
        type: str
    password_profile:
        description:
            - The password for the user.
            - Used when either creating or updating a user account.
        type: str
    usage_location:
        description:
            - A two letter country code, ISO standard 3166.
            - Required for a user that will be assigned licenses due to legal requirement to check for availability of services in countries.
            - Used when either creating or updating a user account.
        type: str
    user_type:
        description:
            - A string value that can be used to classify user types in your directory, such as Member and Guest.
            - Used when either creating or updating a user account.
        type: str
    user_principal_name:
        description:
            - The principal name of the user.
            - Creates, updates, or deletes the user who has this principal name.
            - Mutually exclusive with I(object_id), I(attribute_name), and I(odata_filter).
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to I(attribute_value).
            - If I(attribute_name) is not a collection type it will update or delete the user where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will update or delete the user where I(attribute_value) is in I(attribute_name).
            - Mutually exclusive with I(object_id), I(user_principal_name), and I(odata_filter).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match I(attribute_name) to.
            - If I(attribute_name) is not a collection type it will update or delete the user where I(attribute_name) is equal to I(attribute_value).
            - If I(attribute_name) is a collection type it will update or delete the user where I(attribute_value) is in I(attribute_name).
            - Required together with I(attribute_name).
        type: str
    odata_filter:
        description:
            - Filter that can be used to specify a user to update or delete.
            - Mutually exclusive with I(object_id), I(attribute_name), and I(user_principal_name).
        type: str
extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Cole Neubauer(@coleneubauer)

'''

EXAMPLES = '''
- name: Create user
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "present"
    account_enabled: "True"
    display_name: "Test_{{ user_principal_name }}_Display_Name"
    password_profile: "password"
    mail_nickname: "Test_{{ user_principal_name }}_mail_nickname"
    immutable_id: "{{ object_id }}"
    given_name: "First"
    surname: "Last"
    user_type: "Member"
    usage_location: "US"
    mail: "{{ user_principal_name }}@contoso.com"

- name: Update user with new value for account_enabled
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "present"
    account_enabled: "False"

- name: Delete user
  azure_rm_aduser:
    user_principal_name: "{{ user_id }}"
    tenant: "{{ tenant_id }}"
    state: "absent"

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


class AzureRMADUser(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            object_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            account_enabled=dict(type='bool'),
            display_name=dict(type='str'),
            password_profile=dict(type='str', no_log=True),
            mail_nickname=dict(type='str'),
            immutable_id=dict(type='str'),
            usage_location=dict(type='str'),
            given_name=dict(type='str'),
            surname=dict(type='str'),
            user_type=dict(type='str'),
            mail=dict(type='str'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.user_principal_name = None
        self.state = None
        self.object_id = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.account_enabled = None
        self.display_name = None
        self.password_profile = None
        self.mail_nickname = None
        self.immutable_id = None
        self.usage_location = None
        self.given_name = None
        self.surname = None
        self.user_type = None
        self.mail = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]

        super(AzureRMADUser, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=False,
                                            mutually_exclusive=mutually_exclusive,
                                            required_together=required_together,
                                            required_one_of=required_one_of,
                                            is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        client = self.get_msgraph_client()
        changed = False
        response = None
        try:
            if self.object_id:
                response = client.get('/users/' + self.object_id).json()
            elif self.display_name is not None:
                response = client.get('/users/').json()['value']
                flag = False
                for item in response:
                    if item['displayName'] == self.display_name:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None
            elif self.user_principal_name is not None:
                response = client.get('/users/').json()['value']
                flag = False
                for item in response:
                    if item['userPrincipalName'] == self.user_principal_name:
                        flag = True
                        response = item
                        break
                if not flag:
                    response = None
        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        if response is not None and response.get('error'):
            response = None

        if response is not None:
            if self.state == 'present':
                changed = True
                response = self.update_resource(response['id'], self.body)
                self.log("The ad user account exist, don't recreate")
            else:
                response = self.delete_resource(response['id'])
                changed = True
        else:
            if self.state == 'present':
                response = self.create_resource(self.body)
                changed = True
            else:
                changed = False
                response = None
                self.log("The ad user account does not exist")

        self.results['state'] = self.user_to_dict(response)
        self.results['changed'] = changed

        return self.results

    def update_resource(self, obj_id, obj):
        res = None
        url = '/users/' + obj_id
        try:
            res = client.patch(url, data=json.dumps(obj), headers={'Content-Type': 'application/json'})

            if res.status_code == 204:
                self.log("Update ad user success full")
                return client.get(url).json()
            else:
                self.fail("Update ad user fail, Msg {0}".format(res.json().get('error')))
        except Exception as e:
            self.fail("Update ad user get exception, Exceptioin as: {0}".format(str(e)))

    def create_resource(self, obj):
        res = None
        try:
            res = client.post('/users/', data=json.dumps(obj), headers={'Content-Type': 'application/json'})

            if res.json().get('error') is not None:
                self.fail("Create ad user fail, Msg {0}".format(res.json().get('error')))
            else:
                return res.json()
        except Exception as e:
            self.fail("Error creating ad user, {0}".format(str(e)))

    def delete_resource(self, obj):
        try:
            client.delete('/users/' + obj)
        except Exception as e:
            self.fail("Error deleting ad users {0}".format(str(e)))

    def user_to_dict(self, object):
        if object:
            return dict(
                object_id=object['id'],
                display_name=object['displayName'],
                user_principal_name=object['userPrincipalName'],
                given_name=object['givenName'],
                surname=object['surname'],
                mail=object['mail'],
            )
        else:
            return []


def main():
    AzureRMADUser()


if __name__ == '__main__':
    main()
