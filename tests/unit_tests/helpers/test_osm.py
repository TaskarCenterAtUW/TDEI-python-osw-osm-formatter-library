import os
import asyncio
import unittest
from src.osm_osw_reformatter.serializer.osm.osm_graph import OSMGraph
from src.osm_osw_reformatter.serializer.counters import WayCounter, PointCounter, NodeCounter
from src.osm_osw_reformatter.helpers.osm import count_entities, get_osm_graph, osw_way_filter, osw_node_filter, \
    osw_point_filter, simplify_og, construct_geometries

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_FILE = os.path.join(ROOT_DIR, 'test_files/wa.microsoft.osm.pbf')


class TestOSMHelper(unittest.TestCase):

    def setUp(self):
        self.osm_file_path = TEST_FILE

    def test_count_entities_with_ways_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await count_entities(osm_file_path, WayCounter)
            self.assertEqual(result, 4630)

        asyncio.run(run_test())

    def test_count_entities_with_points_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await count_entities(osm_file_path, PointCounter)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_count_entities_with_nodes_counter(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await count_entities(osm_file_path, NodeCounter)
            self.assertEqual(result, 17502)

        asyncio.run(run_test())

    def test_get_osm_graph(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)

        asyncio.run(run_test())

    def test_osw_way_filter(self):
        tags = {'key': 'value'}
        result = osw_way_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_osw_node_filter(self):
        tags = {'key': 'value'}
        result = osw_node_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_osw_point_filter(self):
        tags = {'key': 'value'}
        result = osw_point_filter(tags)
        self.assertTrue(isinstance(result, bool))

    def test_simplify_og(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)
            simplify_og_result = await simplify_og(result)
            self.assertIsNone(simplify_og_result)

        asyncio.run(run_test())

    def test_construct_geometries(self):
        osm_file_path = self.osm_file_path

        async def run_test():
            result = await get_osm_graph(osm_file_path)
            self.assertIsInstance(result, OSMGraph)
            construct_geometries_result = await construct_geometries(result)
            self.assertIsNone(construct_geometries_result)

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
