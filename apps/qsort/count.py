import argparse
from collections import Counter
parser = argparse.ArgumentParser()
parser.add_argument("-f")
parser.add_argument("--head", action="store_true")
args = parser.parse_args()

with open(args.f, "rb") as f:
    data = f.read()

print(f"length: {len(data)}")

c = Counter()

if not args.head:
    for i in data:
        val = int(i)
        c[val] += 1


for k in sorted(c.keys()):
    v = c[k]
    print(f"{k}: {v}")

