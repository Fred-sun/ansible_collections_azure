#!/usr/bin/python
#
# Copyright (c) 2017 Fred Sun, <xiuxi.sun@qq.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_hybridcompute
version_added: '1.14.0'
short_description: Mange hybrid compute
description:
    - Create, update or delete hybrid compute.

options:
    resource_group:
        description:
            - The name of the resource group.
        type: str
        required: True
    name:
        description:
            - The name of the hybrid compute.
        type: str
        required: True
    state:
        description:
            - State of the hybrid compute.
            - Use C(present) to create or update hybrid compute and use C(absent) to delete.
        type: str
        default: present
        choices:
            - present
            - absent

extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - Fred Sun (@Fred-sun)
    - xuzhang3 (@xuzhang3)

'''

EXAMPLES = '''
- name: Delete hybrid compute
  azure_rm_hybridcompute:
    resource_group: "{{ resource_group }}"
    name: "{{ hybrid-name }}"
    state: absent
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

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.core.exceptions import ResourceNotFoundError
except ImportError:
    pass


class AzureRMHybridCompute(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                default='present'
            )
        )
        # store the results of the module operation
        self.results = dict()
        self.resource_group = None
        self.name = None

        super(AzureRMHybridCompute, self).__init__(self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec) + ['tags']:
            setattr(self, key, kwargs[key])

        hybrid_compute = self.get()
        changed = False

        if self.state == 'present':
            pass
        else:
            if not self.check_mode and hybrid_compute is not None:
                changed = True
                hybrid_compute = self.delete_hybrid_compute()

        self.results['changed'] = changed
        self.results['hybridcompute'] = hybrid_compute
        return self.results

    def get(self):
        try:
            response = self.hybrid_client.machines.get(self.resource_group, self.name)
            return self.to_dict(response)
        except ResourceNotFoundError:
            pass

    def delete_hybrid_compute(self):
        try:
            return self.hybrid_client.machines.delete(self.resource_group, self.name)
        except Exception as exc:
            self.fail('Error when deleting hybrid compute {0}: {1}'.format(self.name, exc.message))

    def to_dict(self, pip):
        if not pip:
            return None
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


def main():
    AzureRMHybridCompute()


if __name__ == '__main__':
    main()
