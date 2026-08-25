#!/bin/sh
#
# Only keep places that are in the given state.
#
# The filter will keep a place when the 'state' field of the address
# contains exactly the given name. You need to give the state name in the
# local language.

NAME="$@"

if [ "x$NAME" = "x" ]; then
    echo "Usage: ./filter-by-state.sh <state name>"
    exit 1
fi

jq -c "if .type == \"Place\" and .content.[0].address?.state? != \"$NAME\" then empty end"
