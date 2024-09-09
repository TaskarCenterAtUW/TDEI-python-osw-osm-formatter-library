import os
import argparse
from memory_profiler import profile
import asyncio
from osm_osw_reformatter import Formatter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = f'{ROOT_DIR}/output'
# OSM_INPUT_FILE = f'{ROOT_DIR}/input/wedgewood_output.osm.pbf'
OSM_INPUT_FILE = f'{ROOT_DIR}/input/map.osm'
OSW_INPUT_FILE = f'{ROOT_DIR}/input/wa.seattle.b.zip'
# OSW_INPUT_FILE = f'{ROOT_DIR}/input/wa.seattle.zip'

is_exists = os.path.exists(OUTPUT_DIR)
if not is_exists:
    os.makedirs(OUTPUT_DIR)

@profile
async def osm_convert(input_file, output_dir):
    # f = Formatter(workdir=OUTPUT_DIR, file_path=OSM_INPUT_FILE)
    f = Formatter(workdir=output_dir, file_path=input_file)
    await f.osm2osw()
    # Uncomment below line to clean up the generated files
    # f.cleanup()

@profile
def osw_convert(input_file=OSW_INPUT_FILE, output_dir=OUTPUT_DIR):
    # f = Formatter(workdir=OUTPUT_DIR, file_path=OSW_INPUT_FILE)
    print("input_file: ", input_file)
    f = Formatter(workdir=output_dir, file_path=input_file)
    f.osw2osm()
    # Uncomment below line to clean up the generated files
    # f.cleanup()
    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run OSW to OSM conversion or vice versa')
    parser.add_argument('-d', '--direction', help='OSW2OSM or OSM2OSW', required=True)
    parser.add_argument('-i', '--input_file', help='input file', required=True)
    parser.add_argument('-o', '--output_dir', help='output directory', required=True)
    args = parser.parse_args()
    
    asyncio.run(osm_convert(args.input_file, args.output_dir)) if args.direction == 'OSM2OSW' else osw_convert(args.input_file, args.output_dir)
    # osw_convert()
