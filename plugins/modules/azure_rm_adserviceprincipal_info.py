#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_adserviceprincipal_info

version_added: "0.2.0"

short_description: Get Azure Active Directory service principal info

description:
    - Get Azure Active Directory service principal info.

options:
    app_id:
        description:
            - The application ID.
        type: str
    tenant:
        description:
            - The tenant ID.
        type: str
    object_id:
        description:
            - It's service principal's object ID.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
'''

EXAMPLES = '''
  - name: get ad sp info
    azure_rm_adserviceprincipal_info:
      app_id: "{{ app_id }}"
      tenant: "{{ tenant_id }}"

'''

RETURN = '''
app_display_name:
    description:
        - Object's display name or its prefix.
    type: str
    returned: always
    sample: sp
app_id:
    description:
        - The application ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
app_role_assignment_required:
    description:
        - Whether the Role of the Service Principal is set.
    type: bool
    returned: always
    sample: false
object_id:
    description:
        - It's service principal's object ID.
    returned: always
    type: str
    sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase
import json


class AzureRMADServicePrincipalInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            object_id=dict(type='str'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.app_id = None
        self.object_id = None
        self.results = dict(changed=False)
        required_one_of = [['app_id', 'object_id']]

        super(AzureRMADServicePrincipalInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False,
                                                            required_one_of=required_one_of)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        service_principals = []

        try:
            client = self.get_msgraph_client()
            if self.object_id is not None:
                service_principals = client.get('/serviceprincipals/' + self.object_id).json()
            else:
                url = "/serviceprincipals(appID='{0}')".format(self.app_id)
                service_principals = client.get(url).json()

            if service_principals.get('error'):
                self.results['service_principals'] = []
            else:
                self.results['service_principals'] = self.to_dict(service_principals)
        except Exception as ge:
            self.fail("failed to get service principal info {0}".format(str(ge)))

        return self.results

    def to_dict(self, object):
        return dict(
            app_id=object['appId'],
            object_id=object['id'],
            app_display_name=object['appDisplayName'],
            app_role_assignment_required=object['appRoleAssignmentRequired']
        )


def main():
    AzureRMADServicePrincipalInfo()


if __name__ == '__main__':
    main()
