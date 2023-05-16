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
        type: str
    account_enabled:
        description:
            - A boolean determing whether or not the user account is enabled.
            - Used when either creating or updating a user account.
        type: bool
        default: True
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
    user_principal_name:
        description:
            - The principal name of the user.
            - Creates, updates, or deletes the user who has this principal name.
        type: str
    attribute_name:
        description:
            - The name of an attribute that you want to match to attribute_value.
            - If attribute_name is not a collection type it will update or delete the user where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will update or delete the user where attribute_value is in attribute_name.
            - Mutually exclusive with I(object_id), I(user_principal_name), and I(odata_filter).
            - Required together with I(attribute_value).
        type: str
    attribute_value:
        description:
            - The value to match attribute_name to.
            - If attribute_name is not a collection type it will update or delete the user where attribute_name is equal to attribute_value.
            - If attribute_name is a collection type it will update or delete the user where attribute_value is in attribute_name.
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
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

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
    sample: ansibletest
user_principal_name:
    description:
        - The principal name of the user.
    returned: always
    type: str
    sample: John Smith
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
surname:
    description:
        - The user's surname (family name or last name).
    type: str
    returned: always
    sample: Smith
given_name:
    description:
        - The given name for the user.
    returned: always
    type: str
    sample: John
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
import json


class AzureRMADUser(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            user_principal_name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            object_id=dict(type='str'),
            account_enabled=dict(type='bool', default=True),
            display_name=dict(type='str'),
            password_profile=dict(type='str', no_log=True),
            mail_nickname=dict(type='str'),
            mail=dict(type='str'),
            tenant=dict(type='str'),
            immutable_id=dict(type='str'),
            attribute_name=dict(type='str'),
            attribute_value=dict(type='str'),
            odata_filter=dict(type='str'),
            usage_location=dict(type='str'),
            given_name=dict(type='str'),
            surname=dict(type='str'),
            user_type=dict(type='str'),
        )

        self.user_principal_name = None
        self.state = None
        self.object_id = None
        self.account_enabled = None
        self.display_name = None
        self.password_profile = None
        self.mail_nickname = None
        self.mail = None
        self.immutable_id = None
        self.usage_location = None
        self.given_name = None
        self.surname = None
        self.user_type = None
        self.attribute_name = None
        self.attribute_value = None
        self.odata_filter = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(changed=False)
        self.body = dict()

        mutually_exclusive = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]
        required_together = [['attribute_name', 'attribute_value']]
        required_one_of = [['odata_filter', 'attribute_name', 'object_id', 'user_principal_name']]

        super(AzureRMADUser, self).__init__(derived_arg_spec=self.module_arg_spec,
                                            supports_check_mode=False,
                                            supports_tags=False,
                                            mutually_exclusive=mutually_exclusive,
                                            required_together=required_together,
                                            required_one_of=required_one_of,
                                            )

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

            if key == 'display_name' and kwargs[key] is not None:
                self.body['displayName'] = kwargs[key]
            elif key == 'password_profile' and kwargs[key] is not None:
                self.body['passwordProfile'] = dict(Password=kwargs[key])
            elif key == 'account_enabled' and kwargs[key] is not None:
                self.body['accountEnabled'] = kwargs[key]
            elif key == 'mail_nickname' and kwargs[key] is not None:
                self.body['mailNickname'] = kwargs[key]
            elif key == 'mail' and kwargs[key] is not None:
                self.body['mail'] = kwargs[key]
            elif key == 'user_principal_name' and kwargs[key] is not None:
                self.body['userPrincipalName'] = kwargs[key]
            elif key == 'immutable_id' and kwargs[key] is not None:
                self.body['onPremisesImmutableId'] = kwargs[key]
            elif key == 'usage_location' and kwargs[key] is not None:
                self.body['usageLocation'] = kwargs[key]
            elif key == 'user_type' and kwargs[key] is not None:
                self.body['userType'] = kwargs[key]
            elif key == 'given_name' and kwargs[key] is not None:
                self.body['givenName'] = kwargs[key]
            elif key == 'surname' and kwargs[key] is not None:
                self.body['surname'] = kwargs[key]

        client = self.get_msgraph_client()
        changed = False
        response = self.get_exisiting_user(client)

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
            elif self.odata_filter is not None:
                url = '/users' + self.odata_filter
                response = client.get(url).json()
            elif self.attribute_name is not None and self.attribute_value is not None:
                res = client.get('/users/').json()['value']
                for item in res:
                    if item[self.attribute_name] == self.attribute_value:
                        response = item

        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        if response is not None and response.get('error'):
            response = None

        if response is not None:
            if self.state == 'present':
                if (self.body.get('displayName') is not None and response['displayName'] != self.body.get('displayName')) |\
                    (self.body.get('givenName') is not None and response['givenName'] != self.body.get('givenName')) |\
                    (self.body.get('mail') is not None and response['mail'] != self.body.get('mail')) |\
                    (self.body.get('surname') is not None and response['surname'] != self.body.get('surname')) |\
                    (self.body.get('userPrincipalName') is not None and response['userPrincipalName'] != self.body.get('userPrincipalName')):

                    changed = True
                    response = self.update_resource(response['id'], self.body)
                    self.log("The ad user account exist, It will be update")
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

    def get_exisiting_user(self, client):
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
            elif self.odata_filter is not None:
                url = '/users' + self.odata_filter
                response = client.get(url).json()
                if len(response) > 1:
                    response = response[0]
            elif self.attribute_name is not None and self.attribute_value is not None:
                res = client.get('/users/').json()['value']
                for item in res:
                    if item[self.attribute_name] == self.attribute_value:
                        response = item

        except Exception as e:
            self.fail("failed to get ad user info {0}".format(str(e)))

        if response is not None and response.get('error'):
            response = None

        return response

    def update_resource(self, obj_id, obj):
        client = self.get_msgraph_client()
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
        client = self.get_msgraph_client()
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
        client = self.get_msgraph_client()
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
                user_type=object.get('userType'),
                mail_nickname=object.get('mailNickname'),
                account_enabled=object.get('accountEnabled')
            )
        else:
            return []


def main():
    AzureRMADUser()


if __name__ == '__main__':
    main()
