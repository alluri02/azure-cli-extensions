# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "network manager routing-config rule-collection rule wait",
)
class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.network/networkmanagers/{}/routingconfigurations/{}/rulecollections/{}/rules/{}", "2024-05-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.config_name = AAZStrArg(
            options=["--config-name"],
            help="The name of the network manager Routing Configuration.",
            required=True,
            id_part="child_name_1",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9_.-]*$",
            ),
        )
        _args_schema.manager_name = AAZStrArg(
            options=["--manager-name"],
            help="The name of the network manager.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9_.-]*$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.collection_name = AAZStrArg(
            options=["--collection-name"],
            help="The name of the network manager routing Configuration rule collection.",
            required=True,
            id_part="child_name_2",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9_.-]*$",
            ),
        )
        _args_schema.rule_name = AAZStrArg(
            options=["-n", "--name", "--rule-name"],
            help="The name of the rule.",
            required=True,
            id_part="child_name_3",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9_.-]*$",
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.RoutingRulesGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=False)
        return result

    class RoutingRulesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkManagers/{networkManagerName}/routingConfigurations/{configurationName}/ruleCollections/{ruleCollectionName}/rules/{ruleName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "configurationName", self.ctx.args.config_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "networkManagerName", self.ctx.args.manager_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "ruleCollectionName", self.ctx.args.collection_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "ruleName", self.ctx.args.rule_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-05-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.etag = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.description = AAZStrType()
            properties.destination = AAZObjectType(
                flags={"required": True},
            )
            properties.next_hop = AAZObjectType(
                serialized_name="nextHop",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.resource_guid = AAZStrType(
                serialized_name="resourceGuid",
                flags={"read_only": True},
            )

            destination = cls._schema_on_200.properties.destination
            destination.destination_address = AAZStrType(
                serialized_name="destinationAddress",
                flags={"required": True},
            )
            destination.type = AAZStrType(
                flags={"required": True},
            )

            next_hop = cls._schema_on_200.properties.next_hop
            next_hop.next_hop_address = AAZStrType(
                serialized_name="nextHopAddress",
            )
            next_hop.next_hop_type = AAZStrType(
                serialized_name="nextHopType",
                flags={"required": True},
            )

            system_data = cls._schema_on_200.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            return cls._schema_on_200


class _WaitHelper:
    """Helper class for Wait"""


__all__ = ["Wait"]
