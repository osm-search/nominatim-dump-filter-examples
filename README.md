# Examples for Filtering Nominatim Data Dumps

This repository contains simple example scripts that can be used to
filter Nominatim data dumps as created by Photon.

### Usage with Photon Imports

These filters can be used to create customised databases for the
[Photon](https://github.com/komoot/photon) geocoder. Simply add the filter
script when unpacking the Nominatim dta dump like this:

```sh
zstdcat photon-dump-planet-1.0-latest.jsonl.zst \
  | ./filter-by-address.sh city Paris \
  | java -jar photon.jar import -import-file -
```

### License

All scripts are hereby put into the public domain.
