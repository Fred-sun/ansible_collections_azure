#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_oracleautonomousdatabase_info
version_added: "3.9.0"
short_description: Get or list Oracle Autonomous Database
description:
    - Get or list Autonomous Database.

options:
    name:
        description:
            - The name of the database.
        type: str
    resource_group:
        description:
            - The name of the resource group. The name is case insensitive.
        type: str
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list
        elements: str

extends_documentation_fragment:
    - azure.azcollection.azure

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Get Oracle Autonomous Database
  azure.azcollection.azure_rm_oracleautonomousdatabase_info:
    name: databasename
    resource_group: Resource_Group_Name

- name: List all Oracle Autonomous Database in the resource_group
  azure.azcollection.azure_rm_oracleautonomousdatabase_info:
    resource_group: Resource_Group_Name

- name: List all Oracle Autonomous Database in the current subscription
  azure.azcollection.azure_rm_oracleautonomousdatabase_info:
'''

RETURN = '''
oracleautonomousdatabases:
    description:
        - List of oracle autonomous databases.
    type: complex
    returned: always
    contains:
        etag:
            description:
                - Resource entity tag (ETag).
            type: str
            returned: always
            sample: "3d001f14-0000-0100-0000-68ca270a0000"
        provisioning_state:
            description:
                - The resource provisioning state. This property is READ-ONLY.
            type: str
            returned: always
            sample: Succeeded
        system_data:
            description:
                - Metadata pertaining to creation and last modification of the resource.
            type: dict
            returned: always
            sample: {
                "created_at": "2025-09-17T03:12:08.743499Z",
                "created_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "created_by_type": "Application",
                "last_modified_at": "2025-09-17T03:12:08.743499Z",
                "last_modified_by": "00867800-0fa3-4d02-8bc8-35edac3a0d32",
                "last_modified_by_type": "Application"
            }
        tags:
            description:
                - Resource tags.
            returned: always
            type: dict
            sample: {'key1': 'value1'}
        type:
            description:
                - The type of the resource.
            returned: always
            type: str
            sample: 
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase


class AzureRMOracleAutonomousDatabaseInfo(AzureRMModuleBase):
    """Information class for an Azure RM Data Collection Rules"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str'),
            resource_group=dict(type='str'),
            tags=dict(type='list', elements='str')
        )

        self.required_by = {
            'name': 'resource_group'
        }

        self.resource_group = None
        self.name = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            oracleautonomousdatabases=[]
        )

        super(AzureRMOracleAutonomousDatabaseInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=False,
                                                                  facts_module=True,
                                                                  required_by=self.required_by)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.name:
            result = self.get_autonomousdatabase()
        else:
            result = self.list_autonomousdatabases()

        self.results['autonomousdatabases'] = result

        return self.results

    def get_autonomousdatabase(self):
        '''
        Gets the specified data collection rule endpoint
        '''
        result = []
        response = None

        try:
            response = self.oracle_autonomous_database_client.autonomous_databases.get(self.resource_group, self.name)
        except Exception as ex:
            self.log("Could not find oracle autonomous database {0} in resource group {1}, Exception as {2}".format(self.name, self.resource_group, ex))
            return []
        if response and self.has_tags(response.tags, self.tags):
            result = [response.as_dict()]
        return result

    def list_autonomousdatabases(self):
        '''
        Lists Data Collection Endpoint for the specified resource.
        '''
        result = []
        response = None

        if self.resource_group:
            try:
                response = self.oracle_autonomous_database_client.autonomous_databases.list_by_resource_group(self.resource_group)
            except Exception as ex:
                self.log("Could not list oracle autonomous database in resource group {0}, Exception as {1}".format(self.resource_group, ex))
                return []
        else:
            try:
                response = self.oracle_autonomous_database_client.autonomous_databases.list_by_subscription()
            except Exception as ex:
                self.log("Could not list oracle autonomous database in the subscription_id, Exception as {0}".format(ex))
                return []
        if response:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    result.append(item.as_dict())

        return result


def main():
    """Main execution"""
    AzureRMOracleAutonomousDatabaseInfo()


if __name__ == '__main__':
    main()
