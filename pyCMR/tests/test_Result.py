'''
Copyright 2017, United States Government, as represented by the Administrator of the National Aeronautics and Space Administration. All rights reserved.

The pyCMR platform is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import os
import unittest
import xml.etree.ElementTree as ET

from ..pyCMR import CMR

mock_response_file_2hit = "pyCMR/tests/mock_responses/granules_2-hits.xml"

class TestCMRResult(unittest.TestCase):

    def test_results_len_on_2hit_mock_response(self):
        """
        tests CMR._parse_search_response returns list of len 2 using a pregen
        mock xml response with 2 hits.
        """
        with open(mock_response_file_2hit) as mock_response:
            results, empty_page_flag = CMR._parse_search_response(mock_response.read())
            print(results)
            self.assertEqual(len(results), 2)

    def test_get_dl_url_is_not_none(self):
        """
        tests that cmr.searchGranule().getDownloadUrl() is not None
        https://github.com/nasa/pyCMR/issues/27
        """
        with open(mock_response_file_2hit) as mock_response:
            results, empty_page_flag = CMR._parse_search_response(mock_response.read())

            for res in results:
                self.assertIsNotNone(res.getDownloadUrl())
