#!/bin/sh
#
# Only keep places that are in the given postal city.
#
# The filter will keep a place when the 'city' field of the address
# contains exactly the city name. You need to give the city name in the
# local language.

NAME="$@"

if [ "x$NAME" = "x" ]; then
    echo "Usage: ./filter-by-city.sh <city name>"
    exit 1
fi

jq -c "if .type == \"Place\" and .content.[0].address?.city? != \"$NAME\" then empty end"
