import os
import re
import asyncio
import unittest
from src.osm_osw_reformatter.osm2osw.osm2osw import OSM2OSW

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')


class TestOSM2OSW(unittest.IsolatedAsyncioTestCase):
    def test_convert_successful(self):
        osm_file_path = TEST_FILE

        async def run_test():
            osm2osw = OSM2OSW(osm_file=osm_file_path, workdir=OUTPUT_DIR, prefix='test')
            result = await osm2osw.convert()
            self.assertTrue(result.status)
            for file in result.generated_files:
                os.remove(file)

        asyncio.run(run_test())

    def test_generated_3_files(self):
        osm_file_path = TEST_FILE

        async def run_test():
            osm2osw = OSM2OSW(osm_file=osm_file_path, workdir=OUTPUT_DIR, prefix='test')
            result = await osm2osw.convert()
            self.assertEqual(len(result.generated_files), 6)
            for file in result.generated_files:
                os.remove(file)

        asyncio.run(run_test())

    def test_generated_files_include_nodes_points_edges(self):
        osm_file_path = TEST_FILE

        async def run_test():
            osm2osw = OSM2OSW(osm_file=osm_file_path, workdir=OUTPUT_DIR, prefix='test')
            result = await osm2osw.convert()
            for file_path in result.generated_files:
                self.assertTrue(re.search(r'(nodes|points|edges|zones|polygons|lines)', file_path))
            for file_path in result.generated_files:
                os.remove(file_path)

        asyncio.run(run_test())

    def test_generated_files_are_string(self):
        osm_file_path = TEST_FILE

        async def run_test():
            osm2osw = OSM2OSW(osm_file=osm_file_path, workdir=OUTPUT_DIR, prefix='test')
            result = await osm2osw.convert()
            for file_path in result.generated_files:
                self.assertIsInstance(file_path, str)
            for file_path in result.generated_files:
                os.remove(file_path)

        asyncio.run(run_test())

    async def test_convert_error(self):
        async def mock_count_entities_error(osm_file_path, counter_cls):
            raise Exception("Error in counting entities")

        osm2osw = OSM2OSW(osm_file='test.pbf', workdir='work_dir', prefix='test')

        result = await osm2osw.convert()
        self.assertFalse(result.status)


if __name__ == '__main__':
    unittest.main()
