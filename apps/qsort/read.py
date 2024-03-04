import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f")
parser.add_argument("--head", action="store_true")
args = parser.parse_args()

with open(args.f, "rb") as f:
    data = f.read()

print(f"length: {len(data)}")

if not args.head:
    for i in data:
        print(int(i))


