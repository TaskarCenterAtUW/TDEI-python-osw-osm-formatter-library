import os
import shutil
import asyncio
import unittest
from src.osm_osw_reformatter import Formatter
from src.osm_osw_reformatter.helpers.response import Response

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PBF_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')
TEST_OSW_FILE = os.path.join(ROOT_DIR, 'test_files/osw.zip')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_DIR = 'test-directory'
EXISTING_DIR = 'existing_directory'


class TestFormatter(unittest.TestCase):

    def setUp(self):
        self.osm_file_path = TEST_PBF_FILE
        self.osw_file_path = TEST_OSW_FILE
        self.existing_files = [f'{OUTPUT_DIR}/file1.txt', f'{OUTPUT_DIR}/file2.txt']
        self.non_existent_files = [f'{OUTPUT_DIR}/non_existent1.txt', f'{OUTPUT_DIR}/non_existent2.txt']
        for file in self.existing_files:
            with open(file, 'w') as f:
                f.write('Test data')

    def tearDown(self) -> None:
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        if os.path.exists(EXISTING_DIR):
            shutil.rmtree(EXISTING_DIR)
        for file in self.existing_files + self.non_existent_files:
            if os.path.exists(file):
                os.remove(file)

    def test_osm2osw_successful(self):
        osm_file = self.osm_file_path

        async def run_test():
            formatter = Formatter(file_path=osm_file, workdir=OUTPUT_DIR)
            result = await formatter.osm2osw()
            formatter.cleanup()
            self.assertTrue(result.status)

        asyncio.run(run_test())

    def test_osm2osw_error(self):
        osm_file = 'test.pbf'

        async def run_test():
            formatter = Formatter(file_path=osm_file, workdir=TEST_DIR)
            result = await formatter.osm2osw()
            self.assertFalse(result.status)

        asyncio.run(run_test())

    def test_workdir_creation(self):
        formatter = Formatter(workdir=TEST_DIR, file_path='test.pbf')
        self.assertTrue(os.path.exists(TEST_DIR))

    def test_workdir_already_exists(self):
        workdir = EXISTING_DIR
        os.makedirs(workdir)
        formatter = Formatter(workdir=workdir, file_path='test.pbf')
        self.assertTrue(os.path.exists(workdir))

    def test_cleanup_existing_files(self):
        formatter = Formatter(workdir=OUTPUT_DIR, file_path='test.pbf')
        response = Response(status=True, generated_files=self.existing_files)
        formatter.generated_files = response.generated_files

        # Verify that cleanup removes existing files
        self.assertTrue(os.path.exists(f'{OUTPUT_DIR}/file1.txt'))
        self.assertTrue(os.path.exists(f'{OUTPUT_DIR}/file2.txt'))
        formatter.cleanup()
        self.assertFalse(os.path.exists(f'{OUTPUT_DIR}/file1.txt'))
        self.assertFalse(os.path.exists(f'{OUTPUT_DIR}/file2.txt'))

    def test_cleanup_non_existent_files(self):
        formatter = Formatter(workdir=OUTPUT_DIR, file_path='test.pbf')
        # Simulate the generation of files
        response = Response(status=True,
                            generated_files=self.non_existent_files)
        formatter.generated_files = response.generated_files

        # Verify that cleanup handles non-existent files without errors
        formatter.cleanup()
        self.assertFalse(os.path.exists(f'{OUTPUT_DIR}/non_existent1.osm'))
        self.assertFalse(os.path.exists(f'{OUTPUT_DIR}/non_existent2.osm'))


if __name__ == '__main__':
    unittest.main()
