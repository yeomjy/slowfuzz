import numpy as np
import argparse
from pathlib import Path
import shutil
parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int)
parser.add_argument("--len", type=int)
args = parser.parse_args()
seed = args.seed
length = args.len
rng = np.random.default_rng(seed)

seed_files = [
        rng.integers(low=0, high=256, size=length).squeeze().tolist()
        for _ in range(100)
        ]

base_dir = Path.cwd()

corpus_dir = base_dir / 'corpus'
output_dir = base_dir / 'output'

corpus_dir.mkdir(exist_ok=True, parents=True)
output_dir.mkdir(exist_ok=True, parents=True)

for i in range(100):
    with open(corpus_dir / f"seed_file_{i}", "wb") as f:
        for e in seed_files[i]:
            f.write(e.to_bytes())


