import json
import collections
from data.models import *
'''
Script used to filter ingredients after postprocessing 
Attempts to assimilate uncommon ingredients with a the most common single word ingredient contained (e.g. maple sugar- sugar)
Assimilates plural common ingredients with corresponding singular (e.g. eggs - egg)
Assimilates single word common ingredient with their two word counterpart. (e.g. mintleaves - mintleaves )
'''
def main():
    # Read indexed ingredients from json file and create ordered dictionary in descending order.
    with open('replacetest.json') as json_file:
        data = json.load(json_file)
    data_dict = {}
    for ing in data:
        dict[ing['title']] = ing['num_recipe']
    ordered = {k: v for k, v in sorted(data_dict.items(), key=lambda item: item[1], reverse= True)}
# variables used for statistics only
    total_ingredients = 0
    total_uncommon = 0
# listS with common and uncommon ingredients
    common_ingredients = []
    uncommon_ingredients = []
    THRESHOLD = 50 # ingredient frequency required for an ingredient to be considered common
    for k,v in ordered.items():
        total_ingredients += v
        if v >= THRESHOLD:
            common_ingredients.append(k)
        else:
            total_uncommon += v
            uncommon_ingredients.append(k)
    replacements = {} # contains all assimilations that will be performed at the end. key: old ingredient. value: new ingredient 
    total_replacements = 0 # Statistics purposes only
    # Replace all uncommon ingredients with the most common single word ingredient contained in the string
    for ing in uncommon_ingredients:
        max_freq = 0
        max_ingredient ='unmatched'
        for word in ing.split():
            if word in common_ingredients:
                if ordered[word] > max_freq:
                    max_freq = ordered[word]
                    max_ingredient = word
        if max_ingredient != 'unmatched':
            replacements[ing] = max_ingredient
            total_replacements += ordered[ing]
    # Asimillate plural ingredients with their corresponding singular ingredient (e.g. eggs - egg)
    for ing in common_ingredients:
        if ing[-1] == 's' and ing[:-1] in common_ingredients:
            replacements[ing] = ing[:-1]
            common_ingredients.remove(ing)
    #Asimillate single word ingredients with their corresponding two word variant (e.g. mintleaves - mint leaves)
    for ing in common_ingredients:
        if ' ' in ing:
            conc =''.join(ing.split())
            if conc in common_ingredients:
                replacements[conc] = ing
    #Update database
    for old in replacements.keys():
        ingr = Ingredient.objects.get(title=t[old])
        RecipeIngredient.objects.filter(ingredient__title=old).update(ingredient = ingr)

if __name__ == "__main__":
    main()
