#!/usr/bin/env python3
"""Fetch pinned public references. Never overwrites an existing checkout."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def git(*args, cwd=None):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def main():
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / "upstream.lock.json").read_text(encoding="utf-8"))
    deps = lock["dependencies"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dependency", nargs="?", choices=sorted(deps))
    parser.add_argument("--list", action="store_true", help="只列出固定版本，不下载")
    args = parser.parse_args()
    if args.list:
        for name, spec in deps.items():
            print(f"{name}: {spec['ref']} -> {spec['path']}")
        return 0
    if args.dependency is None:
        parser.error("请选择 dependency，或使用 --list")

    spec = deps[args.dependency]
    destination = root / spec["path"]
    resolved = destination.resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise RuntimeError("Dependency path must remain inside the project.")
    if destination.exists():
        raise RuntimeError(
            f"Destination already exists; left unchanged: {destination}\n"
            "Inspect the checkout manually before updating or retrying."
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    print(f"Fetching {args.dependency} at {spec['ref']}...", flush=True)
    git("init", cwd=destination)
    git("remote", "add", "origin", spec["url"], cwd=destination)
    git("fetch", "--depth=1", "origin", spec["ref"], cwd=destination)
    revision = git("rev-parse", "FETCH_HEAD^{commit}", cwd=destination)
    if spec["revision_kind"] == "commit" and revision != spec["ref"]:
        raise RuntimeError("Fetched commit does not match upstream.lock.json.")
    git("checkout", "--detach", revision, cwd=destination)
    if spec.get("recursive_submodules"):
        git("submodule", "update", "--init", "--recursive", "--depth=1", cwd=destination)
    print(f"Ready: {destination}\nCommit: {revision}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Fetch failed: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        print("Existing/partial directories are preserved for inspection.", file=sys.stderr)
        raise SystemExit(1)
