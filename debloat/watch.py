"""Reversible Galaxy Watch (Wear OS) debloat over plain adb.

    python3 debloat/watch.py check
    python3 debloat/watch.py dump
    python3 debloat/watch.py disable debloat/batch1-samsung-extras.pkgs
    python3 debloat/watch.py enable  debloat/batch1-samsung-extras.pkgs
    python3 debloat/watch.py enable  all

Only `pm disable-user --user 0`, never uninstall. Names in never-disable.txt are refused.
Set ADB (path) and ADB_SERIAL (ip:port) in the environment or .env.
"""
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG = os.path.join(HERE, "log.tsv")
NEVER = os.path.join(HERE, "never-disable.txt")

env = os.path.join(ROOT, ".env")
if os.path.exists(env):
    for line in open(env):
        k, _, v = line.strip().partition("=")
        if k and v:
            os.environ.setdefault(k, v)

ADB = os.environ.get("ADB", "adb")
SERIAL = os.environ.get("ADB_SERIAL")


def sh(*args):
    cmd = [ADB] + (["-s", SERIAL] if SERIAL else []) + ["shell", *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return (r.stdout + r.stderr).strip()


def read_list(path):
    out = []
    for line in open(path):
        word = line.split("#", 1)[0].strip()
        if word:
            out.append(word.split()[0])
    return out


def log(pkg, action, result):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{action}\t{pkg}\t{result}\n")


def pkgs_from(arg):
    if arg == "all":
        seen = []
        for p in sorted(glob.glob(os.path.join(HERE, "*.pkgs"))):
            seen += [x for x in read_list(p) if x not in seen]
        return seen
    return read_list(arg)


def check():
    for label, prop in [("model", "ro.product.model"), ("android", "ro.build.version.release"),
                        ("build", "ro.build.display.id")]:
        print(f"{label}: {sh('getprop', prop)}")
    print("home:", sh("cmd", "package", "resolve-activity", "--brief", "-c", "android.intent.category.HOME").splitlines()[-1:])
    print("disabled:\n" + sh("pm", "list", "packages", "-d"))
    print(sh("dumpsys", "meminfo", "|", "grep", "-E", "'Free RAM|Used RAM'"))


def dump():
    model = sh("getprop", "ro.product.model").replace(" ", "")
    path = os.path.join(HERE, f"packages-{model}.txt")
    out = sh("pm", "list", "packages", "-f", "--user", "0")
    open(path, "w").write(out + "\n")
    print(f"saved {path} ({len(out.splitlines())} packages)")


def apply(action, arg):
    never = set(read_list(NEVER))
    for pkg in pkgs_from(arg):
        if action == "disable" and pkg in never:
            print(f"REFUSED {pkg}")
            log(pkg, action, "refused")
            continue
        cmd = "disable-user" if action == "disable" else "enable"
        extra = ["--user", "0"] if action == "disable" else []
        res = sh("pm", cmd, *extra, pkg)
        print(f"{action} {pkg}: {res}")
        log(pkg, action, res)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["check"]:
        check()
    elif a[:1] == ["dump"]:
        dump()
    elif len(a) == 2 and a[0] in ("disable", "enable"):
        apply(*a)
    else:
        print(__doc__)
