import os
import shutil
import asyncio
import unittest
from src.osm_osw_reformatter import Formatter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_DIR = 'test-directory'
EXISTING_DIR = 'existing_directory'


class TestFormatter(unittest.TestCase):

    def setUp(self):
        self.pbf_file_path = TEST_FILE

    def tearDown(self) -> None:
        is_exists = os.path.exists(TEST_DIR)
        if is_exists:
            shutil.rmtree(TEST_DIR)
        is_existing_dir = os.path.exists(EXISTING_DIR)
        if is_existing_dir:
            shutil.rmtree(EXISTING_DIR)

    def test_osm2osw_successful(self):
        pbf_file = self.pbf_file_path

        async def run_test():
            formatter = Formatter(pbf_file=pbf_file, workdir=OUTPUT_DIR)
            result = await formatter.osm2osw()
            self.assertTrue(result)

        asyncio.run(run_test())

    def test_osm2osw_error(self):
        pbf_file = 'test.pbf'

        async def run_test():
            formatter = Formatter(pbf_file=pbf_file, workdir=TEST_DIR)
            result = await formatter.osm2osw()
            self.assertFalse(result)

        asyncio.run(run_test())

    def test_workdir_creation(self):
        formatter = Formatter(workdir=TEST_DIR, pbf_file='test.pbf')
        self.assertTrue(os.path.exists(TEST_DIR))

    def test_workdir_already_exists(self):
        workdir = EXISTING_DIR
        os.makedirs(workdir)
        formatter = Formatter(workdir=workdir, pbf_file='test.pbf')
        self.assertTrue(os.path.exists(workdir))


if __name__ == '__main__':
    unittest.main()
