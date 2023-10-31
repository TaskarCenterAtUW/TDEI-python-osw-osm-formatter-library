import os
import asyncio
import unittest
from src.osm_osw_reformatter.helpers.osw import OSWHelper
from src.osm_osw_reformatter.serializer.osm.osm_graph import OSMGraph
from src.osm_osw_reformatter.serializer.counters import WayCounter, PointCounter, NodeCounter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'output')
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')


class TestOSWHelper(unittest.TestCase):
    def setUp(self):
        self.pbf_file_path = TEST_FILE
        is_exists = os.path.exists(OUTPUT_DIR)
        if not is_exists:
            os.makedirs(OUTPUT_DIR)

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
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_ways(pbf_path)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_nodes(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_nodes(pbf_path)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_count_points(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_points(pbf_path)
            self.assertEqual(result, 0)

        asyncio.run(run_test())

    def test_count_entities_with_ways_counter(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_entities(pbf_path, WayCounter)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_entities_with_points_counter(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_entities(pbf_path, PointCounter)
            self.assertEqual(result, 0)

        asyncio.run(run_test())

    def test_count_entities_with_nodes_counter(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.count_entities(pbf_path, NodeCounter)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_get_osm_graph(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(pbf_path)
            self.assertIsInstance(result, OSMGraph)

        asyncio.run(run_test())

    def test_simplify_og(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(pbf_path)
            self.assertIsInstance(result, OSMGraph)
            simplify_og_result = await OSWHelper.simplify_og(result)
            self.assertIsNone(simplify_og_result)

        asyncio.run(run_test())

    def test_construct_geometries(self):
        pbf_path = self.pbf_file_path

        async def run_test():
            result = await OSWHelper.get_osm_graph(pbf_path)
            self.assertIsInstance(result, OSMGraph)
            construct_geometries_result = await OSWHelper.construct_geometries(result)
            self.assertIsNone(construct_geometries_result)

        asyncio.run(run_test())
