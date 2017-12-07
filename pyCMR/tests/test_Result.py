'''
Copyright 2017, United States Government, as represented by the Administrator of the National Aeronautics and Space Administration. All rights reserved.

The pyCMR platform is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import os
import unittest
import xml.etree.ElementTree as ET

from ..pyCMR import CMR, Collection, Granule

class TestCMRResult(unittest.TestCase):
    def test_get_dl_url_is_not_none(self):
        """
        tests that cmr.searchGranule().getDownloadUrl() is not None
        https://github.com/nasa/pyCMR/issues/27

        NOTE: this uses an actual call to the API; might be better to mock it
        """
        cmr=CMR("cmr.cfg")
        results = cmr.searchGranule(
            limit=10,
            short_name="MOD09CMG",
            temporal="2010-02-01T10:00:00Z,2010-02-01T12:00:00Z"
        )

        self.assertEqual(2, len(results))

        for res in results:
            self.assertIsNotNone(res.getDownloadUrl())
