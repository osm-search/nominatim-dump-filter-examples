#!/bin/sh
#
# Only keep places that are points of interest.
#
# The Nominatim dumps do not have a separate type for POIs. They are
# intermingled with addresses in the 'house' address type. So we use a
# heuristic here: if the OSM main tag is something other than building
# or place, it is likely a POI. A positive filter which explicitly
# lists the tags you are interested in.

jq -c 'if .type == "Place" and (.content.[0].address_type != "house" or .content.[0].osm_key? == "building" or .content.[0].osm_key? == "place") then empty end'
