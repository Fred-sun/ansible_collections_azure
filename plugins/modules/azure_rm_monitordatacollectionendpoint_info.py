#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionendpoint_info
version_added: "2.7.0"
short_description: Get the Data Collection Endpoint facts
description:
    - Get or list the Data Collection Endpoint.
options:
    resource_group:
        description:
            - Name of resource group.
        type: str
    name:
        description:
            - The name of the Data Collection Endpoint.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - xuzhang3 (@xuzhang3)
    - Fred-sun (@Fred-sun)

'''

EXAMPLES = '''
- name: Get the Data Collection Endpoint facts
  azure_rm_monitordatacollectionendpoint_info:
    resource_group: myResourceGroup
    name: mydatacollectionendpoint

- name: List all Data Collection Endpoint and filter by tags
  azure_rm_monitordatacollectionendpoint_info:
    tags:
      - key1
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
        configuration_access:
            descritpion:
                - The endpoint used by clients to access their configuration.
            type: dict
            returned: always
            sample: {"endpoint": "https://datacollectionfredvmss-uk2o.eastus-1.handler.control.monitor.azure.com"}
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
        immutable_id:
            description:
                - The immutable ID of this data collection endpoint resource.
            type: str
            returned: always
            sample: dce-bf81af171c3d4c9482cb9784ea851d63
        kind:
            descritpion:
                - The kind of the resource.
            type: dict
            returned: always
            sample: Linux 
        logs_ingestion:
            descritpion:
                - The endpoint used by clients to ingest logs.
            type: dict
            returned: always
            sample: {"endpoint": "https://datacollectionfredvmss-uk2o.eastus-1.ingest.monitor.azure.com"}
        network_acls:
            descritpion:
                - Network access control rules for the endpoints.
            type: dict
            returned: always
            sample: {"public_network_access": "Enabled"}
        metrics_ingestion:
            descritpion:
                - The endpoint used by clients to ingest metrics.
            type: dict
            returned: always
            sample: {"endpoint": "https://datacollectionfredvmss-uk2o.eastus-1.metrics.ingest.monitor.azure.com"}
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                    "created_at": "2024-08-05T13:43:56.267959Z",
                    "created_by": "235b0fed-809d-4a99-b03b-2e088d3d5b33",
                    "created_by_type": "Application",
                    "last_modified_at": "2024-08-05T13:44:50.352826Z",
                    "last_modified_by": "235b0fed-809d-4a99-b03b-2e088d3d5b33",
                    "last_modified_by_type": "Application"}
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
    from azure.mgmt.core.tools import parse_resource_id
except ImportError:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt


class AzureRMMonitorDataCollectionEndpointInfo(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str'),
            name=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.resource_group = None
        self.name = None
        self.tags = None

        self.results = dict(
            changed=False,
            state=list()
        )

        super(AzureRMMonitorDataCollectionEndpointInfo, self).__init__(self.module_arg_spec,
                                                                       supports_tags=False,
                                                                       facts_module=True,
                                                                       supports_check_mode=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        if self.name is not None and self.resource_group is not None:
            response = self.get_by_name()
        elif self.resource_group is not None:
            response = self.list_by_resourcegroup()
        else:
            response = self.list_all()
        self.results['state'] = [self.to_dict(item) for item in response if response is not None]

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.get(self.resource_group, self.name)

        except HttpResponseError as exec:
            self.log("Failed to get Data Collection Endpoint, Exception as {0}".format(exec))

        return [response]

    def list_by_resourcegroup(self):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.list_by_resource_group(self.resource_group)

        except HttpResponseError as exec:
            self.log("Failed to list the Data Collection Endpoint, Exception as {0}".format(exec))

        return response

    def list_all(self):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_endpoints.list_by_subscription()

        except HttpResponseError as exec:
            self.log("Failed to list the Data Collection Endpoint, Exception as {0}".format(exec))

        return response

    def to_dict(self, body):
        results = None
        if body is not None and self.has_tags(body.tags, self.tags):
            results = dict(
                resource_group=parse_resource_id(body.id).get('resource_group'),
                name=body.name,
                location=body.location,
                tags=body.tags,
                kind=body.kind,
                provisioning_state=body.provisioning_state,
                type=body.type,
                id=body.id,
                description=body.description,
                immutable_id=body.immutable_id,
                network_acls=dict(),
                identity=body.identity.as_dict() if body.identity else None,
                system_data=body.system_data.as_dict() if body.system_data else None,
                configuration_access=body.configuration_access.as_dict() if body.configuration_access else None,
                logs_ingestion=body.logs_ingestion.as_dict() if body.logs_ingestion else None,
                metrics_ingestion=body.metrics_ingestion.as_dict() if body.metrics_ingestion else None,
            )
            if body.network_acls is not None:
                results['network_acls']['public_network_access'] = body.network_acls.public_network_access

        return results


def main():
    AzureRMMonitorDataCollectionEndpointInfo()


if __name__ == '__main__':
    main()
