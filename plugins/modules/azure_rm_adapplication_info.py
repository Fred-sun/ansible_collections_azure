#!/usr/bin/python
#
# Copyright (c) 2020 Guopeng Lin, <linguopeng1998@google.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: azure_rm_adapplication_info

version_added: "1.6.0"

short_description: Get Azure Active Directory application info

description:
    - Get Azure Active Directory application info.

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
            - It's application's object ID.
        type: str
    identifier_uri:
        description:
            - It's identifier_uri's object ID.
        type: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    haiyuan_zhang (@haiyuazhang)
    Fred-sun (@Fred-sun)
    guopeng_lin (@guopenglin)
'''

EXAMPLES = '''
  - name: get ad app info by App ID
    azure_rm_adapplication_info:
      app_id: "{{ app_id }}"
      tenant: "{{ tenant_id }}"

  - name: get ad app info ---- by object ID
    azure_rm_adapplication_info:
      object_id: "{{ object_id }}"
      tenant: "{{ tenant_id }}"

  - name: get ad app info ---- by identifier uri
    azure_rm_adapplication_info:
      identifier_uri: "{{ identifier_uri }}"
      tenant: "{{ tenant_id }}"

'''

RETURN = '''
applications:
    description:
        - The info of the ad application.
    type: complex
    returned: aways
    contains:
        app_display_name:
            description:
                - Object's display name or its prefix.
            type: str
            returned: always
            sample: app
        app_id:
            description:
                - The application ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        identifier_uris:
            description:
                - The identifiers_uri list of app.
            type: list
            returned: always
            sample: ["http://ansible-atodorov"]
        object_id:
            description:
                - It's application's object ID.
            returned: always
            type: str
            sample: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBase


class AzureRMADApplicationInfo(AzureRMModuleBase):

    def __init__(self):
        self.module_arg_spec = dict(
            app_id=dict(
                type='str'
            ),
            object_id=dict(
                type='str'
            ),
            identifier_uri=dict(
                type='str'
            ),
            tenant=dict(
                type='str',
            )
        )
        self.tenant = None
        self.app_id = None
        self.object_id = None
        self.identifier_uri = None
        self.results = dict(changed=False)
        super(AzureRMADApplicationInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                       supports_check_mode=True,
                                                       supports_tags=False)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        applications = []
        try:
            client = self.get_msgraph_client()
            if self.object_id:
                applications = [client.get('/applications/' + self.object_id).json()]
            else:
                apps = [client.get('/applications/').json()]
                if self.app_id is not None:
                    for item in apps:
                        if item['appId'] == self.app_id:
                            applications.append(item)
                if self.identifier_uri is not None:
                    for item in apps:
                        if item.get('identifierUris') == self.identifier_uri:
                            applications.append(item)
            self.results['applications'] = [self.to_dict(app) for app in applications]
        except Exception as ge:
            self.fail("failed to get application info {0}".format(str(ge)))

        return self.results

    def to_dict(self, object):
        return dict(
            app_id=object['appId'],
            object_id=object['id'],
            app_display_name=object['displayName'],
            identifier_uris=object['dentifierUris']
        )


def main():
    AzureRMADApplicationInfo()


if __name__ == '__main__':
    main()
