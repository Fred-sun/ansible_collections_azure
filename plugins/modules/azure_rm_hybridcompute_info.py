#!/usr/bin/python
#
# Copyright (c) 2018 Fred-sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_hybridcompute_info
version_added: "1.14.0"
short_description: Get hybrid compute facts
description:
    - Get facts for a specific hybrid compute.

options:
    name:
        description:
            - The hybrid compute name.
        type: str
    resource_group:
        description:
            - The name of the resource group.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - Fred-sun (@Fred-sun)
    - xuzhang3 (@xuzhang3)
'''

EXAMPLES = '''
    - name: Get hybrid compute machine by name
      azure_rm_hybridcompute_info:
        resource_group: "{{ resource_group }}"
        name: "{{ name }}"

    - name: Get hybrid compute by resource group
      azure_rm_hybridcompute_info:
        resource_group: "{{ resource_group }}"

    - name: Get all bybrid compute by subscription ID  filter by tags
      azure_rm_hybridcompute_info:
        tags:
          - key1
'''

RETURN = '''
hybridcompute:
    description:
        - Current state fo the hybrid compute.
    returned: always
    type: complex
    contains:
        id:
            description:
                - The hybrid compute ID.
            type: str
            returned: always
            sample: "/subscriptions/xxx-xxx-xxx/resourceGroups/fredRG/providers/Microsoft.HybridCompute/machines/testVM"
        location:
            description:
                - The resource location.
            type: str
            returned: always
            sample: eastus
        name:
            description:
                - The resource name.
            type: str
            returned: always
            sample: testVM
        type:
            description:
                - The resource type.
            type: str
            returned: always
            sample: "Microsoft.HybridCompute/machines"
        tags:
            description:
                - List the hybrid compute tags.
            type: str
            returned: always
            sample: {'key1':'value1'}
        identity:
            description:
                -  Managed service identity of the hybrid compute.
            type: str
            returned: always
            contains:
                principal_id:
                    description:
                        - The principal id of the identity.
                    type: str
                    returned: always
                    sample: "***********"
                tenant_id:
                    description:
                        - The client tenant id of the identity.
                    type: str
                    returned: always
                    sample: "***********"
        properties:
            description:
                - "Describes the properties of a hybrid machine.
            type: str
            returned: always
            contains:
                status:
                    description:
                        -  The status of the hybrid machine agent. Possible values include: "Connected",
                    type: str
                    returned: always
                    sample: Connected
                provisioning_state:
                    description:
                        - The provisioning state, which only appears in the response.
                    type: str
                    returned: always
                    sample: Succeeded
                ad_fqdn:
                    description:
                        - Specifies the AD fully qualified display name.
                    type: str
                    returned: always
                    sample: unknow
                display_name:
                    description:
                        - Specifies the hybrid machine display name.
                    type: str
                    returned: always
                    sample: testVM
                domain_name:
                    description:
                        - Specifies the Windows domain name.
                    type: str
                    returned: always
                    sample: unknow
                os_name:
                    description:
                        - The Operating System running on the hybrid machine.
                    type: str
                    returned: always
                    sample:  "linux"
                machine_fqdn:
                    description:
                        - Specifies the hybrid machine FQDN.
                    type: str
                    returned: always
                    sample: testVM
                os_sku:
                    description:
                        - Specifies the Operating System product SKU.
                    type: str
                    returned: always
                    sample: Ubuntu 20.04.4 LTS
                os_version:
                    description:
                        - The version of Operating System running on the hybrid machine.
                    type: str
                    returned: always
                    sample: 5.15.0-1017-azure
                parent_cluster_resource_id:
                    description:
                        - The resource id of the parent cluster (Azure HCI) this machine is assigned to.
                    type: str
                    returned: always
                    sample: null
                vm_id:
                    description:
                        - Specifies the hybrid machine unique ID.
                    type: str
                    returned: always
                    sample: "1f26c460-0f7b-4388-a2ac-2d8c02554dec"
                vm_uuid:
                    description:
                        - Specifies the Arc Machine's unique SMBIOS ID.
                    type: str
                    returned: always
                    sample: 0120e3d4-3c10-4d1d-821f-8e00b05e4b99
                private_link_scope_resource_id:
                    description:
                        - The resource id of the private link scope this machine.
                    type: str
                    returned: always
                    sample: null
                detected_properties:
                    description:
                        - Detected properties from the machine.
                    type: dict
                    returned: always
                    sample: {
                        "Azure-resourceId": "/subscriptions/xxx-xxx/ResourceGroups/fredRG/providers/Microsoft.Compute/virtualMachines/testVM",
                        "cloudprovider": "Azure",
                        "logicalCoreCount": "2",
                        "manufacturer": "Microsoft Corporation",
                        "model": "Virtual Machine",
                        "mssqldiscovered": "false"
                    } 
