# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
# pylint: disable=too-many-lines

from azure.cli.core.aaz import *


@register_command(
    "databricks workspace create",
    is_preview=True,
)
class Create(AAZCommand):
    """Create a new workspace.

    :example: Create a workspace
        az databricks workspace create --resource-group MyResourceGroup --name MyWorkspace --location westus --sku standard

    :example: Create a workspace with managed identity for storage account
        az databricks workspace create --resource-group MyResourceGroup --name MyWorkspace --location eastus2euap --sku premium --prepare-encryption
    """

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations(), result_callback=self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.workspace_name = AAZStrArg(
            options=['--workspace-name', '--name', '-n'],
            help='The name of the workspace.',
            required=True,
            id_part='name',
        )
        _args_schema.location = AAZResourceLocationArg(
            help='The geo-location where the resource lives',
            required=True,
        )
        _args_schema.authorizations = AAZListArg(
            options=['--authorizations'],
            singular_options=['--authorization'],
            help='The workspace provider authorizations.',
        )
        _args_schema.managed_resource_group_id = AAZStrArg(
            options=['--managed-resource-group-id'],
            help='The managed resource group Id.',
            required=True,
        )
        _args_schema.parameters = AAZObjectArg(
            options=['--parameters'],
            help='The workspace\'s custom parameters.',
        )
        _args_schema.ui_definition_uri = AAZStrArg(
            options=['--ui-definition-uri'],
            help='The blob URI where the UI definition file is located.',
        )
        _args_schema.sku = AAZObjectArg(
            options=['--sku'],
            help='The SKU of the resource.',
        )
        _args_schema.tags = AAZDictArg(
            options=['--tags'],
            help='Resource tags.',
        )

        authorizations = cls._args_schema.authorizations
        authorizations.Element = AAZObjectArg(
        )

        _element = cls._args_schema.authorizations.Element
        _element.principal_id = AAZStrType(
            options=['principal-id'],
            help='The provider\'s principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.',
            required=True,
        )
        _element.role_definition_id = AAZStrType(
            options=['role-definition-id'],
            help='The provider\'s role definition identifier. This role will define all the permissions that the provider must have on the workspace\'s container resource group. This role definition cannot have permission to delete the resource group.',
            required=True,
        )

        parameters = cls._args_schema.parameters
        parameters.aml_workspace_id = AAZObjectArg(
            options=['aml-workspace-id'],
            help='The ID of a Azure Machine Learning workspace to link with Databricks workspace',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.aml_workspace_id)
        parameters.custom_private_subnet_name = AAZObjectArg(
            options=['custom-private-subnet-name'],
            help='The name of the Private Subnet within the Virtual Network',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.custom_private_subnet_name)
        parameters.custom_public_subnet_name = AAZObjectArg(
            options=['custom-public-subnet-name'],
            help='The name of a Public Subnet within the Virtual Network',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.custom_public_subnet_name)
        parameters.custom_virtual_network_id = AAZObjectArg(
            options=['custom-virtual-network-id'],
            help='The ID of a Virtual Network where this Databricks Cluster should be created',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.custom_virtual_network_id)
        parameters.enable_no_public_ip = AAZObjectArg(
            options=['enable-no-public-ip'],
            help='Should the Public IP be Disabled?',
        )
        cls._build_args_workspace_custom_boolean_parameter_create(parameters.enable_no_public_ip)
        parameters.encryption = AAZObjectArg(
            options=['encryption'],
            help='Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.',
        )
        parameters.load_balancer_backend_pool_name = AAZObjectArg(
            options=['load-balancer-backend-pool-name'],
            help='Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.load_balancer_backend_pool_name)
        parameters.load_balancer_id = AAZObjectArg(
            options=['load-balancer-id'],
            help='Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.load_balancer_id)
        parameters.nat_gateway_name = AAZObjectArg(
            options=['nat-gateway-name'],
            help='Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.nat_gateway_name)
        parameters.prepare_encryption = AAZObjectArg(
            options=['prepare-encryption'],
            help='Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.',
        )
        cls._build_args_workspace_custom_boolean_parameter_create(parameters.prepare_encryption)
        parameters.public_ip_name = AAZObjectArg(
            options=['public-ip-name'],
            help='Name of the Public IP for No Public IP workspace with managed vNet.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.public_ip_name)
        parameters.require_infrastructure_encryption = AAZObjectArg(
            options=['require-infrastructure-encryption'],
            help='A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.',
        )
        cls._build_args_workspace_custom_boolean_parameter_create(parameters.require_infrastructure_encryption)
        parameters.storage_account_name = AAZObjectArg(
            options=['storage-account-name'],
            help='Default DBFS storage account name.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.storage_account_name)
        parameters.storage_account_sku_name = AAZObjectArg(
            options=['storage-account-sku-name'],
            help='Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.storage_account_sku_name)
        parameters.vnet_address_prefix = AAZObjectArg(
            options=['vnet-address-prefix'],
            help='Address prefix for Managed virtual network. Default value for this input is 10.139.',
        )
        cls._build_args_workspace_custom_string_parameter_create(parameters.vnet_address_prefix)

        encryption = cls._args_schema.parameters.encryption
        encryption.value = AAZObjectArg(
            options=['value'],
            help='The value which should be used for this field.',
        )

        value = cls._args_schema.parameters.encryption.value
        value.key_name = AAZStrArg(
            options=['key-name'],
            help='The name of KeyVault key.',
        )
        value.key_source = AAZStrArg(
            options=['key-source'],
            help='The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault',
            default='Default',
            enum={'Default': 'Default', 'Microsoft.Keyvault': 'Microsoft.Keyvault'},
        )
        value.keyvaulturi = AAZStrArg(
            options=['keyvaulturi'],
            help='The Uri of KeyVault.',
        )
        value.keyversion = AAZStrArg(
            options=['keyversion'],
            help='The version of KeyVault key.',
        )

        sku = cls._args_schema.sku
        sku.name = AAZStrArg(
            options=['name'],
            help='The SKU name.',
            required=True,
        )
        sku.tier = AAZStrArg(
            options=['tier'],
            help='The SKU tier.',
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
        )
        return _args_schema

    _args_workspace_custom_boolean_parameter_create = None

    @classmethod
    def _build_args_workspace_custom_boolean_parameter_create(cls, _schema):
        if cls._args_workspace_custom_boolean_parameter_create is not None:
            _schema.value = cls._args_workspace_custom_boolean_parameter_create.value
            return

        cls._args_workspace_custom_boolean_parameter_create = AAZObjectArg(
        )

        workspace_custom_boolean_parameter_create = cls._args_workspace_custom_boolean_parameter_create
        workspace_custom_boolean_parameter_create.value = AAZBoolArg(
            options=['value'],
            help='The value which should be used for this field.',
            required=True,
        )

        _schema.value = cls._args_workspace_custom_boolean_parameter_create.value

    _args_workspace_custom_string_parameter_create = None

    @classmethod
    def _build_args_workspace_custom_string_parameter_create(cls, _schema):
        if cls._args_workspace_custom_string_parameter_create is not None:
            _schema.value = cls._args_workspace_custom_string_parameter_create.value
            return

        cls._args_workspace_custom_string_parameter_create = AAZObjectArg(
        )

        workspace_custom_string_parameter_create = cls._args_workspace_custom_string_parameter_create
        workspace_custom_string_parameter_create.value = AAZStrArg(
            options=['value'],
            help='The value which should be used for this field.',
            required=True,
        )

        _schema.value = cls._args_workspace_custom_string_parameter_create.value

    def _execute_operations(self):
        yield self.WorkspacesCreateOrUpdate(ctx=self.ctx)()

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class WorkspacesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"
        ERROR_FORMAT = "ODataV4Format"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    deserialization_callback=self.on_200_201,
                    lro_options={'final-state-via': 'azure-async-operation'},
                    path_format_arguments=self.url_parameters,
                )
            return self.on_error(session)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", '2018-04-01',
                    required=True,
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content(
                self.ctx.args,
                typ=AAZObjectType,
            )
            _builder.set_prop('tags', AAZDictType, '.tags')
            _builder.set_prop('location', AAZStrType, '.location', typ_kwargs={'flags': {'required': True}})
            _builder.set_prop('properties', AAZObjectType, '.', typ_kwargs={'flags': {'required': True, 'client_flatten': True}})
            _builder.set_prop('sku', AAZObjectType, '.sku')

            tags = _builder.get('.tags')
            if tags is not None:
                tags.set_elements(AAZStrType, '.')

            properties = _builder.get('.properties')
            if properties is not None:
                properties.set_prop('managedResourceGroupId', AAZStrType, '.managed_resource_group_id', typ_kwargs={'flags': {'required': True}})
                properties.set_prop('parameters', AAZObjectType, '.parameters')
                properties.set_prop('uiDefinitionUri', AAZStrType, '.ui_definition_uri')
                properties.set_prop('authorizations', AAZListType, '.authorizations')

            parameters = _builder.get('.properties.parameters')
            if parameters is not None:
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('amlWorkspaceId', AAZObjectType, '.aml_workspace_id'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('customVirtualNetworkId', AAZObjectType, '.custom_virtual_network_id'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('customPublicSubnetName', AAZObjectType, '.custom_public_subnet_name'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('customPrivateSubnetName', AAZObjectType, '.custom_private_subnet_name'))
                _build_schema_workspace_custom_boolean_parameter_create(parameters.set_prop('enableNoPublicIp', AAZObjectType, '.enable_no_public_ip'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('loadBalancerBackendPoolName', AAZObjectType, '.load_balancer_backend_pool_name'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('loadBalancerId', AAZObjectType, '.load_balancer_id'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('natGatewayName', AAZObjectType, '.nat_gateway_name'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('publicIpName', AAZObjectType, '.public_ip_name'))
                _build_schema_workspace_custom_boolean_parameter_create(parameters.set_prop('prepareEncryption', AAZObjectType, '.prepare_encryption'))
                parameters.set_prop('encryption', AAZObjectType, '.encryption')
                _build_schema_workspace_custom_boolean_parameter_create(parameters.set_prop('requireInfrastructureEncryption', AAZObjectType, '.require_infrastructure_encryption'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('storageAccountName', AAZObjectType, '.storage_account_name'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('storageAccountSkuName', AAZObjectType, '.storage_account_sku_name'))
                _build_schema_workspace_custom_string_parameter_create(parameters.set_prop('vnetAddressPrefix', AAZObjectType, '.vnet_address_prefix'))

            encryption = _builder.get('.properties.parameters.encryption')
            if encryption is not None:
                encryption.set_prop('value', AAZObjectType, '.value')

            value = _builder.get('.properties.parameters.encryption.value')
            if value is not None:
                value.set_prop('keySource', AAZStrType, '.key_source')
                value.set_prop('KeyName', AAZStrType, '.key_name')
                value.set_prop('keyversion', AAZStrType, '.keyversion')
                value.set_prop('keyvaulturi', AAZStrType, '.keyvaulturi')

            authorizations = _builder.get('.properties.authorizations')
            if authorizations is not None:
                authorizations.set_elements(AAZObjectType)

            _elements = _builder.get('.properties.authorizations[]')
            if _elements is not None:
                _elements.set_prop('principalId', AAZStrType, '.principal_id', typ_kwargs={'flags': {'required': True}})
                _elements.set_prop('roleDefinitionId', AAZStrType, '.role_definition_id', typ_kwargs={'flags': {'required': True}})

            sku = _builder.get('.sku')
            if sku is not None:
                sku.set_prop('name', AAZStrType, '.name', typ_kwargs={'flags': {'required': True}})
                sku.set_prop('tier', AAZStrType, '.tier')

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                'self.ctx.vars.instance',
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType (
            )

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.id = AAZStrType(
                flags={'read_only': True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={'read_only': True},
            )
            _schema_on_200_201.type = AAZStrType(
                flags={'read_only': True},
            )
            _schema_on_200_201.tags = AAZDictType(
            )
            _schema_on_200_201.location = AAZStrType(
                flags={'required': True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={'required': True, 'client_flatten': True},
            )
            _schema_on_200_201.sku = AAZObjectType(
            )

            tags = cls._schema_on_200_201.tags
            tags.Element = AAZStrType(
            )

            properties = cls._schema_on_200_201.properties
            properties.managed_resource_group_id = AAZStrType(
                serialized_name='managedResourceGroupId',
                flags={'required': True},
            )
            properties.parameters = AAZObjectType(
            )
            properties.provisioning_state = AAZStrType(
                serialized_name='provisioningState',
                flags={'read_only': True},
            )
            properties.ui_definition_uri = AAZStrType(
                serialized_name='uiDefinitionUri',
            )
            properties.authorizations = AAZListType(
            )
            properties.created_by = AAZObjectType(
                serialized_name='createdBy',
            )
            _build_schema_created_by_read(properties.created_by)
            properties.updated_by = AAZObjectType(
                serialized_name='updatedBy',
            )
            _build_schema_created_by_read(properties.updated_by)
            properties.created_date_time = AAZStrType(
                serialized_name='createdDateTime',
                flags={'read_only': True},
            )
            properties.workspace_id = AAZStrType(
                serialized_name='workspaceId',
                flags={'read_only': True},
            )
            properties.workspace_url = AAZStrType(
                serialized_name='workspaceUrl',
                flags={'read_only': True},
            )
            properties.storage_account_identity = AAZObjectType(
                serialized_name='storageAccountIdentity',
            )

            parameters = cls._schema_on_200_201.properties.parameters
            parameters.aml_workspace_id = AAZObjectType(
                serialized_name='amlWorkspaceId',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.aml_workspace_id)
            parameters.custom_virtual_network_id = AAZObjectType(
                serialized_name='customVirtualNetworkId',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.custom_virtual_network_id)
            parameters.custom_public_subnet_name = AAZObjectType(
                serialized_name='customPublicSubnetName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.custom_public_subnet_name)
            parameters.custom_private_subnet_name = AAZObjectType(
                serialized_name='customPrivateSubnetName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.custom_private_subnet_name)
            parameters.enable_no_public_ip = AAZObjectType(
                serialized_name='enableNoPublicIp',
            )
            _build_schema_workspace_custom_boolean_parameter_read(parameters.enable_no_public_ip)
            parameters.load_balancer_backend_pool_name = AAZObjectType(
                serialized_name='loadBalancerBackendPoolName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_backend_pool_name)
            parameters.load_balancer_id = AAZObjectType(
                serialized_name='loadBalancerId',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_id)
            parameters.nat_gateway_name = AAZObjectType(
                serialized_name='natGatewayName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.nat_gateway_name)
            parameters.public_ip_name = AAZObjectType(
                serialized_name='publicIpName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.public_ip_name)
            parameters.prepare_encryption = AAZObjectType(
                serialized_name='prepareEncryption',
            )
            _build_schema_workspace_custom_boolean_parameter_read(parameters.prepare_encryption)
            parameters.encryption = AAZObjectType(
            )
            parameters.require_infrastructure_encryption = AAZObjectType(
                serialized_name='requireInfrastructureEncryption',
            )
            _build_schema_workspace_custom_boolean_parameter_read(parameters.require_infrastructure_encryption)
            parameters.storage_account_name = AAZObjectType(
                serialized_name='storageAccountName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.storage_account_name)
            parameters.storage_account_sku_name = AAZObjectType(
                serialized_name='storageAccountSkuName',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.storage_account_sku_name)
            parameters.vnet_address_prefix = AAZObjectType(
                serialized_name='vnetAddressPrefix',
            )
            _build_schema_workspace_custom_string_parameter_read(parameters.vnet_address_prefix)
            parameters.resource_tags = AAZObjectType(
                serialized_name='resourceTags',
                flags={'read_only': True},
            )

            encryption = cls._schema_on_200_201.properties.parameters.encryption
            encryption.type = AAZStrType(
                flags={'read_only': True},
            )
            encryption.value = AAZObjectType(
            )

            value = cls._schema_on_200_201.properties.parameters.encryption.value
            value.key_source = AAZStrType(
                serialized_name='keySource',
            )
            value.key_name = AAZStrType(
                serialized_name='KeyName',
            )
            value.keyversion = AAZStrType(
            )
            value.keyvaulturi = AAZStrType(
            )

            resource_tags = cls._schema_on_200_201.properties.parameters.resource_tags
            resource_tags.type = AAZStrType(
                flags={'read_only': True},
            )
            resource_tags.value = AAZDictType(
                flags={'required': True, 'read_only': True},
            )

            authorizations = cls._schema_on_200_201.properties.authorizations
            authorizations.Element = AAZObjectType(
            )

            _element = cls._schema_on_200_201.properties.authorizations.Element
            _element.principal_id = AAZStrType(
                serialized_name='principalId',
                flags={'required': True},
            )
            _element.role_definition_id = AAZStrType(
                serialized_name='roleDefinitionId',
                flags={'required': True},
            )

            storage_account_identity = cls._schema_on_200_201.properties.storage_account_identity
            storage_account_identity.principal_id = AAZStrType(
                serialized_name='principalId',
                flags={'read_only': True},
            )
            storage_account_identity.tenant_id = AAZStrType(
                serialized_name='tenantId',
                flags={'read_only': True},
            )
            storage_account_identity.type = AAZStrType(
                flags={'read_only': True},
            )

            sku = cls._schema_on_200_201.sku
            sku.name = AAZStrType(
                flags={'required': True},
            )
            sku.tier = AAZStrType(
            )

            return cls._schema_on_200_201


def _build_schema_workspace_custom_boolean_parameter_create(_builder):
    if _builder is None:
        return
    _builder.set_prop('value', AAZBoolType, '.value', typ_kwargs={'flags': {'required': True}})


def _build_schema_workspace_custom_string_parameter_create(_builder):
    if _builder is None:
        return
    _builder.set_prop('value', AAZStrType, '.value', typ_kwargs={'flags': {'required': True}})


_schema_created_by_read = None


def _build_schema_created_by_read(_schema):
    global _schema_created_by_read
    if _schema_created_by_read is not None:
        _schema.application_id = _schema_created_by_read.application_id
        _schema.oid = _schema_created_by_read.oid
        _schema.puid = _schema_created_by_read.puid
        return

    _schema_created_by_read = AAZObjectType(
    )

    created_by_read = _schema_created_by_read
    created_by_read.oid = AAZStrType(
        flags={'read_only': True},
    )
    created_by_read.puid = AAZStrType(
        flags={'read_only': True},
    )
    created_by_read.application_id = AAZStrType(
        serialized_name='applicationId',
        flags={'read_only': True},
    )

    _schema.application_id = _schema_created_by_read.application_id
    _schema.oid = _schema_created_by_read.oid
    _schema.puid = _schema_created_by_read.puid


_schema_workspace_custom_boolean_parameter_read = None


def _build_schema_workspace_custom_boolean_parameter_read(_schema):
    global _schema_workspace_custom_boolean_parameter_read
    if _schema_workspace_custom_boolean_parameter_read is not None:
        _schema.type = _schema_workspace_custom_boolean_parameter_read.type
        _schema.value = _schema_workspace_custom_boolean_parameter_read.value
        return

    _schema_workspace_custom_boolean_parameter_read = AAZObjectType(
    )

    workspace_custom_boolean_parameter_read = _schema_workspace_custom_boolean_parameter_read
    workspace_custom_boolean_parameter_read.type = AAZStrType(
        flags={'read_only': True},
    )
    workspace_custom_boolean_parameter_read.value = AAZBoolType(
        flags={'required': True},
    )

    _schema.type = _schema_workspace_custom_boolean_parameter_read.type
    _schema.value = _schema_workspace_custom_boolean_parameter_read.value


_schema_workspace_custom_string_parameter_read = None


def _build_schema_workspace_custom_string_parameter_read(_schema):
    global _schema_workspace_custom_string_parameter_read
    if _schema_workspace_custom_string_parameter_read is not None:
        _schema.type = _schema_workspace_custom_string_parameter_read.type
        _schema.value = _schema_workspace_custom_string_parameter_read.value
        return

    _schema_workspace_custom_string_parameter_read = AAZObjectType(
    )

    workspace_custom_string_parameter_read = _schema_workspace_custom_string_parameter_read
    workspace_custom_string_parameter_read.type = AAZStrType(
        flags={'read_only': True},
    )
    workspace_custom_string_parameter_read.value = AAZStrType(
        flags={'required': True},
    )

    _schema.type = _schema_workspace_custom_string_parameter_read.type
    _schema.value = _schema_workspace_custom_string_parameter_read.value


__all__ = ['Create']
