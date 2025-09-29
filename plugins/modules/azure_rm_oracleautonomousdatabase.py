#!/usr/bin/python
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: azure_rm_oracleautonomousdatabase
version_added: "3.9.0"
short_description: Managed the Oracle Autonomous Database
description:
    - Create, update and delete Oracle Autonomous Database

options:
    name:
        description:
            - The name of the oracle autonomous database you're creating/changing
        required: true
        type: str
    resource_group:
        description:
            - The name of the resource group
        required: true
        type: str
    location:
        description:
            - Location of the resource.
        type: str
    state:
        description:
            - State of the oracle autonomous database
            - Use C(present) for creating/updating a oracle autonomous database.
            - Use C(absent) for deleting a oracle autonomous database.
        default: present
        type: str
        choices:
            - present
            - absent
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags

author:
    - magodo (@magodo)
    - Fred Sun (@Fred-sun)
'''

EXAMPLES = '''
- name: Create a new oracle autonomous database
  azure.azcollection.azure_rm_oracleautonomousdatabase:
    state: present
    name: oracle_autonomous_database_name
    resource_group: resource_group_name
    location: westeurope

- name: Delete a oracle autonomous database
  azure.azcollection.azure_rm_oracleautonomousdatabase:
    state: present
    name: oracle_autonomous_database_name
    resource_group: resource_group_name
'''

RETURN = '''
oracleautonomousdatabase:
    description:
        - Details of the oracle autonomous database
    type: dict
    returned: always
    sample: {}
