'''
Copyright 2017, United States Government, as represented by the Administrator of the National Aeronautics and Space Administration. All rights reserved.

The pyCMR platform is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import unittest
from datetime import datetime, timedelta

from ..pyCMR import CMR

mock_response_file_2hit = "pyCMR/tests/mock_responses/granules_2-hits.xml"

class IntegrationTests(unittest.TestCase):

    def test_temporal_query(self):
        """
        should get at least one granule for MODIS Aqua granule from LANCE
        at time range 2017-12-04T19:15:01,2017-12-04T19:19:59
        """
        exec_datetime = datetime(2017, 12, 4, 19, 15)
        TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"  # iso 8601
        cmr = CMR("cmr.cfg")
        time_range = str(
            (exec_datetime + timedelta(           seconds=1 )).strftime(TIME_FMT) + ',' +
            (exec_datetime + timedelta(minutes=4, seconds=59)).strftime(TIME_FMT)
        )
        print(time_range)
        results = cmr.searchGranule(
            limit=10,
            short_name="MYD01",  # [M]odis (Y)aqua (D) (0) level [1]
            # collection_data_type="NRT",  # this is not available for granules
            provider="LANCEMODIS",  # lance modis is hopefullly only serving NRT
            temporal=time_range
        )
        print(results)
        self.assertTrue(len(results) > 0)
