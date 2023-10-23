import os
import asyncio
from lib_formatter import Formatter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = f'{ROOT_DIR}/output'
INPUT_FILE = f'{ROOT_DIR}/input/wa.microsoft.osm.pbf'

is_exists = os.path.exists(OUTPUT_DIR)
if not is_exists:
    os.makedirs(OUTPUT_DIR)


async def main():
    f = Formatter(workdir=OUTPUT_DIR, pbf_file=INPUT_FILE)
    await f.osm2osw()


if __name__ == '__main__':
    asyncio.run(main())
