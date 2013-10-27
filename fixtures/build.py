#! /usr/bin/python3
import glob
from PIL import Image
import json
import sys

typedict = dict()
invtypedict = dict()
starters = dict()
f=open("tree_structure.json")
data = json.loads(f.read())
for val in data:
  if val["model"] == "store.fandomhierarchy":
    typedict[val["fields"]["name"]] = val["pk"]
    invtypedict[val["pk"]] = val
    if val["fields"]["name"] == "Starters":
      starters[invtypedict[val["fields"]["parent"]]["pk"]] = val["pk"]
# {"pk": 7, "model": "store.fandomhierarchy", "fields": {"rght": 13, "name": "Red/Green/Blue/Yellow", "parent": 1, "level": 1, "
# {"pk": 8, "model": "store.fandomhierarchy", "fields": {"rght": 12, "name": "Starters", "parent": 7, "level": 2, "lft": 11, "tr

imagepk = 1
patternpk = 1
existing_images = {}
image_patterns = {}

def generation_and_starter(number):
  generations = [0, 151, 251, 386, 493, 649, 718]
  i = 0
  while number > generations[i]:
    i += 1
  offset = number - generations[i - 1]
  if i == 5:
    offset -= 1
  isStarter = (offset == 1 or offset == 4 or offset == 7)
  if i == 1 and offset == 25:
    isStarter = True # Pikachu
  print("Pokemon #%d: generation %d offset %d starter: %s" % (number, i, offset, isStarter))
  return (i, isStarter)
  
def addPattern(imagename, imagepk, fandoms):
  global patternpk
  im = Image.open(imagename)
  width, height = im.size
  pattern = { "pk": patternpk, "model": "store.pattern", "fields":
    {
      "image": imagename,
      "pixel_width": width,
      "pixel_height": height,
      "fandoms": typeids,
      "patternof": imagepk,
    }}
  patternpk += 1
  if imagepk in image_patterns:
    image_patterns[imagepk].append(pattern)
  else:
    image_patterns[imagepk] = [pattern]

print(starters)
generation_names = {"Red/Green/Blue/Yellow": 1, "Gold/Silver/Crystal": 2, "Ruby/Sapphire/Emerald": 3, "Diamond/Pearl": 4, "Black/White": 5, "X/Y": 6}
generation_ids = dict(map(lambda item: (item[1], typedict[item[0]]), generation_names.items()))
print(generation_ids)
starter_ids = dict(map(lambda item: (item[0], starters[item[1]]), generation_ids.items()))

f=open("pokemon.txt", encoding='utf-8')
for line in f:
	ignore, number, file_hint, name, types = line.split('\t', 4)
	number = int(number[2:])
	types = types.strip().split('\t')
	typeids = list(map(lambda x: typedict[x], types))
	if name in existing_images:
	  image = existing_images[name]
	else:
# {"pk": 1, "model": "store.image", "fields": {"name": "Bulbasaur"}},
	  image = { "pk": imagepk, "model": "store.image", "fields": { "name": name } }
	  imagepk += 1
	  existing_images[name] = image
	picture_pattern = "pokemon-sprites-32x32/%sMS.png" % file_hint
	file_list = glob.glob(picture_pattern)
	generation, isStarter = generation_and_starter(number)
	typeids.append(generation_ids[generation])
	if isStarter: typeids.append(starter_ids[generation])
	if len(file_list) == 0:
	  raise(IOError("Cannot determine file for #%d, %s with glob %s!" % (number, name, picture_pattern)))
	elif len(file_list) > 1:
	  raise(IOError("Ambiguous image for %d, %s: more than one image found, modify first field to specify. %s" % (number, name, file_list)))
	else: # len == 1
	  addPattern(file_list[0], image["pk"], typeids)

result = list(existing_images.values())
for v in image_patterns.values():
  result.extend(v)

out = open(sys.argv[1], 'w', encoding='utf-8')
out.write(json.dumps(result, indent=1))
