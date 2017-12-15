'''
A few little integration tests that make actual queries to the CMR.
These can fail b/c of network issues, changes to the CMR, or CMR downtime.
'''

import unittest
from datetime import datetime, timedelta

from ..pyCMR import CMR

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
            temporal=time_range
        )
        print(results)
        self.assertTrue(len(results) > 0)

    def test_download(self):
        """
        download one granule for MODIS Aqua granule from LANCE
        this assumes that three-day-old data will be available
        """
        exec_datetime = datetime.now() - timedelta(days=3)
        TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"  # iso 8601
        cmr = CMR("cmr.cfg")
        time_range = str(
            (exec_datetime                      ).strftime(TIME_FMT) + ',' +
            (exec_datetime + timedelta(hours=1)).strftime(TIME_FMT)
        )
        print(time_range)
        results = cmr.searchGranule(
            limit=10,
            short_name="MYD01",  # [M]odis (Y)aqua (D) (0) level [1]
            # collection_data_type="NRT",  # this is not available for granules
            temporal=time_range,
            downloadable='true'
        )
        results[0].download()
