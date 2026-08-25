#!/usr/bin/python3
#
# This filter removes all POI-like data leaving only places, streets
# and addresses in the data.
#
# Nominatim data doesn't have a distinct address type. While sometimes
# addresses appear on their own, they are as often just a property of a POI.
# Therefore the script does the following:
#
# * only keep places that are places, streets
#   or have a housenumber or addr:housename
# * for address-like objects remove all names except addr:housename
#   and change the type to a simple place=house
#
# The script will leave duplicate entries for addresses. These will be
# filtered out during search time.
import sys
import json

for line in sys.stdin:
    data = json.loads(line)

    if data['type'] == 'Place':
        outplaces = []
        for place in data['content']:
            if place['address_type'] == 'house':
                housename = place.get('name', {}).get('addr:housename')
                if housename is not None or 'housenumber' in place:
                    if 'name' in place:
                        if housename is not None:
                            place['name'] = {'addr:housename': housename}
                        else:
                            del place['name']
                    place['osm_key'] = 'place'
                    place['osm_value'] = 'house'
                    outplaces.append(place)
            elif place['address_type'] != 'other':
                outplaces.append(place)
        if not outplaces:
            continue
        data['content'] = outplaces

    json.dump(data, sys.stdout, ensure_ascii=False)
    print('')
