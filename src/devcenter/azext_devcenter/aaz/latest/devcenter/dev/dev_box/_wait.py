# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["data-plane:microsoft.devcenter", "/projects/{}/users/{}/devboxes/{}", "2025-04-01-preview"],
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

        # define Arg Group "Client"

        _args_schema = cls._args_schema
        _args_schema.endpoint = AAZStrArg(
            options=["--endpoint"],
            arg_group="Client",
            help="The API endpoint for the developer resources. Use az configure -d endpoint=<endpoint_uri> to configure a default.",
            required=True,
        )

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.dev_box_name = AAZStrArg(
            options=["-n", "--name", "--dev-box", "--dev-box-name"],
            help="The name of a dev box.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9-_.]{2,62}$",
                max_length=63,
                min_length=3,
            ),
        )
        _args_schema.project_name = AAZStrArg(
            options=["--project", "--project-name"],
            help="The name of the project. Use az configure -d project=<project_name> to configure a default.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9-_.]{2,62}$",
                max_length=63,
                min_length=3,
            ),
        )
        _args_schema.user_id = AAZStrArg(
            options=["--user-id"],
            help="The AAD object id of the user. If value is 'me', the identity is taken from the authentication context.",
            required=True,
            default="me",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9]{8}-([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12}$|^me$",
                max_length=36,
                min_length=2,
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.DevBoxesGetDevBoxByUser(ctx=self.ctx)()
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

    class DevBoxesGetDevBoxByUser(AAZHttpOperation):
        CLIENT_TYPE = "AAZMicrosoftDevcenterDataPlaneClient_devcenter"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/projects/{projectName}/users/{userId}/devboxes/{devBoxName}",
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
                    "endpoint", self.ctx.args.endpoint,
                    skip_quote=True,
                    required=True,
                ),
                **self.serialize_url_param(
                    "devBoxName", self.ctx.args.dev_box_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "projectName", self.ctx.args.project_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "userId", self.ctx.args.user_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2025-04-01-preview",
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
            _schema_on_200.action_state = AAZStrType(
                serialized_name="actionState",
                flags={"read_only": True},
            )
            _schema_on_200.active_hours_configuration = AAZObjectType(
                serialized_name="activeHoursConfiguration",
                flags={"read_only": True},
            )
            _schema_on_200.created_time = AAZStrType(
                serialized_name="createdTime",
                flags={"read_only": True},
            )
            _schema_on_200.error = AAZObjectType(
                flags={"read_only": True},
            )
            _WaitHelper._build_schema_azure_core_foundations_error_read(_schema_on_200.error)
            _schema_on_200.hardware_profile = AAZObjectType(
                serialized_name="hardwareProfile",
                flags={"read_only": True},
            )
            _schema_on_200.hibernate_support = AAZStrType(
                serialized_name="hibernateSupport",
                flags={"read_only": True},
            )
            _schema_on_200.image_reference = AAZObjectType(
                serialized_name="imageReference",
                flags={"read_only": True},
            )
            _schema_on_200.last_connected_time = AAZStrType(
                serialized_name="lastConnectedTime",
                flags={"read_only": True},
            )
            _schema_on_200.local_administrator = AAZStrType(
                serialized_name="localAdministrator",
                flags={"read_only": True},
            )
            _schema_on_200.location = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.os_type = AAZStrType(
                serialized_name="osType",
                flags={"read_only": True},
            )
            _schema_on_200.pool_name = AAZStrType(
                serialized_name="poolName",
                flags={"required": True},
            )
            _schema_on_200.power_state = AAZStrType(
                serialized_name="powerState",
                flags={"read_only": True},
            )
            _schema_on_200.project_name = AAZStrType(
                serialized_name="projectName",
                flags={"read_only": True},
            )
            _schema_on_200.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            _schema_on_200.storage_profile = AAZObjectType(
                serialized_name="storageProfile",
                flags={"read_only": True},
            )
            _schema_on_200.unique_id = AAZStrType(
                serialized_name="uniqueId",
                flags={"read_only": True},
            )
            _schema_on_200.uri = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.user = AAZStrType(
                flags={"read_only": True},
            )

            active_hours_configuration = cls._schema_on_200.active_hours_configuration
            active_hours_configuration.auto_start_enable_status = AAZStrType(
                serialized_name="autoStartEnableStatus",
                flags={"required": True},
            )
            active_hours_configuration.end_time_hour = AAZIntType(
                serialized_name="endTimeHour",
            )
            active_hours_configuration.keep_awake_enable_status = AAZStrType(
                serialized_name="keepAwakeEnableStatus",
                flags={"required": True},
            )
            active_hours_configuration.start_time_hour = AAZIntType(
                serialized_name="startTimeHour",
            )
            active_hours_configuration.time_zone = AAZStrType(
                serialized_name="timeZone",
            )

            hardware_profile = cls._schema_on_200.hardware_profile
            hardware_profile.memory_gb = AAZIntType(
                serialized_name="memoryGB",
                flags={"read_only": True},
            )
            hardware_profile.sku_name = AAZStrType(
                serialized_name="skuName",
                flags={"read_only": True},
            )
            hardware_profile.v_cp_us = AAZIntType(
                serialized_name="vCPUs",
                flags={"read_only": True},
            )

            image_reference = cls._schema_on_200.image_reference
            image_reference.name = AAZStrType(
                flags={"read_only": True},
            )
            image_reference.operating_system = AAZStrType(
                serialized_name="operatingSystem",
                flags={"read_only": True},
            )
            image_reference.os_build_number = AAZStrType(
                serialized_name="osBuildNumber",
                flags={"read_only": True},
            )
            image_reference.published_date = AAZStrType(
                serialized_name="publishedDate",
                flags={"read_only": True},
            )
            image_reference.version = AAZStrType(
                flags={"read_only": True},
            )

            storage_profile = cls._schema_on_200.storage_profile
            storage_profile.os_disk = AAZObjectType(
                serialized_name="osDisk",
            )

            os_disk = cls._schema_on_200.storage_profile.os_disk
            os_disk.disk_size_gb = AAZIntType(
                serialized_name="diskSizeGB",
                flags={"read_only": True},
            )

            return cls._schema_on_200


class _WaitHelper:
    """Helper class for Wait"""

    _schema_azure_core_foundations_error_read = None

    @classmethod
    def _build_schema_azure_core_foundations_error_read(cls, _schema):
        if cls._schema_azure_core_foundations_error_read is not None:
            _schema.code = cls._schema_azure_core_foundations_error_read.code
            _schema.details = cls._schema_azure_core_foundations_error_read.details
            _schema.innererror = cls._schema_azure_core_foundations_error_read.innererror
            _schema.message = cls._schema_azure_core_foundations_error_read.message
            _schema.target = cls._schema_azure_core_foundations_error_read.target
            return

        cls._schema_azure_core_foundations_error_read = _schema_azure_core_foundations_error_read = AAZObjectType(
            flags={"read_only": True}
        )

        azure_core_foundations_error_read = _schema_azure_core_foundations_error_read
        azure_core_foundations_error_read.code = AAZStrType(
            flags={"required": True},
        )
        azure_core_foundations_error_read.details = AAZListType()
        azure_core_foundations_error_read.innererror = AAZObjectType()
        cls._build_schema_azure_core_foundations_inner_error_read(azure_core_foundations_error_read.innererror)
        azure_core_foundations_error_read.message = AAZStrType(
            flags={"required": True},
        )
        azure_core_foundations_error_read.target = AAZStrType()

        details = _schema_azure_core_foundations_error_read.details
        details.Element = AAZObjectType()
        cls._build_schema_azure_core_foundations_error_read(details.Element)

        _schema.code = cls._schema_azure_core_foundations_error_read.code
        _schema.details = cls._schema_azure_core_foundations_error_read.details
        _schema.innererror = cls._schema_azure_core_foundations_error_read.innererror
        _schema.message = cls._schema_azure_core_foundations_error_read.message
        _schema.target = cls._schema_azure_core_foundations_error_read.target

    _schema_azure_core_foundations_inner_error_read = None

    @classmethod
    def _build_schema_azure_core_foundations_inner_error_read(cls, _schema):
        if cls._schema_azure_core_foundations_inner_error_read is not None:
            _schema.code = cls._schema_azure_core_foundations_inner_error_read.code
            _schema.innererror = cls._schema_azure_core_foundations_inner_error_read.innererror
            return

        cls._schema_azure_core_foundations_inner_error_read = _schema_azure_core_foundations_inner_error_read = AAZObjectType()

        azure_core_foundations_inner_error_read = _schema_azure_core_foundations_inner_error_read
        azure_core_foundations_inner_error_read.code = AAZStrType()
        azure_core_foundations_inner_error_read.innererror = AAZObjectType()
        cls._build_schema_azure_core_foundations_inner_error_read(azure_core_foundations_inner_error_read.innererror)

        _schema.code = cls._schema_azure_core_foundations_inner_error_read.code
        _schema.innererror = cls._schema_azure_core_foundations_inner_error_read.innererror


__all__ = ["Wait"]
