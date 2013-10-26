import json
import sys
result = []
for file in sys.argv[1:]:
  sys.stderr.write("Loading %s\n" % file)
  content = json.loads(open(file).read())
  result.extend(content)

print(json.dumps(result, indent=1))