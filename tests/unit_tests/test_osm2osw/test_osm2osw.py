import os
import asyncio
import unittest
from unittest.mock import AsyncMock
from src.osm_osw_reformatter.osm2osw.osm2osw import OSM2OSW

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')


class TestOSM2OSW(unittest.IsolatedAsyncioTestCase):
    def test_convert_successful(self):
        pbf_path = TEST_FILE

        async def run_test():
            osm2osw = OSM2OSW(pbf_file=pbf_path, workdir=OUTPUT_DIR)
            result = await osm2osw.convert()
            self.assertTrue(result)

        asyncio.run(run_test())

    async def test_convert_error(self):
        async def mock_count_entities_error(pbf_path, counter_cls):
            raise Exception("Error in counting entities")

        o2o = OSM2OSW(pbf_file='test.pbf', workdir='work_dir')

        result = await o2o.convert()

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
