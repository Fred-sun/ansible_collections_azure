#!/usr/bin/python
#
# Copyright (c) 2024 xuzhang3 (@xuzhang3), Fred-sun (@Fred-sun)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_monitordatacollectionrule
version_added: "2.7.0"
short_description: Manage Data Collection rule.
description:
    - Create, update or delete the Data Collection rule.
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
            - The name of the Data Collection rule.
        required: true
        type: str
    kind:
        description:
            - The kind of the resource.
        type: str
        choices:
            - Linux
            - Windows
    description:
        description:
            - Description of the data collection rule.
        type: str
    network_acls:
        description:
            - Network access control rules for the rules.
        type: dict
        suboptions:
            public_network_access:
                description:
                    - The configuration to set whether network access from public internet to the rules are allowed.
                type: str
                choices:
                    - Enabled
                    - Disabled
                    - SecuredByPerimeter
    state:
        description:
            - State of the Data Collection rule. Use C(present) to create or update and C(absent) to delete.
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
- name: Create a Data Collection rule
  azure_rm_monitordatacollectionrule:
    resource_group: myResourceGroup
    name: mydatacollectionrule
    kind: Windows
    description: fredtest01
    network_acls:
      public_network_access: Disabled
    tags:
      testing: testing
      delete: on-exit

- name: Delete a Data Collection rule
  azure_rm_monitordatacollectionrule:
    resource_group: myResourceGroup
    name: mydatacollectionrule
    state: absent
'''
RETURN = '''
state:
    description:
        - Current state of the Data Collection rule.
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
            sample: myDataCollectionrule
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
            sample: "/subscriptions/xxx-xxx/resourceGroups/testRG/providers/Microsoft.Insights/dataCollectionrules/freddata01"
        description:
            descritpion:
                - Description of the data collection rule.
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
                - Network access control rules for the rules.
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
            sample: Microsoft.Insights/dataCollectionrules
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


columns_spec = dict(
    name=dict(type='str'),
    type=dict(type='str', choices=["string", "int", "long", "real", "boolean", "datetime", "dynamic"])
)


class AzureRMMonitorDataCollectionrule(AzureRMModuleBaseExt):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            location=dict(type='str'),
            kind=dict(type='str', choices=['Linux', 'Windows']),
            description=dict(type='str'),
            data_collection_endpoint_id=dict(type='str'),
            stream_declarations=dict(
                type='dict',
                options=dict(
                    columns=dict(type='list', elements='dict', options=columns_spec)
                )
            ),
            data_sources=dict(
                type='dict',
                options=dict(
                    performance_counters=dict(
                    windows_event_logs=dict(
                    syslog=dict(
                    extensions=dict(
                    iis_logs=dict(
                        type='dict',
                        options=dict(
                            streams=dict(type='list', elements='str'),
                            name=dict(type='str'),
                            log_directories=dict(type='list', elements='str')
                        )
                    ),
                    windows_firewall_logs=dict(
                        type='dict',
                        options=dict(
                            name=dict(type='str'),
                            streams=dict(type='list', elements='str')
                        )
                    ),
                    prometheus_forwarder=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            streams=dict(type='list', elements='str', choices=['Microsoft-PrometheusMetrics']),
                            label_include_filter=dict(type='dict'),
                            name=dict(type='str')
                        )
                    )
                    platform_telemetry=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            streams=dict(type='list', elements='str'),
                            name=dict(type='str')
                        )
                    ),
                    data_imports=dict(
                        type='dict',
                        options=dict(
                            event_hub=dict(
                                type='dict',
                                options=dict(
                                    name=dict(type='str'),
                                    consumer_group=dict(type='str'),
                                    stream=dict(type='str')
                                )
                            )
                        )
                    )
                )
            ),
            destinations=dict(type='dict', options=destinations_spec),
            data_flows=dict(type='list', elements='dict', options=data_flows_spec),
        )

        self.resource_group = None
        self.name = None
        self.state = None
        self.location = None
        self.kind = None
        self.description = None
        self.network_acls = None
        self.body = {}

        self.results = dict(
            changed=False,
            state=dict()
        )

        super(AzureRMMonitorDataCollectionrule, self).__init__(self.module_arg_spec,
                                                                   supports_tags=True,
                                                                   supports_check_mode=True)

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

        if old_response is not None:
            if self.state == 'present':
                update_tags, self.body['tags'] = self.update_tags(old_response['tags'])
                if update_tags:
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
                self.log("The Data Collection rule is not exists")

        self.results['changed'] = changed
        self.results['state'] = results

        return self.results

    def get_by_name(self):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_rules.get(self.resource_group, self.name)

        except HttpResponseError as exec:
            self.log("Failed to get Data Collection rule, Exception as {0}".format(exec))

        return self.to_dict(response)

    def create(self, body):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_rules.create(self.resource_group, self.name, body)
        except HttpResponseError as exc:
            self.fail("Error creating Data Collection rule {0} - {1}".format(self.name, str(exc)))

        return self.to_dict(response)

    def update(self, body):
        response = None
        try:
            response = self.monitor_data_collection_client.data_collection_rules.update(self.resource_group, self.name, body)
        except HttpResponseError as exc:
            self.fail("Error creating Data Collection rule {0} - {1}".format(self.name, str(exc)))

        return self.to_dict(response)

    def delete(self):
        try:
            self.monitor_data_collection_client.data_collection_rules.delete(self.resource_group, self.name)
        except Exception as exc:
            self.fail("Error deleting Data Collection rule {0} - {1}".format(self.name, str(exc)))

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
                identity=body.identity.as_dict() if body.identity else None,
                network_acls=dict()
            )
            if body.network_acls is not None:
                results['network_acls']['public_network_access'] = body.network_acls.public_network_access
            return results


def main():
    AzureRMMonitorDataCollectionrule()


if __name__ == '__main__':
    main()
