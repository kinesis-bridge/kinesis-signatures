from pathlib import Path

import re
import json

pattern = re.compile(r"^sigs-(?P<name>[^-]+)-(?P<domain>[^-]+)$")

CHECKPOINT_RE = re.compile(r"^checkpoint_(\d+)_with_id\.json$")

DATA=Path("data")

total = {"kadena":0, "eth":0}
validators = {"kadena":{}, "eth":{}}

for x in DATA.iterdir():

  if x.is_dir():
    m = pattern.match(x.name)
    if m:
      validator = m.group("name")
      domain = m.group("domain")

      height = 0
      for cp in x.iterdir():
        match = CHECKPOINT_RE.match(cp.name)

        if match:
          checkpoint_id = int(match.group(1))
          height = max(checkpoint_id, height)

      total[domain] = max(total[domain], height)

      validators[domain][validator] = {"name": validator, "height":height}

for d in ["kadena", "eth"]:
  for val in validators[d].values():
    val["ok"] = total[d] == val["height"]

with open("summary.json","w") as fd:
  json.dump( {"total": total, "validators":validators}, fd)
