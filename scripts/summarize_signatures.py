from pathlib import Path

import re
import json
from operator import itemgetter

VALIDATORS_RE = re.compile(r"^sigs-(?P<name>[^-]+)-(?P<domain>[^-]+)$")
CHECKPOINT_RE = re.compile(r"^checkpoint_(\d+)_with_id\.json$")

DOMAINS = ["kadena","eth"]

DATA=Path("data")

total = {}
validators = {}

def checkpoints(validator_dir):
  for cp in validator_dir.iterdir():
    match = CHECKPOINT_RE.match(cp.name)
    if match:
      yield int(match.group(1))

def get_max_checkpoint(validator_dir):
  return max(checkpoints(validator_dir), default=0)

def get_validators(domain):
  for d in DATA.iterdir():
    if d.is_dir():
      m = VALIDATORS_RE.match(d.name)
      if m and m.group("domain") == domain:
        yield (d, m.group("name"))


for domain in DOMAINS:
  validators[domain] = {}

  for (v_dir, validator) in get_validators(domain):
    validators[domain][validator] = {"name": validator, "height":get_max_checkpoint(v_dir), "ok":False}

  max_domain_cp = max( map(itemgetter("height"), validators[domain].values()))

  for v in validators[domain].values():
    if v["height"] == max_domain_cp:
      v["ok"] = True

  total[domain] = max_domain_cp

with open("summary.json","w") as fd:
  json.dump( {"total": total, "validators":validators}, fd, indent=4)
