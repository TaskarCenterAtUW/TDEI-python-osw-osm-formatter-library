import os
import unittest
from src.osm_osw_reformatter.osw2osm.osw2osm import OSW2OSM

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_ZIP_FILE = os.path.join(ROOT_DIR, 'test_files/osw.zip')


class TestOSW2OSM(unittest.IsolatedAsyncioTestCase):
    def test_convert_successful(self):
        zip_file = TEST_ZIP_FILE
        osw2osm = OSW2OSM(zip_file_path=zip_file, workdir=OUTPUT_DIR, prefix='test')
        result = osw2osm.convert()
        self.assertTrue(result.status)
        os.remove(result.generated_files)

    def test_generated_file(self):
        zip_file = TEST_ZIP_FILE
        osw2osm = OSW2OSM(zip_file_path=zip_file, workdir=OUTPUT_DIR, prefix='test')
        result = osw2osm.convert()
        self.assertEqual(len([result.generated_files]), 1)
        os.remove(result.generated_files)

    def test_generated_file_should_be_xml(self):
        zip_file = TEST_ZIP_FILE
        osw2osm = OSW2OSM(zip_file_path=zip_file, workdir=OUTPUT_DIR, prefix='test')
        result = osw2osm.convert()
        self.assertTrue(result.generated_files.endswith('.xml'))
        os.remove(result.generated_files)

    def test_convert_generated_files_are_string(self):
        zip_file = TEST_ZIP_FILE
        osw2osm = OSW2OSM(zip_file_path=zip_file, workdir=OUTPUT_DIR, prefix='test')
        result = osw2osm.convert()
        self.assertIsInstance(result.generated_files, str)
        os.remove(result.generated_files)

    async def test_convert_error(self):
        osw2osm = OSW2OSM(zip_file_path='test.zip', workdir=OUTPUT_DIR, prefix='test')
        result = osw2osm.convert()
        self.assertFalse(result.status)


if __name__ == '__main__':
    unittest.main()
