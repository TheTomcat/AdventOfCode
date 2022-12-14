from collections import defaultdict

from framework.input_helper import read_entire_input
from framework.helpers import solution_timer


test = [
    "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
    "trh fvjkl sbzzf mxmxvkd (contains dairy)",
    "sqjhc fvjkl (contains soy)",
    "sqjhc mxmxvkd sbzzf (contains fish)",
]

data = read_entire_input(2020,21)

def parse(data):
    all_ingredients = []
    all_allergens = {}
    for row in data:
        ingredients, allergens = row.split(" (contains ")
        ingredients = ingredients.split(" ")
        allergens = allergens[:-1].split(", ")
        all_ingredients += ingredients
        for allergen in allergens:
            if allergen in all_allergens:
                all_allergens[allergen] &= set(ingredients)
            else:
                all_allergens[allergen] = set(ingredients)
    return all_ingredients, all_allergens

def create_allergen_index(data):
    index = defaultdict(list)
    for ingredients, allergens in data:
        index[tuple(sorted(allergens))].append(set(ingredients))
    return index

i,a = parse(test)

@solution_timer(2020,21,1)
def part_one(data, verbose=False):
    ingredients, allergens = parse(data)

    foods_with_allergents = set([i for v in allergens.values() for i in v])
    safe_foods = [i for i in ingredients if i not in foods_with_allergents]
    return len(safe_foods)

@solution_timer(2020,21,2)
def part_two(data, verbose=False):
    ingredients, allergens = parse(data)
    canonical = {}
    
    while allergens:
        known = [(allergen,list(ingredient_set)[0]) for allergen,ingredient_set in allergens.items() if len(ingredient_set) == 1] # Find recipes that contain a single ingredient
        for known_allergen,canonical_ingredient in known: 
            canonical[known_allergen] = canonical_ingredient
            del allergens[known_allergen] 
            for a in allergens: # Remove this ingredient from all recipes
                if canonical_ingredient in allergens[a]:
                    allergens[a].remove(canonical_ingredient)
    
    return ','.join([canonical_ingredient for known_allergen,canonical_ingredient in sorted(canonical.items())])
    