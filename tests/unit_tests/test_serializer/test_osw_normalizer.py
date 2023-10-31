import unittest
from src.osm_osw_reformatter.serializer.osw.osw_normalizer import OSWWayNormalizer, OSWNodeNormalizer, \
    OSWPointNormalizer, tactile_paving, surface, crossing, crossing_markings, incline


class TestOSWWayNormalizer(unittest.TestCase):
    def test_is_sidewalk(self):
        tags = {'highway': 'footway', 'footway': 'sidewalk'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_sidewalk())

    def test_is_crossing(self):
        tags = {'highway': 'footway', 'footway': 'crossing'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_crossing())

    def test_is_traffic_island(self):
        tags = {'highway': 'footway', 'footway': 'traffic_island'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_traffic_island())

    def test_is_footway(self):
        tags = {'highway': 'footway'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_footway())

    def test_is_stairs(self):
        tags = {'highway': 'steps'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_stairs())

    def test_is_pedestrian(self):
        tags = {'highway': 'pedestrian'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_pedestrian())

    def test_is_cycleway(self):
        tags = {'highway': 'cycleway'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_cycleway())

    def test_is_living_street(self):
        tags = {'highway': 'living_street'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_living_street())

    def test_is_path(self):
        tags = {'highway': 'path'}
        normalizer = OSWWayNormalizer(tags)
        self.assertTrue(normalizer.is_path())

    def test_normalize_sidewalk(self):
        tags = {'highway': 'footway', 'footway': 'sidewalk', 'width': '1.5', 'surface': 'asphalt'}
        normalizer = OSWWayNormalizer(tags)
        result = normalizer.normalize()
        expected = {'highway': 'footway', 'width': 1.5, 'surface': 'asphalt', 'footway': 'sidewalk'}
        self.assertEqual(result, expected)

    def test_normalize_crossing(self):
        tags = {'highway': 'footway', 'footway': 'crossing'}
        normalizer = OSWWayNormalizer(tags)
        result = normalizer.normalize()
        expected = {'highway': 'footway', 'footway': 'crossing'}
        self.assertEqual(result, expected)

    def test_normalize_invalid_way(self):
        tags = {'highway': 'invalid_type'}
        normalizer = OSWWayNormalizer(tags)
        with self.assertRaises(ValueError):
            normalizer.normalize()


class TestOSWNodeNormalizer(unittest.TestCase):
    def test_is_kerb(self):
        tags = {'kerb': 'flush'}
        normalizer = OSWNodeNormalizer(tags)
        self.assertTrue(normalizer.is_kerb())

    def test_is_kerb_invalid(self):
        tags = {'kerb': 'invalid_type'}
        normalizer = OSWNodeNormalizer(tags)
        self.assertFalse(normalizer.is_kerb())

    def test_normalize_kerb(self):
        tags = {'kerb': 'flush', 'barrier': 'some_barrier', 'tactile_paving': 'yes'}
        normalizer = OSWNodeNormalizer(tags)
        result = normalizer.normalize()
        expected = {'kerb': 'flush', 'barrier': 'some_barrier', 'tactile_paving': True, 'barrier': 'kerb'}
        self.assertEqual(result, expected)

    def test_normalize_invalid_node(self):
        tags = {'type': 'invalid_node_type'}
        normalizer = OSWNodeNormalizer(tags)
        with self.assertRaises(ValueError):
            normalizer.normalize()


class TestOSWPointNormalizer(unittest.TestCase):
    def test_is_powerpole(self):
        tags = {'power': 'pole'}
        normalizer = OSWPointNormalizer(tags)
        self.assertTrue(normalizer.is_powerpole())

    def test_is_powerpole_invalid(self):
        tags = {'power': 'invalid_type'}
        normalizer = OSWPointNormalizer(tags)
        self.assertFalse(normalizer.is_powerpole())

    def test_normalize_powerpole(self):
        tags = {'power': 'pole', 'barrier': 'some_barrier', 'tactile_paving': 'yes'}
        normalizer = OSWPointNormalizer(tags)
        result = normalizer.normalize()
        expected = {'is_point': True, 'power': 'pole'}
        self.assertEqual(result, expected)

    def test_normalize_invalid_point(self):
        tags = {'type': 'invalid_point_type'}
        normalizer = OSWPointNormalizer(tags)
        with self.assertRaises(ValueError):
            normalizer.normalize()


class TestCommonFunctions(unittest.TestCase):
    def test_tactile_paving(self):
        self.assertTrue(tactile_paving('yes'))
        self.assertTrue(tactile_paving('contrasted'))
        self.assertFalse(tactile_paving('no'))
        self.assertIsNone(tactile_paving('invalid_value'))

    def test_surface(self):
        self.assertEqual(surface('asphalt'), 'asphalt')
        self.assertEqual(surface('concrete'), 'concrete')
        self.assertIsNone(surface('invalid_surface'))

    def test_crossing(self):
        self.assertEqual(crossing('marked'), 'marked')
        self.assertEqual(crossing('uncontrolled'), 'marked')
        self.assertEqual(crossing('traffic_signals'), 'marked')
        self.assertEqual(crossing('zebra'), 'marked')
        self.assertEqual(crossing('unmarked'), 'unmarked')
        self.assertIsNone(crossing('invalid_value'))

    def test_crossing_markings(self):
        self.assertEqual(crossing_markings('dashes'), 'dashes')
        self.assertEqual(crossing_markings('dots'), 'dots')
        self.assertIsNone(crossing_markings('invalid_value'))

    def test_incline(self):
        self.assertEqual(incline('up'), 'up')
        self.assertEqual(incline('down'), 'down')
        self.assertIsNone(incline('invalid_value'))


if __name__ == '__main__':
    unittest.main()
