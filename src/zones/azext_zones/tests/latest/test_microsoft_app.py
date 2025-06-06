# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure.cli.testsdk import ScenarioTest
from ..._resourceTypeValidation import (
    getResourceTypeValidator,
    load_validators,
    ZoneRedundancyValidationResult,
)


class test_microsoft_app(ScenarioTest):
    resource_zr = {
        "type": "microsoft.app/managedenvironments",
        "resourceGroup": "testResourceGroup",
        "properties": {
            "zoneRedundant": True,
        },
    }

    resource_nonzr = {
        "type": "microsoft.app/managedenvironments",
        "resourceGroup": "testResourceGroup",
        "properties": {
            "zoneRedundant": False,
        },
    }

    validator = None

    @classmethod
    def setUpClass(cls):
        super(test_microsoft_app, cls).setUpClass()
        # Load the resource type validators
        load_validators()

        resourceProvider = cls.resource_zr["type"].split("/")[0]
        cls.validator = getResourceTypeValidator(resourceProvider)

    def test_zr(self):
        # Test for zone redundancy scenario
        zrResult = self.validator.validate(self.resource_zr)
        self.assertEqual(zrResult, ZoneRedundancyValidationResult.Yes)

    def test_nonzr(self):
        # Test for non-zone redundancy scenario
        zrResult = self.validator.validate(self.resource_nonzr)
        self.assertEqual(zrResult, ZoneRedundancyValidationResult.No)
