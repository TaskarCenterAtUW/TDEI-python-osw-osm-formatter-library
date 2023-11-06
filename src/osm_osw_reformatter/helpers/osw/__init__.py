import os
import json
import zipfile
import asyncio
from typing import List
from pathlib import Path
from ...serializer.osm.osm_graph import OSMGraph
from ...serializer.counters import WayCounter, NodeCounter, PointCounter
from ...serializer.osw.osw_normalizer import OSWWayNormalizer, OSWNodeNormalizer, OSWPointNormalizer


class OSWHelper:
    @staticmethod
    def osw_way_filter(tags):
        normalizer = OSWWayNormalizer(tags)
        return normalizer.filter()

    @staticmethod
    def osw_node_filter(tags):
        normalizer = OSWNodeNormalizer(tags)
        return normalizer.filter()

    @staticmethod
    def osw_point_filter(tags):
        normalizer = OSWPointNormalizer(tags)
        return normalizer.filter()

    @staticmethod
    async def count_ways(pbf_path: str):
        loop = asyncio.get_event_loop()
        way_counter = WayCounter()
        await loop.run_in_executor(None, way_counter.apply_file, pbf_path)
        return way_counter.count

    @staticmethod
    async def count_nodes(pbf_path: str):
        loop = asyncio.get_event_loop()
        node_counter = NodeCounter()
        await loop.run_in_executor(None, node_counter.apply_file, pbf_path)
        return node_counter.count

    @staticmethod
    async def count_points(pbf_path: str):
        loop = asyncio.get_event_loop()
        point_counter = PointCounter()
        await loop.run_in_executor(None, point_counter.apply_file, pbf_path)
        return point_counter.count

    @staticmethod
    async def count_entities(pbf_path: str, counter_class):
        loop = asyncio.get_event_loop()
        counter = counter_class()
        await loop.run_in_executor(None, counter.apply_file, pbf_path)
        return counter.count

    @staticmethod
    async def get_osm_graph(pbf_path: str):
        loop = asyncio.get_event_loop()
        OG = await loop.run_in_executor(
            None,
            OSMGraph.from_pbf,
            pbf_path,
            OSWHelper.osw_way_filter,
            OSWHelper.osw_node_filter,
            OSWHelper.osw_point_filter
        )

        return OG

    @staticmethod
    def unzip(zip_file: str, output: str):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(output)
            extracted_files = zip_ref.namelist()
            required_files = ['nodes', 'edges', 'points']
            file_locations = {}

            for required_file in required_files:
                for extracted_file in extracted_files:
                    if '__MACOSX' in extracted_file:
                        continue
                    if required_file in extracted_file:
                        file_locations[required_file] = f"{output}/{extracted_file}"

            return file_locations

    @staticmethod
    def merge(osm_files: object, output: str, prefix: str):
        fc = {'type': 'FeatureCollection', 'features': []}
        for file, location in osm_files.items():
            geojson_path = Path(location)
            if geojson_path.exists():
                with open(geojson_path) as f:
                    region_fc = json.load(f)
                    fc['features'] = fc['features'] + region_fc['features']
                os.remove(geojson_path)
        output_path = Path(output, f'{prefix}.graph.all.geojson')
        with open(output_path, 'w') as f:
            json.dump(fc, f)

        return str(output_path)

    @classmethod
    async def simplify_og(cls, og):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, og.simplify)

    @classmethod
    async def construct_geometries(cls, og):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, og.construct_geometries)

    @classmethod
    async def write_og(cls, workdir: str, filename: str, og) -> List[str]:
        loop = asyncio.get_event_loop()
        points_path = Path(workdir, f'{filename}.graph.points.geojson')
        nodes_path = Path(workdir, f'{filename}.graph.nodes.geojson')
        edges_path = Path(workdir, f'{filename}.graph.edges.geojson')
        await loop.run_in_executor(None, og.to_geojson, nodes_path, edges_path, points_path)
        return [str(nodes_path), str(edges_path), str(points_path)]
