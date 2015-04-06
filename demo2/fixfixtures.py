import json

src = json.load(open("demo.json"))
for obj in src:
    keys = obj['fields'].copy().keys()
    for field in keys:
        if field in "modified created status_changed version".split(" "):
            del obj['fields'][field]

print(json.dumps(src))
