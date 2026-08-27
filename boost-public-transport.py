#!/usr/bin/python3
#
# This example boosts the importance of public transport stops, so that
# they are preferably returned during search.

import sys
import json

# Define the minimum importance a place gets with a given main tag.
PT_TAGS = {
  'highway' : { 'bus_stop': 0.1 },
  'public_transport' : { 'station': 0.15, 'platform': 0.8 },
  'amenity' : {'bus_station': 0.2, 'ferry_terminal': 0.6 },
  'railway' : {'station' : 0.7, 'halt': 0.4 },
}

for line in sys.stdin:
    data = json.loads(line)

    modified = False
    if data['type'] == 'Place':
        outplaces = []
        for place in data['content']:
            okey = place.get('osm_key')
            ovalue = place.get('osm_value')
            if pt_importance := PT_TAGS.get(okey, {}).get(ovalue):
                orig_importance = place.get('importance', 0.0)
                # Add the original importance proportionally to the
                # base importance for the stop type. That way station that
                # are important enough to have their own wikipedia page
                # get an extra boost.
                place['importance'] = pt_importance \
                                       + (1 - pt_importance) * orig_importance
                modified = True

    # When the places are unmodified then skip json serialisation and
    # simply forward the original line.
    if modified:
        json.dump(data, sys.stdout, ensure_ascii=False)
        print('')
    else:
        print(line, end='')
