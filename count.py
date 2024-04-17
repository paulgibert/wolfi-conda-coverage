# Standard lib
from typing import List, Dict
import argparse
import json
import subprocess

# 3rd party
from tqdm import tqdm

# Local


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("wolfi_packages")
    parser.add_argument("conda_packages")
    parser.add_argument("-o", "--out",
                        help="Output JSON file to store matches",
                        default="matches.json")
    return parser.parse_args()


def read_wolfi_packages(file_name: str) -> List[str]:
    with open(file_name, "r", encoding="utf-8") as f:
        packages = f.readlines()
    return [p.strip("\n") for p in packages if p.startswith("py3")]


def read_conda_packages(file_name: str) -> List[str]:
    with open(file_name, "r", encoding="utf-8") as f:
        packages = f.readlines()
    return [p.strip("\n") for p in packages if not p.startswith("r-")]


def get_conda_equivalent(package: str, conda_packages: List[str]) -> bool:
    """
    Match against the inner package name of the wolfi package name. I.e
    assume all wolfi package names follow the same naming convention
    for python:
    
    [py3*]-[package_name]-[version]-[revision]
    """
    name = "-".join(package.split("-")[1:-2])
    for cpkg in conda_packages:
        if name == cpkg:
            return cpkg
    return None


def write_matches(file_name: str, matches: Dict):
    with open(file_name, "w") as f:
        matches_str = json.dumps(matches, indent=4)
        f.write(matches_str)


def main():
    args = parse_args()

    wolfi_pkgs = read_wolfi_packages(args.wolfi_packages)
    conda_pkgs = read_conda_packages(args.conda_packages)
    
    matches = {}
    for wpkg in tqdm(wolfi_pkgs):
        cpkg = get_conda_equivalent(wpkg, conda_pkgs)
        matches[wpkg] = cpkg
    
    n_matches = len([v for v in matches.values() if v is not None])
    print(f"{n_matches} of {len(wolfi_pkgs)} wolfi packages were found in conda.")
    print(f"{len(conda_pkgs) - n_matches} conda packages had no wolfi equivalent.")
    write_matches(args.out, matches)


if __name__ == "__main__":
    main()