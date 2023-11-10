import os
import asyncio
from pathlib import Path
from ..serializer.counters import WayCounter, PointCounter, NodeCounter
from ..helpers.response import Response
from ..helpers.osw import OSWHelper


class OSM2OSW:
    def __init__(self, prefix: str, pbf_file=None, workdir=None):
        self.pbf_path = str(Path(pbf_file))
        filename = os.path.basename(pbf_file).replace('.pbf', '').replace('.osm', '')
        self.workdir = workdir
        self.filename = f'{prefix}.{filename}'
        self.generated_files = []

    async def convert(self) -> Response:
        try:
            print('Estimating number of ways, nodes and points in datasets...')
            tasks = [
                OSWHelper.count_entities(self.pbf_path, WayCounter),
                OSWHelper.count_entities(self.pbf_path, NodeCounter),
                OSWHelper.count_entities(self.pbf_path, PointCounter)
            ]

            count_results = await asyncio.gather(*tasks)

            print('Creating networks from region extracts...')
            tasks = [OSWHelper.get_osm_graph(self.pbf_path)]
            osm_graph_results = await asyncio.gather(*tasks)
            osm_graph_results = list(osm_graph_results)
            OG = osm_graph_results[0]

            await OSWHelper.simplify_og(OG)

            await OSWHelper.construct_geometries(OG)

            # for OG in osm_graph_results:
            generated_files = await OSWHelper.write_og(self.workdir, self.filename, OG)

            print(f'Created OSW files!')
            self.generated_files = generated_files
            resp = Response(status=True, generated_files=generated_files)
        except Exception as error:
            print(error)
            resp = Response(status=False, error=str(error))
        return resp

