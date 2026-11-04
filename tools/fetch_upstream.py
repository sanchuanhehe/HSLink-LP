#!/usr/bin/env python3
"""Initialize or verify the Git submodules pinned in upstream.lock.json."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def git(*args, cwd, capture=True):
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture else ""


def dependency_path(root, spec):
    destination = root / spec["path"]
    resolved = destination.resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise RuntimeError("Dependency path must remain inside the project.")
    return destination


def check_registration(root, spec):
    if spec["revision_kind"] != "commit":
        raise RuntimeError("Pin the dependency to a commit before initializing it.")
    entry = git("ls-files", "--stage", "--", spec["path"], cwd=root)
    metadata, separator, path = entry.partition("\t")
    if not separator or path != spec["path"]:
        raise RuntimeError(f"Not a registered Git submodule: {spec['path']}")
    if metadata.split() != ["160000", spec["ref"], "0"]:
        raise RuntimeError(f"Git submodule and lock file disagree: {spec['path']}")
    url = git(
        "config", "--file", ".gitmodules", "--get",
        f"submodule.{spec['path']}.url", cwd=root,
    )
    if url != spec["url"]:
        raise RuntimeError(f"Submodule URL and lock file disagree: {spec['path']}")


def check_checkout(destination, spec):
    if not (destination / ".git").exists():
        raise RuntimeError(f"Dependency is not initialized: {destination}")
    checkout_root = Path(git("rev-parse", "--show-toplevel", cwd=destination))
    if checkout_root.resolve() != destination.resolve():
        raise RuntimeError(f"Not a standalone checkout: {destination}")
    revision = git("rev-parse", "HEAD", cwd=destination)
    if revision != spec["ref"]:
        raise RuntimeError(f"Checkout differs from the locked commit: {destination}")
    if git("remote", "get-url", "origin", cwd=destination) != spec["url"]:
        raise RuntimeError(f"Checkout origin differs from the locked URL: {destination}")
    changes = git("status", "--porcelain", "--untracked-files=all", cwd=destination)
    if changes:
        raise RuntimeError(f"Checkout has local changes; left unchanged: {destination}\n{changes}")


def check_nested(destination):
    # Keep the leading space: '-', '+' and 'U' report incomplete/mismatched states.
    result = subprocess.run(
        ["git", "submodule", "status", "--recursive"], cwd=destination,
        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    lines = result.stdout.splitlines()
    invalid = [line for line in lines if line and line[0] != " "]
    if invalid:
        raise RuntimeError("Nested submodules are not at their pinned commits:\n" + "\n".join(invalid))
    return len(lines)


def main():
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / "upstream.lock.json").read_text(encoding="utf-8"))
    deps = lock["dependencies"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dependency", nargs="?", choices=sorted(deps))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", help="只列出固定版本，不下载")
    mode.add_argument("--check", action="store_true", help="只读核对版本、工作区和嵌套子模块")
    args = parser.parse_args()
    if args.list:
        for name, spec in deps.items():
            print(f"{name}: {spec['ref']} -> {spec['path']}")
        return 0
    if args.dependency is None and not args.check:
        parser.error("请选择 dependency，或使用 --list / --check")

    selected = [args.dependency] if args.dependency else list(deps)
    for name in selected:
        spec = deps[name]
        destination = dependency_path(root, spec)
        check_registration(root, spec)
        if not args.check:
            if destination.exists() and any(destination.iterdir()):
                check_checkout(destination, spec)
            print(f"Initializing {name} at {spec['ref']}...", flush=True)
            command = ["submodule", "update", "--init", "--checkout", "--depth=1"]
            if spec.get("recursive_submodules"):
                command.append("--recursive")
            git(*command, "--", spec["path"], cwd=root, capture=False)
        check_checkout(destination, spec)
        nested = check_nested(destination)
        print(f"OK {name}: {spec['ref']} ({nested} nested submodules)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Upstream operation failed: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        print("Existing/partial directories are preserved for inspection.", file=sys.stderr)
        raise SystemExit(1)
