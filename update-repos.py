#!/usr/bin/env python3
"""Fetch upstream and rebase the standard CFEngine repos."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

REPOS = ["core", "masterfiles", "enterprise", "nova", "mission-portal", "buildscripts"]
ROOT = Path.home() / "ntech"


@dataclass
class Result:
    name: str
    status: str
    message: str = ""
    children: list["Result"] = field(default_factory=list)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True)


def has_upstream(repo: Path) -> bool:
    r = run(["git", "remote"], repo)
    return "upstream" in r.stdout.split()


def is_clean(repo: Path) -> bool:
    r = run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=no",
            "--ignore-submodules=all",
        ],
        repo,
    )
    return r.returncode == 0 and r.stdout.strip() == ""


def ref_exists(repo: Path, ref: str) -> bool:
    r = run(["git", "rev-parse", "--verify", "--quiet", ref], repo)
    return r.returncode == 0


def local_branch_exists(repo: Path, branch: str) -> bool:
    return ref_exists(repo, f"refs/heads/{branch}")


def rev_count(repo: Path, range_expr: str) -> int:
    r = run(["git", "rev-list", "--count", range_expr], repo)
    if r.returncode != 0:
        return 0
    return int(r.stdout.strip() or "0")


def head_sha(repo: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], repo).stdout.strip()


def update_repo(
    name: str, repo: Path, branch: str | None, tag: str | None, is_core: bool
) -> Result:
    if not repo.exists():
        return Result(name, "failed", f"directory not found: {repo}")
    if not (repo / ".git").exists():
        return Result(name, "failed", "not a git repository")
    if not has_upstream(repo):
        return Result(name, "failed", "no 'upstream' remote")
    if not is_clean(repo):
        return Result(name, "skipped", "working tree dirty")

    fetch = run(["git", "fetch", "upstream"], repo)
    if fetch.returncode != 0:
        return Result(name, "failed", f"fetch failed: {fetch.stderr.strip()}")

    if tag is not None:
        result = checkout_tag(name, repo, tag)
    else:
        assert branch is not None
        result = rebase_branch(name, repo, branch)

    if is_core and result.status != "failed":
        result.children.append(sync_submodule("libntech", repo, "libntech"))

    return result


def sync_submodule(name: str, parent: Path, sub_path: str) -> Result:
    sub_repo = parent / sub_path
    if sub_repo.exists() and (sub_repo / ".git").exists() and not is_clean(sub_repo):
        return Result(name, "skipped", "working tree dirty")

    old_head = (
        head_sha(sub_repo)
        if sub_repo.exists() and (sub_repo / ".git").exists()
        else None
    )

    r = run(["git", "submodule", "update", "--init", sub_path], parent)
    if r.returncode != 0:
        detail = r.stderr.strip() or r.stdout.strip()
        return Result(name, "failed", f"submodule update failed: {detail}")

    new_head = head_sha(sub_repo)
    if old_head == new_head:
        return Result(name, "ok", f"already at {new_head[:12]}")
    return Result(name, "ok", f"checked out {new_head[:12]}")


def rebase_branch(name: str, repo: Path, branch: str) -> Result:
    upstream_ref = f"upstream/{branch}"
    if not ref_exists(repo, upstream_ref):
        return Result(name, "skipped", f"{upstream_ref} does not exist")

    if local_branch_exists(repo, branch):
        co = run(["git", "checkout", branch], repo)
    else:
        co = run(["git", "checkout", "-b", branch, "--track", upstream_ref], repo)
    if co.returncode != 0:
        return Result(name, "failed", f"checkout failed: {co.stderr.strip()}")

    old_head = head_sha(repo)
    ahead = rev_count(repo, f"{old_head}..{upstream_ref}")

    rebase = run(["git", "rebase", upstream_ref], repo)
    if rebase.returncode != 0:
        _ = run(["git", "rebase", "--abort"], repo)
        detail = rebase.stderr.strip() or rebase.stdout.strip()
        return Result(name, "failed", f"rebase failed: {detail}")

    message = (
        "already up to date"
        if ahead == 0
        else f"rebased onto {upstream_ref} (+{ahead} commits)"
    )
    return Result(name, "ok", message)


def checkout_tag(name: str, repo: Path, tag: str) -> Result:
    tag_ref = f"refs/tags/{tag}"
    if not ref_exists(repo, tag_ref):
        return Result(name, "skipped", f"tag {tag} not found")

    tag_sha = run(["git", "rev-parse", f"{tag_ref}^{{commit}}"], repo).stdout.strip()
    if head_sha(repo) == tag_sha:
        return Result(name, "ok", f"already at tag {tag}")

    co = run(["git", "checkout", "--detach", tag_ref], repo)
    if co.returncode != 0:
        return Result(name, "failed", f"checkout failed: {co.stderr.strip()}")

    return Result(name, "ok", f"checked out tag {tag}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    _ = group.add_argument(
        "--branch",
        default=None,
        help="Branch to track (default: master). E.g. 3.27.x",
    )
    _ = group.add_argument(
        "--tag",
        default=None,
        help="Tag to check out in detached HEAD. E.g. 3.24.2",
    )
    args = ap.parse_args()
    branch = cast(str | None, args.branch)
    tag = cast(str | None, args.tag)
    if branch is None and tag is None:
        branch = "master"

    width = max(len(r) for r in REPOS + ["libntech"])
    parent_prefix_w = len(f"[{len(REPOS)}/{len(REPOS)}] ")
    tags = {"ok": "ok", "skipped": "SKIP", "failed": "FAIL"}

    def print_result(prefix: str, res: Result) -> None:
        name_w = width - (len(prefix) - parent_prefix_w)
        line = f"{prefix}{res.name:<{name_w}} ... {tags[res.status]}"
        if res.message:
            line += f": {res.message}"
        print(line)

    results: list[Result] = []
    for i, name in enumerate(REPOS, 1):
        path = ROOT / name
        res = update_repo(name, path, branch, tag, is_core=(name == "core"))
        results.append(res)
        print_result(f"[{i}/{len(REPOS)}] ", res)
        for child in res.children:
            print_result("      └ ", child)

    flat = [r for res in results for r in (res, *res.children)]
    ok = sum(1 for r in flat if r.status == "ok")
    skipped = sum(1 for r in flat if r.status == "skipped")
    failed = sum(1 for r in flat if r.status == "failed")
    print()
    print(f"Summary: {ok} ok, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
