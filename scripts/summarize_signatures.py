from pathlib import Path

import re
import json

pattern = re.compile(r"^sigs-(?P<name>[^-]+)-(?P<domain>[^-]+)$")


DATA=Path("data")

total = {"kadena":0, "eth":0}
validators = {"kadena":{}, "eth":{}}

for x in DATA.iterdir():

  if x.is_dir():
    m = pattern.match(x.name)
    if m:
      validator = m.group("name")
      domain = m.group("domain")


      latest = x.joinpath("checkpoint_latest_index.json")
      if latest.exists():
        with open(latest) as fd:
          height = int(fd.read())

        total[domain] = max(total[domain], height)

        validators[domain][validator] = {"name": validator, "height":height}

for d in ["kadena", "eth"]:
  for val in validators[d].values():
    val["ok"] = total[d] == val["height"]

with open("summary.json","w") as fd:
  json.dump( {"total": total, "validators":validators}, fd)
