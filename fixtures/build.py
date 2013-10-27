import glob
from PIL import Image
import json
import sys

typedict = dict()
f=open("tree_structure.json")
data = json.loads(f.read())
for val in data:
  if val["model"] == "store.fandomhierarchy":
    typedict[val["fields"]["name"]] = val["pk"]

f=open("pokemon.txt", encoding='utf-8')

imagepk = 1
patternpk = 1
existing_images = {}
image_patterns = {}

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

#{"pk": 1, "model": "store.pattern", "fields": {"pixel_width": 32, "pixel_height": 32, "image": "/media/pokemon-sprites-32x32/001MS.png", "fandoms": [8, 31, 25], "patternof": 1}},


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