'''

try:
    from azure.core.exceptions import ResourceNotFoundError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

AZURE_OBJECT_CLASS = 'HybridComputeInfo'


class AzureRMHybridComputeInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.results = dict(
            changed=False,
        )

        self.name = None
        self.resource_group = None
        self.if_none_match = None

        super(AzureRMHybridComputeInfo, self).__init__(self.module_arg_spec,
                                                     supports_check_mode=True,
                                                     supports_tags=False,
                                                     facts_module=True)

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        result = []

        if self.name and self.resource_group:
            result = self.get_item()
        elif self.resource_group:
            result = self.list_by_resourcegroup()
        else:
            result = self.list_all()

        self.results['hybridcompute'] = self.format(result)

        return self.results

    def format(self, raw):
        if not raw:
            return None
        results = []
        for item in raw:
            if self.has_tags(item.tags, self.tags):
                results.append(self.pip_to_dict(item))
        return results

    def pip_to_dict(self, pip):
        result = dict(
            id=pip.id,
            name=pip.name,
            type=pip.type,
            location=pip.location,
            tags=pip.tags,
            identity=dict(),
            properties=dict()
        )
        if pip.identity:
            result['identity']['principal_id'] = pip.identity.principal_id
            result['identity']['tenant_id'] = pip.identity.tenant_id
        if pip.properties:
            result['properties']['status'] = pip.properties.status
            result['properties']['provisioning_state'] = pip.properties.provisioning_state
            result['properties']['display_name']=pip.properties.display_name
            result['properties']['vm_id']=pip.properties.vm_id
            result['properties']['machine_fqdn']=pip.properties.machine_fqdn
            result['properties']['os_name']=pip.properties.os_name
            result['properties']['os_version']=pip.properties.os_version
            result['properties']['vm_uuid']=pip.properties.vm_uuid
            result['properties']['os_sku']=pip.properties.os_sku
            result['properties']['domain_name']=pip.properties.domain_name
            result['properties']['ad_fqdn']=pip.properties.ad_fqdn
            result['properties']['private_link_scope_resource_id']=pip.properties.private_link_scope_resource_id
            result['properties']['parent_cluster_resource_id']=pip.properties.parent_cluster_resource_id
            result['properties']['detected_properties']=pip.properties.detected_properties
        return result

    def get_item(self):
        response = None
        self.log('"Retrieves information about the model view or the instance view of a hybrid machine.')
        try:
            response = self.hybrid_client.machines.get(self.resource_group, self.name, self.if_none_match)
        except ResourceNotFoundError:
            pass
        return [response] if response else []

    def list_by_resourcegroup(self):
        self.log("Lists all the hybrid machines in the specified resource group.")
        try:
            response = self.hybrid_client.machines.list_by_resource_group(self.resource_group)
        except Exception:
            pass
        return response if response else []

    def list_all(self):
        self.log("Lists all the hybrid machines in the specified subscription.")
        response = None
        try:
            response = self.hybrid_client.machines.list_by_subscription()
        except Exception as ec:
            self.fail(ec)
            pass
        return response if response else []


def main():
    AzureRMHybridComputeInfo()


if __name__ == '__main__':
    main()
