import os
import json
import zipfile
import asyncio
import unittest
from pathlib import Path
from src.osm_osw_reformatter.helpers.osw import OSWHelper
from src.osm_osw_reformatter.serializer.osm.osm_graph import OSMGraph
from src.osm_osw_reformatter.serializer.counters import WayCounter, PointCounter, NodeCounter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')
TEST_ZIP_FILE = os.path.join(ROOT_DIR, 'test_files/test.zip')


class TestOSWHelper(unittest.TestCase):
    def setUp(self):
        self.osm_file_path = TEST_FILE
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        if not os.path.exists(TEST_ZIP_FILE):
            with zipfile.ZipFile(TEST_ZIP_FILE, 'w') as zf:
                zf.writestr('nodes', 'Nodes content')
                zf.writestr('edges', 'Edges content')
                zf.writestr('points', 'Points content')
        self.geojson_files = {
            f'{OUTPUT_DIR}/file1.geojson': {
                'type': 'FeatureCollection',
                'features': [
                    {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [1, 2]}}]
            },
            f'{OUTPUT_DIR}/file2.geojson': {
                'type': 'FeatureCollection',
                'features': [
                    {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [3, 4]}}]
            }
        }
        for filename, data in self.geojson_files.items():
            with open(filename, 'w') as f:
                json.dump(data, f)

    def tearDown(self):
        if os.path.exists(TEST_ZIP_FILE):
            os.remove(TEST_ZIP_FILE)

        for filename in self.geojson_files.keys():
            if os.path.exists(filename):
                os.remove(filename)

    def test_osw_way_filter(self):
        tags = {'tag1': 'value1', 'tag2': 'value2'}
        result = OSWHelper.osw_way_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_osw_node_filter(self):
        tags = {'tag1': 'value1', 'tag2': 'value2'}
        result = OSWHelper.osw_node_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_osw_point_filter(self):
        tags = {'tag1': 'value1', 'tag2': 'value2'}
        result = OSWHelper.osw_point_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_count_ways(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_ways(osm_file_path)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_nodes(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_nodes(osm_file_path)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_count_points(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_points(osm_file_path)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_count_zones(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_zones(osm_file_path)
            self.assertEqual(result, 956)

        asyncio.run(run_test())

    def test_count_lines(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_lines(osm_file_path)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_polygons(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_polygons(osm_file_path)
            self.assertEqual(result, 956)

        asyncio.run(run_test())

    def test_count_entities_with_ways_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_entities(osm_file_path, WayCounter)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_entities_with_points_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_entities(osm_file_path, PointCounter)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_count_entities_with_nodes_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.count_entities(osm_file_path, NodeCounter)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_get_osm_graph(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)

        asyncio.run(run_test())

    def test_simplify_og(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)
            simplify_og_result = await OSWHelper.simplify_og(result)
            self.assertIsNone(simplify_og_result)

        asyncio.run(run_test())

    def test_construct_geometries(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)
            construct_geometries_result = await OSWHelper.construct_geometries(result)
            self.assertIsNone(construct_geometries_result)

        asyncio.run(run_test())

    def test_unzip(self):
        file_locations = OSWHelper.unzip(zip_file=TEST_ZIP_FILE, output=OUTPUT_DIR)
        self.assertTrue(os.path.exists(os.path.join(OUTPUT_DIR, 'nodes')))
        self.assertTrue(os.path.exists(os.path.join(OUTPUT_DIR, 'edges')))
        self.assertTrue(os.path.exists(os.path.join(OUTPUT_DIR, 'points')))
        self.assertEqual(len(file_locations), 3)
        self.assertEqual(file_locations['nodes'], os.path.join(OUTPUT_DIR, 'nodes'))
        self.assertEqual(file_locations['edges'], os.path.join(OUTPUT_DIR, 'edges'))
        self.assertEqual(file_locations['points'], os.path.join(OUTPUT_DIR, 'points'))
        os.remove(os.path.join(OUTPUT_DIR, 'nodes'))
        os.remove(os.path.join(OUTPUT_DIR, 'edges'))
        os.remove(os.path.join(OUTPUT_DIR, 'points'))

    def test_unzip_should_return_3_files(self):
        file_locations = OSWHelper.unzip(zip_file=TEST_ZIP_FILE, output=OUTPUT_DIR)
        self.assertEqual(len(file_locations), 3)
        os.remove(os.path.join(OUTPUT_DIR, 'nodes'))
        os.remove(os.path.join(OUTPUT_DIR, 'edges'))
        os.remove(os.path.join(OUTPUT_DIR, 'points'))

    def test_missing_files(self):
        zip_file_path = f'{OUTPUT_DIR}/test_missing_files.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zf:
            zf.writestr('other_file.txt', 'Other file content')

        file_locations = OSWHelper.unzip(zip_file=zip_file_path, output=OUTPUT_DIR)
        self.assertEqual(len(file_locations), 0)

        os.remove(f'{OUTPUT_DIR}/other_file.txt')
        os.remove(zip_file_path)

    def test_merge(self):
        osm_files = {file: file for file in self.geojson_files.keys()}
        output_path = OSWHelper.merge(osm_files=osm_files, output=OUTPUT_DIR, prefix='test')
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(Path(output_path).is_file())

    def test_cleanup_of_temp_files(self):
        osm_files = {file: file for file in self.geojson_files.keys()}
        output_path = OSWHelper.merge(osm_files=osm_files, output=OUTPUT_DIR, prefix='test')

        # Check if the temporary GeoJSON files have been removed
        for filename in self.geojson_files.keys():
            self.assertFalse(os.path.exists(filename))
