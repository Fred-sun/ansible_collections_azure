#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionendpoint
version_added: "2.7.0"
short_description: Manage Data Collection Endpoint.
description:
    - Create, update or delete the Data Collection Endpoint.
options:
    resource_group:
        description:
            - Name of resource group.
        required: true
        type: str
    location:
        description:
            - Valid Azure location. Defaults to location of the resource group.
        type: str
    name:
        description:
            - The name of the Data Collection Endpoint.
        required: true
        type: str
    kind:
        description:
            - The kind of the resource.
        type: str
        choices:
            - Linux
            - Windows
    identity:
        description:
            - Identity for the Data Collection Endpoint.
        type: dict
        suboptions:
            type:
                description:
                    - Type of the managed identity.
                choices:
                    - SystemAssigned
                    - UserAssigned
                    - SystemAssigned, UserAssigned
                    - None
                default: None
                type: str
            user_assigned_identities:
                description:
                    - User Assigned Managed Identities and its options.
                type: str
    description:
        description:
            - Description of the data collection endpoint.
        type: str
    network_acls:
        description:
            - Network access control rules for the endpoints.
        type: dict
        suboptions:
            public_network_access:
                description:
                    - The configuration to set whether network access from public internet to the endpoints are allowed.
                type: str
                choices:
                    - Enabled
                    - Disabled
                    - SecuredByPerimeter
    state:
        description:
            - State of the Data Collection Endpoint. Use C(present) to create or update and C(absent) to delete.
        default: present
        type: str
        choices:
            - absent
            - present

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Create a Data Collection Endpoint
  azure_rm_monitordatacollectionendpoint:
    resource_group: myResourceGroup
    name: mydatacollectionendpoint
    tags:
      testing: testing
      delete: on-exit

- name: Delete a Data Collection Endpoint
  azure_rm_monitordatacollectionendpoint:
    resource_group: myResourceGroup
    name: mydatacollectionendpoint
    state: absent
'''
RETURN = '''
state:
    description:
        - Current state of the Data Collection Endpoint.
    returned: always
    type: complex
    contains:
        location:
            description:
                - The Geo-location where the resource lives.
            returned: always
            type: str
            sample: eastus
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: myDataCollectionEndpoint
        resource_group:
            description:
                - The resource group name.
            type: str
            returned: always
            sample: testRG
        id:
            descritpion:
                - Fully qualified ID of the resource.
            type: dict
            returned: always
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Insights/dataCollectionEndpoints/freddata01"
        description:
            descritpion:
                - Description of the data collection endpoint.
            type: dict
            returned: always
            sample: fred test
        identity:
            descritpion:
                -  Managed service identity of the resource.
            type: dict
            returned: always
            sample: {}
        kind:
            descritpion:
                - The kind of the resource.
            type: dict
            returned: always
            sample: Linux
        network_acls:
            descritpion:
                - Network access control rules for the endpoints.
            type: dict
            returned: always
            sample: {"public_network_access": "Enabled"}
        tags:
            description:
                - The resource tags.
            returned: always
            type: dict
            sample: { 'key1':'value1' }
        type:
            description:
                - The type of the resource.
            type: str
            returned: always
            sample: Microsoft.Insights/dataCollectionEndpoints
        provisioning_state:
            description:
                - The resource provisioning state.
            type: str
            returned: always
            sample: succeeded
'''

try:
    from azure.core.exceptions import HttpResponseError
    from azure.mgmt.monitor.v2022_06_01.models import ManagedServiceIdentity, UserAssignedIdentity
    import logging
    logging.basicConfig(filename='log.log', level=logging.INFO)
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMMonitorDataCollectionEndpoint(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            kind=dict(type='str', choices=['Linux', 'Windows']),
            description=dict(type='str'),
            network_acls=dict(
                type='dict',
                options=dict(
                    public_network_access=dict(type='str', choices=['Enabled', 'Disabled', 'SecuredByPerimeter'])
                )
            ),
            identity=dict(type='dict', options=self.managed_identity_single_spec)
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.kind = None
        self.description = None
        self.network_acls = None
        self.identity = None
        self.update_identity = None
        self._managed_identity = None
        self.body = {}

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMMonitorDataCollectionEndpoint, self).__init__(self.module_arg_spec,
                                                                   supports_tags=True,
                                                                   supports_check_mode=True)

    @property
    def managed_identity(self):
        if not self._managed_identity:
            self._managed_identity = {"identity": ManagedServiceIdentity,
                                      "user_assigned": UserAssignedIdentity
                                      }
        return self._managed_identity


    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])
            if key not in ['resource_group', 'name', 'state']:
                self.body[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if self.body.get('location') is None:
            # Set default location
            self.body['location'] = resource_group.location

        changed = False
        results = dict()

        old_response = self.get_by_name()

        curr_identity = old_response["identity"] if old_response else None

        if self.body['identity']:
            self.update_identity, identity_result = self.update_single_managed_identity(curr_identity=curr_identity,
                                                                                        new_identity=self.body['identity'],
                                                                                        patch_support=True)
            logging.info('pppp')
            logging.info(self.update_identity)
            logging.info(identity_result)
            logging.info(self.body['identity'])
            logging.info('eeee')
            self.body['identity'] = identity_result.as_dict()

        if old_response is not None:
            if self.state == 'present':
                update_tags, self.body['tags'] = self.update_tags(old_response['tags'])
                if update_tags or self.update_identity:
                    changed = True
                    if not self.check_mode:
                        results = self.update(self.body)
                else:
                    results = old_response
            else:
                changed = True
                if not self.check_mode:
                    results = self.delete()
        else:
            if self.state == 'present':
                changed = True
                if not self.check_mode:
                    results = self.create(self.body)
            else:
                changed = False
                self.log("The Data Collection Endpoint is not exists")

        self.results['changed'] = changed
        self.results['state'] = results

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.get(self.resource_group, self.name)

        except HttpResponseError as exec:
            self.log("Failed to get Data Collection Endpoint, Exception as {0}".format(exec))

        return self.to_dict(response)

    def create(self, body):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.create(self.resource_group, self.name, body)
        except HttpResponseError as exc:
            self.fail("Error creating Data Collection Endpoint {0} - {1}".format(self.name, str(exc)))

        return self.to_dict(response)

    def update(self, body):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.update(self.resource_group, self.name, body)
        except HttpResponseError as exc:
            self.fail("Error creating Data Collection Endpoint {0} - {1}".format(self.name, str(exc)))

        return self.to_dict(response)

    def delete(self):
        try:
            self.monitor_data_collection_client.data_collection_endpoints.delete(self.resource_group, self.name)
        except Exception as exc:
            self.fail("Error deleting Data Collection Endpoint {0} - {1}".format(self.name, str(exc)))

    def to_dict(self, body):
        if body:
            results = dict(
                resource_group=self.resource_group,
                name=self.name,
                location=body.location,
                id=body.id,
                tags=body.tags,
                description=body.description,
                kind=body.kind,
                provisioning_state=body.provisioning_state,
                description=body.description,
                identity=body.identity.as_dict() if body.identity else None,
                network_acls=dict()
            )
            if body.network_acls is not None:
                results['network_acls']['public_network_access'] = body.network_acls.public_network_access
            return results


def main():
    AzureRMMonitorDataCollectionEndpoint()


if __name__ == '__main__':
    main()
