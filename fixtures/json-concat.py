import json
import sys
result = []
for file in sys.argv[1:-1]:
  sys.stderr.write("Loading %s\n" % file)
  content = json.loads(open(file, encoding='utf-8').read())
  result.extend(content)

sys.stderr.write("Outputting result to %s\n" % sys.argv[-1])
out = open(sys.argv[-1], "w", encoding='utf-8')
out.write(json.dumps(result, indent=1))
