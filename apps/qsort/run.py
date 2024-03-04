import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int)
parser.add_argument("--len", type=int)
args = parser.parse_args()
seed = args.seed
length = args.len

os.environ["ASAN_OPTIONS"]="halt_on_error=0:coverage=1:coverage_order_pcs=1:coverage_counters=1 "

base_dir = Path(f"exp/seed{seed:04}").resolve() / f"len{length}"

corpus_dir = str(base_dir / 'corpus')
output_dir = str(base_dir / 'output')

time.sleep(10)
subprocess.run([
            "./driver",
            corpus_dir + "/",
	        f"-artifact_prefix={output_dir}/",
            "-print_final_stats=1",
            "-detect_leaks=0",
            "-rss_limit_mb=10000",
            "-shuffle=0",
            "-runs=1000",
            f"-max_len={length}",
            "-death_mode=1",
            f"-seed={seed}",
            ])