'''

from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt

try:
    from azure.core.exceptions import ResourceNotFoundError

except ImportError:
    # This is handled in azure_rm_common
    pass

AZURE_OBJECT_CLASS = 'OracleAutonomousDatabase'


properties_spec = dict(
    data_base_type=dict(type='str', choices=['Regular', 'Clone', 'CloneFromBackupTimestamp', 'CrossRegionDisasterRecovery']),
    admin_password=dict(type='str'),
    autonomous_maintenance_schedule_type=dict(type='str', choices=['Early', 'Regular']),
    character_set=dict(type='str'),
    compute_count=dict(type='int'),
    compute_model=dict(type='str', choices=['ECPU', 'OCPU']),
    cpu_core_count=dict(type='int'),
    customer_contacts=dict(type='list', elements='dict', options=dict(email=dict(type='str'))),
    data_storage_size_in_tbs=dict(type='int'),
    data_storage_size_in_gbs=dict(type='int'),
    db_version=dict(type='str'),
    db_workload=dict(type='str', chices=['OLTP', 'DW', 'AJD', 'APEX']),
    display_name=dict(type='str'),
    is_auto_scaling_enabled=dict(type='bool'),
    is_auto_scaling_for_storage_enabled=dict(type='bool'),
    peer_db_id=dict(type='str'),
    peer_db_ids=dict(type='list', elements='str'),
    is_local_data_guard_enabled=dict(type='bool'),
    is_mtls_connection_required=dict(type='bool'),
    is_preview_version_with_service_terms_accepted=dict(type='bool'),
    license_model=dict(type='str', choices=['LicenseIncluded', 'BringYourOwnLicense']),
    ncharacter_set=dict(type='str'),
    private_endpoint_ip=dict(type='str'),
    private_endpoint_label=dict(type='str'),
    subnet_id=dict(type='str'),
    vnet_id=dict(type='str'),
    database_edition=dict(type='str'),
    autonomous_database_id=dict(type='str'),
    local_adg_auto_failover_max_data_loss_limit=dict(type='int'),
    open_mode=dict(type='str', choices=['ReadOnly', 'ReadWrite']),
    permission_level=dict(type='str', choices=['Restricted', 'Unrestricted']),
    role=dict(type='str', choices=['Primary', 'Standby', 'DisabledStandby', 'BackupCopy', 'SnapshotStandby']),
    backup_retention_period_in_days=dict(type='int'),
    whitelisted_ips=dict(type='list', elements='str')
)


class AzureRMOracleAutonomousDatabase(AzureRMModuleBaseExt):
    """Information class for an Azure RM Oracle Autonomous Database"""

    def __init__(self):
        self.module_arg_spec = dict(
            name=dict(type='str', required=True),
            resource_group=dict(type='str', required=True),
            location=dict(type='str'),
            properties=dict(type='dict', options=properties_spec),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )

        self.name = None
        self.resource_group = None
        self.location = None
        self.properties = None
        self.state = None
        self.tags = None
        self.log_path = None
        self.log_mode = None

        self.results = dict(
            changed=False,
            oracleautonomousdatabase=dict(),
            diff=dict(
                before=None,
                after=None
            )
        )

        super(AzureRMOracleAutonomousDatabase, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        # Defaults for variables
        result = None
        result_compare = dict(compare=[])
        before_dict = None

        # Get current oracle autonomous database if it exists
        before_dict = self.get_oracle_autonomous_database()

        # Create dict from input, without None values
        # https://learn.microsoft.com/en-us/python/api/azure-mgmt-monitor/azure.mgmt.monitor.v2021_04_01.models.oracleautonomousdatabaseresource?view=azure-python
        oracle_autonomous_database_template = {
            "location": self.location,
            "properties": self.properties,
            "tags": self.tags
        }
        # Filter out all None values
        oracle_autonomous_database_input = {key: value for key, value in oracle_autonomous_database_template.items() if value is not None}

        # Create/Update if state==present
        if self.state == 'present':
            if before_dict is None:
                # Oracle Autonomous Database does not exist, create
                # On creation default to location of resource group unless otherwise noted in input variables
                if not self.location:
                    resource_group = self.get_resource_group(self.resource_group)
                    oracle_autonomous_database_input['location'] = resource_group.location
                # On creation input == what we send to api
                oracle_autonomous_database_update = oracle_autonomous_database_input
                # Needs to be extended by tags if set
                if self.tags:
                    oracle_autonomous_database_update['tags'] = self.tags
                self.results['changed'] = True
                if self.check_mode:
                    # Check mode, skipping actual creation
                    pass
                else:
                    create_response = self.create_or_update(oracle_autonomous_database_update)
            else:
                # Oracle Autonomous Database already exists, updating it
                # Dict for update is the union of existing object overwritten by input data
                oracle_autonomous_database_update = before_dict | oracle_autonomous_database_input

                # Enhanced with tags (special behaviour because of append_tags possibility)
                update_tags, update_tags_content = self.update_tags(before_dict.get('tags'))
                # Check if we need to update the oracle autonomous database
                if update_tags or not self.default_compare({}, oracle_autonomous_database_update, before_dict, '', result_compare):
                    oracle_autonomous_database_update['tags'] = update_tags_content
                    # Need to create/update the Oracle Autonomous Database; changed -> True
                    self.results['changed'] = True
                    if self.check_mode:
                        # Check mode, skipping actual creation
                        pass
                    else:
                        create_response = self.create_or_update(oracle_autonomous_database_update)

            if self.check_mode or not self.results['changed']:
                # When object was not updated or when running in check mode
                # assume oracle_autonomous_database_update is resulting object
                result = oracle_autonomous_database_update
            else:
                # otherwise take resulting new object from response of create call
                result = create_response

        # Delete oracle autonomous database if state is absent and it exists
        # if it doesn't exist, it's already absent
        elif self.state == 'absent' and before_dict is not None:
            self.results['changed'] = True
            if self.check_mode:
                # do not delete in check mode
                pass
            else:
                self.delete()

        self.results['diff']['before'] = before_dict
        self.results['diff']['after'] = result
        self.results['oracleautonomousdatabase'] = result

        return self.results

    def get_oracle_autonomous_database(self):
        '''
        Gets the properties of the specified oracle autonomous database.

        :return: List of Oracle Autonomous Database
        '''
        self.log("Checking if oracle autonomous database {0} in resource group {1} is present".format(self.name,
                                                                                                self.resource_group))

        response = None

        try:
            response = self.oracle_autonomous_database_client.autonomous_databases.get(self.resource_group, self.name)
        except ResourceNotFoundError:
            self.log("Could not find oracle autonomous database {0} in resource group {1}".format(self.name, self.resource_group))
        if response:
            return self.serialize_obj(response, AZURE_OBJECT_CLASS)

    def create_or_update(self, oracle_autonomous_database_update):
        result = None
        response = None
        try:
            response = self.oracle_autonomous_database_client.autonomous_databases.begin_create_or_update(self.resource_group, self.name, oracle_autonomous_database_update)
        except Exception as ex:
            self.fail("Error creating or update oracle autonomous database {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        if response:
            result = self.serialize_obj(response, AZURE_OBJECT_CLASS)

        return result

    def delete(self):
        response = None
        try:
            response = self.oracle_autonomous_database_client.autonomous_databases.begin_delete(resource_group_name=self.resource_group,
                                                                                          oracle_autonomous_database_name=self.name)
        except Exception as ex:
            self.fail("Error deleting oracle autonomous database {0} in resource group {1}: {2}".format(self.name, self.resource_group, str(ex)))

        return response


def main():
    """Main execution"""
    AzureRMOracleAutonomousDatabase()


if __name__ == '__main__':
    main()
