#!/usr/bin/python3
#
# This example script adds categories based on the OSM cusine tag.
# See https://wiki.openstreetmap.org/wiki/Key:cuisine
#
# The values are grouped in three subgroups: origin, food and place.
# Only known values for each group are accepted.
# If multiple comma-separated values are present, then for each value
# one category entry is made.
import sys
import json

CUISINE_ORIGIN_VALUES = [
'afghan', 'african', 'american', 'arab', 'argentinian', 'armenian', 'asian', 'australian', 'austrian', 'balkan', 'bangladeshi', 'basque', 'bavarian', 'belgian', 'bolivian', 'brazilian', 'british', 'bulgarian', 'cajun', 'cambodian', 'cantonese', 'caribbean', 'catalan', 'chinese', 'colombian', 'croatian', 'cuban', 'czech', 'danish', 'dutch', 'egyptian', 'ethiopian', 'european', 'filipino', 'french', 'galician', 'georgian', 'german', 'ghanaian', 'greek', 'hawaiian', 'hunanese', 'hungarian', 'indian', 'indonesian', 'irish', 'italian', 'jamaican', 'japanese', 'jewish', 'korean', 'kurdish', 'lao', 'latin_american', 'lebanese', 'malagasy', 'malaysian', 'mediterranean', 'mexican', 'middle_eastern', 'padang', 'mongolian', 'moroccan', 'nepalese', 'oriental', 'pakistani', 'persian', 'peruvian', 'polish', 'portuguese', 'romanian', 'russian', 'salvadoran', 'senegalese', 'serbian', 'sichuanese', 'singaporean', 'south_indian', 'southern', 'spanish', 'sri_lankan', 'surinamese', 'swedish', 'swiss', 'syrian', 'taiwanese', 'tex-mex', 'thai', 'tibetan', 'tunisian', 'turkish', 'ukrainian', 'uzbek', 'venezuelan', 'vietnamese', 'western'
]
CUISINE_FOOD_VALUES = [
'açaí', 'arepa', 'bagel', 'beef', 'beef_bowl', 'beef_noodle', 'bubble_tea', 'burger', 'cachapa', 'cake', 'chicken', 'chili', 'chocolate', 'churro', 'coffee_shop', 'couscous', 'crepe', 'curry', 'donut', 'dumplings', 'empanada', 'falafel', 'fish', 'fish_and_chips', 'fondue', 'fried_chicken', 'fries', 'frozen_yogurt', 'gyoza', 'gyros', 'hot_dog', 'ice_cream', 'juice', 'kebab', 'kürtőskalács', 'lángos', 'meat', 'noodle', 'pancake', 'pasta', 'pastry', 'piadina', 'pie', 'pie_and_mash', 'pita', 'pizza', 'poke', 'potato', 'pretzel', 'ramen', 'rice_noodle', 'salad', 'sandwich', 'sausage', 'savory_pancakes', 'seafood', 'shawarma', 'smoothie', 'smørrebrød', 'soba', 'soup', 'souvlaki', 'steak', 'sushi', 'tacos', 'takoyaki', 'tea', 'udon', 'waffle', 'wings', 'yakitori'
]
CUISINE_PLACE_VALUES = [
'bakery', 'bar_and_grill', 'barbecue', 'basque_ciderhouse', 'bistro', 'brasserie', 'breakfast', 'brunch', 'buffet', 'buschenschank', 'deli', 'dessert', 'dim_sum', 'diner', 'fine_dining', 'fried_food', 'friture', 'fusion', 'grill', 'heuriger', 'hotpot', 'international', 'local', 'lunch', 'mongolian_grill', 'pub', 'regional', 'snack', 'steak_house', 'tapas', 'yakiniku'
]

# Create a lookup-table from value to subgroup:
CUISINE_LOOKUP = {v: 'origin' for v in CUISINE_ORIGIN_VALUES}
CUISINE_LOOKUP.update({v: 'food' for v in CUISINE_FOOD_VALUES})
CUISINE_LOOKUP.update({v: 'place' for v in CUISINE_PLACE_VALUES})


for line in sys.stdin:
    data = json.loads(line)

    modified = False
    if data['type'] == 'Place':
        outplaces = []
        for place in data['content']:
            if cuisine := place.get('extra', {}).get('cuisine'):
                categories = [f'cuisine.{CUISINE_LOOKUP[v]}.{v}' for v in cuisine.split(';')
                              if v in CUISINE_LOOKUP]
                if categories:
                    if 'categories' in place:
                        place['categories'].extend(categories)
                    else:
                        place['categories'] = categories
                    modified = True

    # When the places are unmodified then skip json serialisation and
    # simply forward the original line.
    if modified:
        json.dump(data, sys.stdout, ensure_ascii=False)
        print('')
    else:
        print(line, end='')
