# coding=utf-8
# COPYRIGHT 2014 Rackspace
#
# Author: Tim Simmons <tim.simmons@rackspace.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo.config import cfg

from designate.tests.test_api.test_v2 import ApiV2TestCase

cfg.CONF.import_opt('enabled_extensions_v2', 'designate.api.v2',
                    group='service:api')


class ApiV2QuotasTest(ApiV2TestCase):
    def setUp(self):
        self.config(enabled_extensions_v2=['quotas'], group='service:api')
        super(ApiV2QuotasTest, self).setUp()

    def test_get_quotas(self):
        self.policy({'get_quotas': '@'})
        context = self.get_admin_context()

        response = self.client.get('/quotas/%s' % context.tenant,
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        self.assertEqual(200, response.status_int)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('quota', response.json)
        self.assertIn('zones', response.json['quota'])
        self.assertIn('zone_records', response.json['quota'])
        self.assertIn('zone_recordsets', response.json['quota'])
        self.assertIn('recordset_records', response.json['quota'])

        max_zones = response.json['quota']['zones']
        max_zone_records = response.json['quota']['zone_records']
        self.assertEqual(cfg.CONF.quota_domains, max_zones)
        self.assertEqual(cfg.CONF.quota_domain_records, max_zone_records)

    def test_patch_quotas(self):
        self.policy({'set_quotas': '@'})
        context = self.get_context(tenant='a', is_admin=True)

        response = self.client.get('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        self.assertEqual(200, response.status_int)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('quota', response.json)
        self.assertIn('zones', response.json['quota'])
        current_count = response.json['quota']['zones']

        body = {'quota': {"zones": 1337}}
        response = self.client.patch_json('/quotas/%s' % 'a', body,
                                          status=200,
                                          headers={'X-Test-Tenant-Id':
                                          context.tenant})
        self.assertEqual(200, response.status_int)

        response = self.client.get('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        new_count = response.json['quota']['zones']

        self.assertNotEqual(current_count, new_count)

    def test_reset_quotas(self):
        self.policy({'reset_quotas': '@'})
        context = self.get_context(tenant='a', is_admin=True)

        response = self.client.get('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        self.assertEqual(200, response.status_int)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('quota', response.json)
        self.assertIn('zones', response.json['quota'])
        current_count = response.json['quota']['zones']

        body = {'quota': {"zones": 1337}}
        response = self.client.patch_json('/quotas/%s' % 'a', body,
                                          status=200,
                                          headers={'X-Test-Tenant-Id':
                                          context.tenant})
        self.assertEqual(200, response.status_int)

        response = self.client.get('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        new_count = response.json['quota']['zones']

        self.assertNotEqual(current_count, new_count)

        response = self.client.delete('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant}, status=204)
        response = self.client.get('/quotas/%s' % 'a',
                                   headers={'X-Test-Tenant-Id':
                                   context.tenant})

        newest_count = response.json['quota']['zones']
        self.assertNotEqual(new_count, newest_count)
        self.assertEqual(current_count, newest_count)
