#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_adserviceprincipal

version_added: "0.2.0"

short_description: Manage Azure Active Directory service principal

description:
        - Manage Azure Active Directory service principal.

options:
    app_id:
        description:
            - The application ID.
        type: str
        required: True
    tenant:
        description:
            - The tenant ID.
        type: str
    app_role_assignment_required:
        description:
            - Whether the Role of the Service Principal is set.
        type: bool
    state:
        description:
            - Assert the state of Active Dirctory service principal.
            - Use C(present) to create or update a Password and use C(absent) to delete.
        default: present
        choices:
            - absent
            - present
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: create ad sp
    azure_rm_adserviceprincipal:
      app_id: "{{ app_id }}"
      state: present
      tenant: "{{ tenant_id }}"
'''

RETURN = '''
app_display_name:
    description:
        - Object's display name or its prefix.
    type: str
    returned: always
    sample: fredAKSCluster
app_id:
    description:
        - The application ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
app_role_assignment_required:
    description:
        - Whether the Role of the Service Principal is set.
    returned: always
    type: bool
    sample: false
object_id:
    description:
        - Object ID of the associated service principal.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
import json


class AzureRMADServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str', required=True),
            tenant=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            app_role_assignment_required=dict(type='bool')
        )

        self.state = None
        self.tenant = None
        self.app_id = None
        self.app_role_assignment_required = None
        self.object_id = None
        self.results = dict(changed=False)
        self.body = dict()

        super(AzureRMADServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=False,
                                                        supports_tags=False,
                                                        is_ad_resource=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

            if key == 'app_id':
                self.body['appId'] = kwargs[key]
            elif key == 'app_role_assignment_required':
                self.body['appRoleAssignmentRequired'] = kwargs[key]

        client = self.get_msgraph_client()
        response = self.get_resource(client)

        if response:
            if self.state == 'present':
                if self.check_update(response):
                    self.update_resource(client, self.body)
                else:
                    self.results['service_principals'] = self.get_resource(client)
            elif self.state == 'absent':
                self.delete_resource(client, response)
        else:
            if self.state == 'present':
                self.create_resource(client, self.body)
            elif self.state == 'absent':
                self.log("try to delete non exist resource")

        return self.results

    def create_resource(self, client, body):
        response = None
        try:
            response = client.post('/serviceprincipals/', data=json.dumps(body), headers={'Content-Type': 'application/json'})
            self.results['changed'] = True
            self.results['service_principals'] = self.get_resource(client)
        except Exception as ge:
            self.fail("Error creating service principle, app id {0} - {1}".format(self.app_id, str(ge)))

    def update_resource(self, client, body):
        response = None
        try:
            response = client.patch('/serviceprincipals/', data=json.dumps(body), headers={'Content-Type': 'application/json'})

            self.results['changed'] = True
            self.results['service_principals'] = self.get_resource(client)
        except Exception as ge:
            self.fail("Error updating the service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def delete_resource(self, client, response):
        try:
            client.delete('/serviceprincipals/' + response.get('object_id'))
            self.results['changed'] = True
        except Exception as ge:
            self.fail("Error deleting service principal app_id {0} - {1}".format(self.app_id, str(ge)))

    def get_resource(self, client):
        try:
            url = "/serviceprincipals(appID='{0}')".format(self.app_id)
            result = client.get(url).json()

            if result.get('error') is not None:
                return None
            else:
                return self.to_dict(result)
        except Exception as ge:
            self.log("Did not find the graph instance instance {0} - {1}".format(self.app_id, str(ge)))

    def check_update(self, response):
        app_assignment_changed = self.app_role_assignment_required is not None and \
            self.app_role_assignment_required != response.get('app_role_assignment_required', None)

        return app_assignment_changed

    def to_dict(self, object):
        return dict(
            app_id=object['appId'],
            object_id=object['id'],
            app_display_name=object['appDisplayName'],
            app_role_assignment_required=object['appRoleAssignmentRequired']
        )


def main():
    AzureRMADServicePrincipal()


if __name__ == '__main__':
    main()
