# TDEI-python-lib-formatter-library

Formatter library which converts OSW to OSM.

Example
```python
    from lib_formatter import Formatter
    formatter = Formatter(workdir=OUTPUT_DIR, pbf_file=INPUT_FILE)
    await formatter.osm2osw()
```
