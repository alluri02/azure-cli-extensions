# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from azure.cli.testsdk import (ScenarioTest, JMESPathCheck, ResourceGroupPreparer,
                               api_version_constraint, live_only)

from .frontdoor_test_util import WafScenarioMixin
from knack.cli import CLIError
from azure.core.exceptions import (HttpResponseError)


class WafTests(WafScenarioMixin, ScenarioTest):
    # @live_only()  # --defer seems not work with VCR.py well
    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_captcha(self, resource_group):
        blockpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {blockpolicy} --captcha-expiration-in-minutes 5 --mode prevention --sku Premium_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['captchaExpirationInMinutes'], 5)
        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --captcha-expiration-in-minutes 12'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['policySettings']['captchaExpirationInMinutes'], 12)

    @live_only()  # --defer seems not work with VCR.py well
    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_log_scrubbing(self, resource_group):
        blockpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {blockpolicy} --mode prevention --sku Standard_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        options = '--log-scrubbing \"{{scrubbing-rules:[{{match-variable:QueryStringArgNames,selector-match-operator:EqualsAny}}],state:Enabled}}\"'
        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy}'.format(**locals())
        result = self.cmd(cmd + ' ' + options).get_output_in_json()
        self.assertEqual(result['policySettings']['scrubbingRules'][0]['state'], "Enabled")

    @live_only()  # --defer seems not work with VCR.py well
    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_policy_basic(self, resource_group):
        # multi-line comment below
        """
    az network front-door waf-policy create --resource-group {resource_group} --name {policyName}
az network front-door waf-policy create -g {resource_group} -n {policyName}
az network front-door waf-policy create -g {resource_group} -n {policyName} [--mode {mode}]
az network front-door waf-policy create -g {resource_group} -n {policyName} [--mode {mode}] [--redirect-url {url}]
az network front-door waf-policy create -g {resource_group} -n {policyName} [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}]
az network front-door waf-policy create -g {resource_group} -n {policyName} [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}] [--custom-block-response-body {body}]
az network front-door waf-policy create -g {resource_group} -n {policyName} [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}] [--custom-block-response-body {body}]  [--disabled]

az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best
az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best  [--mode {mode}]
az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best  [--mode {mode}] [--redirect-url {url}]
az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best  [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}]
az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best  [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}] [--custom-block-response-body {body}]
az network front-door waf-policy update -g {resource_group} -n {policyName} --tags test=best  [--mode {mode}] [--redirect-url {url}] [--custom-block-response-status-code {status code}] [--custom-block-response-body {body}]  [--disabled]
az network front-door waf-policy show -g {resource_group} -n {policyName}
az network front-door waf-policy list -g {resource_group}
az network front-door waf-policy delete -g {resource_group} -n {policyName}
"""
        subscription = self.current_subscription()
        blockpolicy = self.create_random_name(prefix='cli', length=24)
        ruleName = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {blockpolicy} --mode prevention'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        standardskupolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {standardskupolicy} --mode prevention --sku Standard_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], standardskupolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Standard_AzureFrontDoor")

        detectionredirectpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {detectionredirectpolicy} --mode Detection --redirect-url http://www.microsoft.com --sku Premium_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], detectionredirectpolicy)
        self.assertEqual(result['policySettings']['mode'], "Detection")
        self.assertEqual(result['policySettings']['redirectUrl'], "http://www.microsoft.com")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Premium_AzureFrontDoor")

        detectioncbcpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {detectioncbcpolicy} --mode Detection --redirect-url http://www.microsoft.com --custom-block-response-status-code 406 --sku Classic_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], detectioncbcpolicy)
        self.assertEqual(result['policySettings']['mode'], "Detection")
        self.assertEqual(result['policySettings']['redirectUrl'], "http://www.microsoft.com")
        self.assertEqual(result['policySettings']['customBlockResponseStatusCode'], 406)
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        detectioncbbpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {detectioncbbpolicy} --mode Detection --redirect-url http://www.microsoft.com --custom-block-response-status-code 406 --custom-block-response-body YiBvZHk='.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], detectioncbbpolicy)
        self.assertEqual(result['policySettings']['mode'], "Detection")
        self.assertEqual(result['policySettings']['enabledState'], "Enabled")
        self.assertEqual(result['policySettings']['redirectUrl'], "http://www.microsoft.com")
        self.assertEqual(result['policySettings']['customBlockResponseStatusCode'], 406)
        self.assertEqual(result['policySettings']['customBlockResponseBody'], "YiBvZHk=")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        detectiondisabledpolicy = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {detectiondisabledpolicy} --mode Detection --disabled'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], detectiondisabledpolicy)
        self.assertEqual(result['policySettings']['mode'], "Detection")
        self.assertEqual(result['policySettings']['enabledState'], "Disabled")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {detectiondisabledpolicy} --mode Detection'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['policySettings']['enabledState'], "Enabled")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --tags test=best'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        # TODO uncomment once API support for updating tags is fixed :-O
        # self.assertEqual(result['tags'], { 'test': 'best' })
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --mode detection --sku Classic_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Detection")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --mode prevention --redirect-url http://www.microsoft.com'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['redirectUrl'], 'http://www.microsoft.com')
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --custom-block-response-status-code 406'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['customBlockResponseStatusCode'], 406)
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --custom-block-response-status-code 405 --custom-block-response-body YiBvZHk='.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['customBlockResponseStatusCode'], 405)
        self.assertEqual(result['policySettings']['customBlockResponseBody'], "YiBvZHk=")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy update -g {resource_group} -n {blockpolicy} --disabled'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        self.assertEqual(result['policySettings']['enabledState'], "Disabled")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy show -g {resource_group} -n {blockpolicy}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], blockpolicy)
        # spot check
        self.assertEqual(result['policySettings']['enabledState'], "Disabled")
        self.assertEqual(result['policySettings']['customBlockResponseStatusCode'], 405)
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy list -g {resource_group}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 6)
        blockPolicyObject = [policy for policy in result if policy['name'] == blockpolicy][0]
        self.assertEqual(blockPolicyObject['name'], blockpolicy)

        cmd = 'az network front-door waf-policy delete -g {resource_group} -n {blockpolicy}'.format(**locals())
        result = self.cmd(cmd)

        cmd = 'az network front-door waf-policy list -g {resource_group}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 5)
        self.assertEqual(len([policy for policy in result if policy['name'] == blockpolicy]), 0)

    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_policy_custom_rule_matching(self, resource_group):
        # multi-line comment below
        """
Example command sequence:
az network front-door waf-policy create --resource-group {resource_group} --name {policyName}
az network front-door waf-policy rule create  -g {resource_group} --policy-name {policyName} -n {ruleName} --priority 6 --rule-type MatchRule --action Block --match-variable RequestBody --operator RegEx --values "something"
az network front-door create  --resource-group {resource_group} --backend-address www.example.com --name {frontdoorName}
# wait two minutes
az network front-door update --name {frontdoorName}--resource-group {resource_group} --set "FrontendEndpoints[0].WebApplicationFirewallPolicyLink.id=/subscriptions/{subscriptionId}/resourcegroups/{resource_group}/providers/Microsoft.Network/frontdoorwebapplicationfirewallpolicies/{policyName}"
"""

        subscription = self.current_subscription()
        policyName = self.create_random_name(prefix='cli', length=24)
        ruleName = self.create_random_name(prefix='cli', length=24)
        frontdoorName = self.create_random_name(prefix='cli', length=24)

        cmd = 'az network front-door waf-policy create --resource-group {resource_group} --name {policyName} --sku Classic_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        cmd = 'az network front-door waf-policy rule create  -g {resource_group} --policy-name {policyName} -n {ruleName} --priority 6 --rule-type MatchRule --action Block --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertIn('customRules', result)

        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {ruleName} --match-variable RequestBody --operator RegEx --values "something"'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][0]['matchConditions'][0]['matchValue'][0], "something")

        cmd = 'az network front-door create  --resource-group {resource_group} --backend-address www.example.com --name {frontdoorName}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertIn('frontendEndpoints', result)
        hostName = result['frontendEndpoints'][0]['hostName']
        self.assertTrue(hostName is not None)

        wafId = '/subscriptions/{subscription}/resourcegroups/{resource_group}/providers/Microsoft.Network/frontdoorwebapplicationfirewallpolicies/{policyName}'.format(**locals())
        cmd = 'az network front-door update --name {frontdoorName} --resource-group {resource_group} --set "FrontendEndpoints[0].WebApplicationFirewallPolicyLink.id={wafId}"'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertIn('frontendEndpoints', result)
        self.assertEqual(result['frontendEndpoints'][0]['hostName'], hostName)
        self.assertEqual(result['frontendEndpoints'][0]['webApplicationFirewallPolicyLink']['id'], wafId)

        if self.is_live:
            import requests

            import time
            elapsed_seconds = 0
            while elapsed_seconds < 900:
                r = requests.post('http://{hostName}/'.format(**locals()), data="'key':'something'")
                if(r.status_code == 403):
                    break
                time.sleep(10)
                elapsed_seconds += 10
            self.assertEqual(r.status_code, 403)

    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_policy_managed_rules(self, resource_group):
        # multi-line comment below
        """
Example command sequence:
az network front-door waf-policy managed-rules add -g {resource_group} --policy-name {policyName} --type {type} --version {version}
az network front-door waf-policy managed-rules override add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid} [--action {action}] [--disabled]
az network front-door waf-policy managed-rules override remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid}
az network front-door waf-policy managed-rules list -g {resource_group} --policy-name {policyName}
az network front-door waf-policy managed-rules remove -g {resource_group} --policy-name {policyName} --type {type}
az network front-door waf-policy managed-rule-definition list
"""
        subscription = self.current_subscription()
        policyName = self.create_random_name(prefix='cli', length=24)
        ruleName = self.create_random_name(prefix='cli', length=24)
        frontdoorName = self.create_random_name(prefix='cli', length=24)

        cmd = 'az network front-door waf-policy create --resource-group {resource_group} --name {policyName} --sku Premium_AzureFrontDoor'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertEqual(result['sku']['name'], "Premium_AzureFrontDoor")

        type = "DefaultRuleSet"
        version = "1.0"
        cmd = 'az network front-door waf-policy managed-rules add -g {resource_group} --policy-name {policyName} --type {type} --version {version}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertIn('managedRules', result)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleSetType'], type)

        rulegroupid = "SQLI"
        ruleid = "942100"
        action = "Block"
        cmd = 'az network front-door waf-policy managed-rules override add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid} --action {action} --disabled'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["ruleGroupName"], rulegroupid)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["rules"][0]["ruleId"], ruleid)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["rules"][0]["action"], action)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["rules"][0]["enabledState"], "Disabled")

        cmd = 'az network front-door waf-policy managed-rules override remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides']), 0)

        cmd = 'az network front-door waf-policy managed-rules list -g {resource_group} --policy-name {policyName}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['ruleSetType'], type)

        cmd = 'az network front-door waf-policy managed-rules remove -g {resource_group} --policy-name {policyName} --type {type}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertIn('managedRules', result)
        self.assertEqual(len(result['managedRules']['managedRuleSets']), 0)

        type = "Microsoft_DefaultRuleSet"
        version = "2.0"
        action = "Block"
        cmd = 'az network front-door waf-policy managed-rules add -g {resource_group} --policy-name {policyName} --type {type} --version {version} --action {action}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertIn('managedRules', result)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleSetType'], type)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleSetVersion'], version)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleSetAction'], action)


    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    @live_only()  # --defer seems not work with VCR.py well
    def test_waf_policy_custom_rules(self, resource_group):
        # multi-line comment below
        """
Example command sequence:
az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {rateLimit} --priority 10 --action log --rule-type ratelimitrule --rate-limit-duration 5 --rate-limit-threshold 10000 --defer
az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {badRateLimit} --priority 20 --action log --rule-type ratelimitrule --rate-limit-threshold 10000 --defer <-- should error
az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --priority 30 --action log --rule-type ratelimitrule --disabled --rate-limit-duration 1 --rate-limit-threshold 10000 --defer
az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {match} --priority 40 --action log --rule-type matchrule --defer
az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {rateLimit} [--priority 45] [--action log] [--rate-limit-duration 5] [--rate-limit-threshold 10000]
az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} [--priority 75] [--disabled] [--rate-limit-duration 5]
az network front-door waf-policy rule delete -g {resource_group} --policy-name {policyName} -n {disabledRateLimit}
az network front-door waf-policy rule show -g {resource_group} --policy-name {policyName} -n {rateLimit}
az network front-door waf-policy rule list -g {resource_group} --policy-name {policyName}
az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {rateLimit} --match-variable RequestHeaders.value --operator Contains --values foo boo
az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {rateLimit} --match-variable RequestHeaders --operator Contains --values foo boo <-- expect error, no selector
az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {match} --match-variable RequestUri --operator Contains --values foo boo [--negate]
az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {match} --match-variable RequestHeaders.value --operator Contains --values foo boo [--negate] [--transforms Lowercase UrlDecode]
az network front-door waf-policy rule match-condition remove -g {resource_group} --policy-name {policyName} -n {match} --index 1
az network front-door waf-policy rule match-condition list -g {resource_group} --policy-name {policyName} -n {match}
"""

        subscription = self.current_subscription()
        policyName = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {policyName} --mode prevention'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        self.assertEqual(result['sku']['name'], "Classic_AzureFrontDoor")

        rateLimit = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {rateLimit} --priority 10 --action log --rule-type ratelimitrule --rate-limit-duration 5 --rate-limit-threshold 10000 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][0]['rateLimitDurationInMinutes'], 5)
        self.assertEqual(result['customRules']['rules'][0]['rateLimitThreshold'], 10000)

        badRateLimit = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {badRateLimit} --priority 20 --action log --rule-type ratelimitrule --rate-limit-threshold 10000 --defer'.format(**locals())
        try:
            result = self.cmd(cmd)
            self.fail("should throw exception")
        except CLIError as e:
            self.assertEqual(str(e), "rate_limit_duration and rate_limit_threshold are required for a RateLimitRule")

        disabledRateLimit = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --priority 30 --action log --rule-type ratelimitrule --disabled --rate-limit-duration 1 --rate-limit-threshold 10000 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][1]['enabledState'], "Disabled")

        match = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy rule create -g {resource_group} --policy-name {policyName} -n {match} --priority 40 --action log --rule-type matchrule --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][2]['ruleType'], "MatchRule")

        cmd = 'az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {rateLimit} --priority 45 --action block --rate-limit-duration 5 --rate-limit-threshold 10000 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][0]['priority'], 45)
        self.assertEqual(result['customRules']['rules'][0]['action'], "Block")

        cmd = 'az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --priority 75 --disabled --rate-limit-duration 5 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][1]['priority'], 75)
        self.assertEqual(result['customRules']['rules'][1]['rateLimitDurationInMinutes'], 1)
        self.assertEqual(result['customRules']['rules'][1]['enabledState'], 'Disabled')

        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {rateLimit} --match-variable RequestHeader.value --operator Contains --values foo boo --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][0]['matchConditions'][0]['matchVariable'], 'RequestHeader')
        self.assertEqual(result['customRules']['rules'][0]['matchConditions'][0]['selector'], 'value')
        self.assertEqual(result['customRules']['rules'][0]['matchConditions'][0]['matchValue'][0], 'foo')
        self.assertEqual(result['customRules']['rules'][0]['matchConditions'][0]['matchValue'][1], 'boo')

        # Note that this causes 'Selector must be set when using RequestHeader match variable' when we submit the policy to the back-end
        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {rateLimit} --match-variable RequestHeader --operator Contains --values foo boo --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --match-variable RequestUri --operator Contains --values foo boo --negate --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][1]['matchConditions'][0]['matchVariable'], 'RequestUri')
        self.assertEqual(result['customRules']['rules'][1]['matchConditions'][0]['selector'], None)
        self.assertEqual(result['customRules']['rules'][1]['matchConditions'][0]['negateCondition'], True)
        self.assertEqual(result['customRules']['rules'][1]['matchConditions'][0]['matchValue'][0], 'foo')
        self.assertEqual(result['customRules']['rules'][1]['matchConditions'][0]['matchValue'][1], 'boo')

        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {match} --match-variable RequestUri --operator Contains --values foo boo --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][0]['matchVariable'], 'RequestUri')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][0]['selector'], None)
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][0]['negateCondition'], None)
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][0]['matchValue'][0], 'foo')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][0]['matchValue'][1], 'boo')

        cmd = 'az network front-door waf-policy rule match-condition add -g {resource_group} --policy-name {policyName} -n {match} --match-variable RequestHeader.value --operator Contains --values foo boo --transforms Lowercase UrlDecode --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['matchVariable'], 'RequestHeader')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['selector'], 'value')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['matchValue'][0], 'foo')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['matchValue'][1], 'boo')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['transforms'][0], 'Lowercase')
        self.assertEqual(result['customRules']['rules'][2]['matchConditions'][1]['transforms'][1], 'UrlDecode')

        cmd = 'az network front-door waf-policy rule match-condition remove -g {resource_group} --policy-name {policyName} -n {match} --index 1 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result['customRules']['rules'][2]['matchConditions']), 1)

        cmd = 'az network front-door waf-policy rule match-condition list -g {resource_group} --policy-name {policyName} -n {match} --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 1)

        # complete updates on all deferred policies
        try:
            cmd = 'az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --priority 75'.format(**locals())
            result = self.cmd(cmd)
            self.fail()
        except HttpResponseError as e:
            # fails because of missing selector on RequestHeader
            self.assertTrue(e.status_code == 400)

        # delete problematic match condition
        cmd = 'az network front-door waf-policy rule match-condition remove -g {resource_group} --policy-name {policyName} -n {rateLimit} --index 1 --defer'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()

        # complete updates on all deferred policies
        cmd = 'az network front-door waf-policy rule update -g {resource_group} --policy-name {policyName} -n {disabledRateLimit} --priority 75'.format(**locals())
        result = self.cmd(cmd)

        cmd = 'az network front-door waf-policy rule list -g {resource_group} --policy-name {policyName}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 3)

        cmd = 'az network front-door waf-policy rule delete -g {resource_group} --policy-name {policyName} -n {disabledRateLimit}'.format(**locals())
        result = self.cmd(cmd)

        cmd = 'az network front-door waf-policy rule show -g {resource_group} --policy-name {policyName} -n {rateLimit}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], rateLimit)
        self.assertEqual(result['priority'], 45)
        self.assertEqual(result['action'], "Block")
        self.assertEqual(result['rateLimitDurationInMinutes'], 5)

        cmd = 'az network front-door waf-policy rule list -g {resource_group} --policy-name {policyName}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 2)

    @ResourceGroupPreparer(location='westus', additional_tags={'owner': 'jingnanxu'})
    def test_waf_exclusions(self, resource_group):
        # multi-line comment below
        """
  az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type}
  az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group}
  az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group} --rule-id {ruleid} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group} --rule-id {ruleid} --match-variable {match_variable} --operator {operator} --value {value}
  az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rule_group} --rule-id {ruleid}
"""
        subscription = self.current_subscription()
        policyName = self.create_random_name(prefix='cli', length=24)
        cmd = 'az network front-door waf-policy create -g {resource_group} -n {policyName} --mode prevention'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(result['name'], policyName)
        self.assertEqual(result['policySettings']['mode'], "Prevention")
        self.assertEqual(result['policySettings']['requestBodyCheck'], "Enabled")
        self.assertIn('customRules', result)
        self.assertIn('managedRules', result)
        self.assertIn('id', result)
        self.assertEqual(result['sku']['name'], "Premium_AzureFrontDoor")

        type = "DefaultRuleSet"
        version = "1.0"
        cmd = 'az network front-door waf-policy managed-rules add -g {resource_group} --policy-name {policyName} --type {type} --version {version}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertIn('managedRules', result)
        self.assertEqual(result['managedRules']['managedRuleSets'][0]['ruleSetType'], type)

        matchVariable = "RequestHeaderNames"
        op = "Contains"
        selector = "ignoreme"

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 0)

        cmd = 'az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result['managedRules']['managedRuleSets'][0]['exclusions']
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)
        exclusions = None

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result
        self.assertEqual(len(exclusions), 1)
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)

        cmd = 'az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result['managedRules']['managedRuleSets'][0]['exclusions']
        self.assertEqual(len(exclusions), 0)

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        self.assertEqual(len(result), 0)

        rulegroupid = "SQLI"
        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid}'.format(**locals())
        try:
            result = self.cmd(cmd)
            self.fail("should throw exception")
        except CLIError as e:
            self.assertEqual(str(e), "rule group 'SQLI' not found")

        cmd = 'az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        ruleGroupOverride = result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]
        self.assertEqual(rulegroupid, ruleGroupOverride["ruleGroupName"])
        exclusions = ruleGroupOverride['exclusions']
        self.assertEqual(len(exclusions), 1)
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result
        self.assertEqual(len(exclusions), 1)
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)

        cmd = 'az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        ruleGroupOverride = result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]
        self.assertEqual(ruleGroupOverride["ruleGroupName"], rulegroupid)
        exclusions = ruleGroupOverride['exclusions']
        self.assertEqual(len(exclusions), 0)

        ruleid = "942100"
        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid} '.format(**locals())
        try:
            result = self.cmd(cmd)
            self.fail("should throw exception")
        except CLIError as e:
            self.assertEqual(str(e), "rule '942100' not found")

        cmd = 'az network front-door waf-policy managed-rules exclusion add -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid}  --rule-id {ruleid} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        ruleOverride = result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["rules"][0]
        self.assertEqual(ruleOverride["ruleId"], ruleid)
        exclusions = ruleOverride['exclusions']
        self.assertEqual(len(exclusions), 1)
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid} '.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result
        self.assertEqual(len(exclusions), 1)
        self.assertEqual(exclusions[0]["matchVariable"], matchVariable)
        self.assertEqual(exclusions[0]["selectorMatchOperator"], op)
        self.assertEqual(exclusions[0]["selector"], selector)

        cmd = 'az network front-door waf-policy managed-rules exclusion remove -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid}  --rule-id {ruleid} --match-variable {matchVariable} --operator {op} --value {selector}'.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        ruleOverride = result['managedRules']['managedRuleSets'][0]['ruleGroupOverrides'][0]["rules"][0]
        self.assertEqual(ruleOverride["ruleId"], ruleid)
        exclusions = ruleOverride['exclusions']
        self.assertEqual(len(exclusions), 0)

        cmd = 'az network front-door waf-policy managed-rules exclusion list -g {resource_group} --policy-name {policyName} --type {type} --rule-group-id {rulegroupid} --rule-id {ruleid} '.format(**locals())
        result = self.cmd(cmd).get_output_in_json()
        exclusions = result
        self.assertEqual(len(exclusions), 0)
