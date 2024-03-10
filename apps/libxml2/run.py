import os
import json
import subprocess
import argparse
from datetime import datetime
from hashlib import md5
from pathlib import Path


"""
rm -rf $(CORPUS) $(OUTPUT)
mkdir -p $(CORPUS) $(OUTPUT)
unzip bzip2_decompress_target_seed_corpus.zip -d $(CORPUS)
ASAN_OPTIONS=halt_on_error=0:coverage=1:coverage_order_pcs=1:coverage_counters=1 \
./$(TARGET) $(CORPUS) \
-artifact_prefix=$(OUTPUT) -print_final_stats=1 \
-detect_leaks=0 -rss_limit_mb=10000 -shuffle=0 \
-runs=-1 -max_len=$(MAXLEN) -death_mode=3 -max_total_time=86400 \
"""

def main(args):
    mode_map = {
            "random": 0,
            "mutation": 1,
            "offset": 2,
            "hybrid": 3,
            }
    mode = mode_map[args.mode]
    seed = args.seed
    timestamp = datetime.now().strftime("%m%d-%H%M%S")
    print(timestamp)
    fingerprint = f"{args.mode}-s{args.seed:04}-"

    base_dir = Path.cwd() / "exp" / (fingerprint + timestamp)
    base_dir.mkdir(exist_ok=True, parents=True)

    corpus_dir = base_dir / "corpus"
    corpus_dir.mkdir(exist_ok=True, parents=True)
    corpus_dir = str(corpus_dir)

    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_dir = str(output_dir) + "/"
    """
unzip bzip2_decompress_target_seed_corpus.zip -d $(CORPUS)
ASAN_OPTIONS=halt_on_error=0:coverage=1:coverage_order_pcs=1:coverage_counters=1 \
./$(TARGET) $(CORPUS) \
-artifact_prefix=$(OUTPUT) -print_final_stats=1 \
-detect_leaks=0 -rss_limit_mb=10000 -shuffle=0 \
-runs=-1 -max_len=$(MAXLEN) -death_mode=3 -max_total_time=86400 \
    """

    subprocess.run(["unzip", "seed.zip", "-d", corpus_dir])

    cmds = [
            "./driver",
            corpus_dir,
            f"-artifact_prefix={output_dir}",
            "-print_final_stats=1",
            "-detect_leaks=0",
            "-rss_limit_mb=10000",
            "-shuffle=0",
            "-dict=libxml2/fuzz/xml.dict",
            f"-runs={args.runs}",
            f"-max_len={args.max_len}",
            f"-death_mode={mode}",
            f"-max_total_time={args.timeout}",
            ]
    print(" \\\n    ".join(cmds))

    with open(base_dir / "config.json", "w") as f:
        config = vars(args)
        config.update({
            "date": timestamp
            })
        json.dump(config, f)

    env = os.environ.copy()
    env["ASAN_OPTIONS"] = "halt_on_error=0:coverage=1:coverage_order_pcs=1:coverage_counters=1"

    with open(base_dir / "log.txt", "w") as f:
        subprocess.run(cmds, env=env, stderr=f, stdout=f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=21600)
    parser.add_argument("--max_len", type=int, default=500)
    parser.add_argument("--runs", type=int, default=-1)
    parser.add_argument("--mode", choices=[
            "random",
            "mutation",
            "offset",
            "hybrid"
        ], default="hybrid")

    args = parser.parse_args()
    main(args)
