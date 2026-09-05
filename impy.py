from sys import exit, getwindowsversion, argv, stdout
from platform import machine
from json import dump, loads, load

stdout.reconfigure(line_buffering=True)

if machine().lower() != "amd64":
    print(f"\033[0;33mUnsupport architecture: {machine()}\033[0m")

v = getwindowsversion()
match (v.major, v.minor, v.build):
    case (5, 1, _):
        print(f"\033[0;33mUnsupport on Windows XP (build {v.build})\033[0m")
    case (5, 2, _):
        print(f"\033[0;33mUnsupport on Windows XP (build {v.build})\033[0m")
    case (6, 0, _):
        print(f"\033[0;33mUnsupport on Windows Vista (build {v.build})\033[0m")
    case (6, 1, _):
        print(f"\033[0;33mUnsupport on Windows 7 (build {v.build})\033[0m")
    case (6, 2, _):
        print(f"\033[0;33mUnsupport on Windows 8 (build {v.build})\033[0m")
    case (6, 3, _):
        print(f"\033[0;33mUnsupport on Windows 8.1 (build {v.build})\033[0m")
    case (6, 4, _):
        print(f"\033[0;33mUnsupport on Windows 10 (build {v.build})\033[0m")
    case (10, 0, _):
        pass
    case _:
        print("\033[0;31mInvalid Window version!\033[0m")
        exit(1)

from winapi import (CreateProcessW, STARTUPINFOW, PROCESS_INFORMATION, L, et,
                      DWORD, WinError, WaitForSingleObject, INFINITY, GetExitCodeProcess,
                      CloseHandle, DeleteFileW)
from niquests import get, exceptions
from pathlib import Path

args = argv[1:]
localprograms = Path.home() / "AppData" / "Local" / "Programs"
homeurl = "https://mblc-7.github.io/impy"
homepath = localprograms / "ImPy"
homepath.mkdir(exist_ok = True)
setups = homepath / "pythons"
setups.mkdir(exist_ok = True)
impt = "26.1"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 AppleWebKit/605.1.15 (KHTML, like Gecko) Firefox/157.0 Chrome/154.0.8037.0 OPR/137.0.6010.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

def writemanage(
        version: str,
        pypath: str,
        arch: str = "x64",
        adds: bool = True
    ):
    pypath = str(pypath)
    creator = {
        version: {
            "arch": arch,
            "path": pypath
        }
    }
    whereisjson: Path = homepath / "manage.json"
    if whereisjson.exists():
        with open(whereisjson, "r") as f:
            orig: dict = loads(f.read())

        if adds:
            orig |= creator
        else:
            orig.pop(version, None)
        with open(whereisjson, "w") as g:
            dump(orig, g, indent = 4)
    else:
        if adds:
            with open(whereisjson, "w") as f:
                dump(creator, f, indent = 4)
        else:
            with open(whereisjson, "w") as f:
                dump({}, f, indent = 4)

def getjson(jsonnm: str = "versions.json"):
    where = homepath / jsonnm
    wjson = f"{homeurl}/{jsonnm}"
    if where.exists():
        try:
            r = get(wjson)
            d: dict = r.json()
            with open(where, "r", encoding = "utf-8") as f:
                old = load(f)
            if d["meta"] > old["meta"]:
                print(f"Collecting {jsonnm}...")
                ret = _get(wjson, where, None)

                if isinstance(ret, int):
                    print(f"Use local saved: {where}")
        except (exceptions.ConnectionError, exceptions.Timeout):
            print(f"Use local saved: {where}")
    else:
        print("Collecting versions.json...")
        
        ret = _get(wjson, where, None)

        if isinstance(ret, int):
            if ret == 404:
                print("\033[0;31mNo version had found!\033[0m")
            elif ret == -1:
                print("\033[0;31mInternet ConnectFion Failed!\033[0m")
            elif ret == -2:
                print("\033[0;31mTimeout!\033[0m")
            elif ret == -3:
                print("\033[0;31mUnknown error occured!\033[0m")
            else:
                print(f"\033[0;31mDownload Failed! (Status Code: {ret})\033[0m")
            exit(1)

    with open(where, "r") as f:
        old = load(f)
    return old

def _get(
        url: str,
        filename: str | Path,
        params: dict = {},
        timeout: int | None = None,
    ) -> int | None:
    try:
        with get(url, params = params, headers = header, timeout = timeout, stream = True) as r:
            if r.ok:
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(5242880):
                        if chunk:
                            f.write(chunk)
                return None
            return r.status_code
    except exceptions.ConnectionError:
        return -1
    except exceptions.Timeout:
        return -2
    except Exception:
        return -3

def pysetup(
        filename: str,
        switch: str
    ) -> None:
    si = STARTUPINFOW()
    pi = PROCESS_INFORMATION()

    if not CreateProcessW(
        None,
        L(f"\"{filename}\"{switch}"),
        None,
        None,
        False,
        DWORD(0),
        None,
        None,
        et(si),
        et(pi)
    ):
        print(f"\033[0;31mAn error occured while create process: {WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31mAn error occured while get exit code: {WinError()}\033[0m")
            exit(1)
        return exit_code.value

    finally:
        CloseHandle(pi.hProcess)
        CloseHandle(pi.hThread)

def install(
        url: str,
        filename: Path,
        switch: str = "",
        pyver: str = "3",
        pythonfolder: str = "Python3",
        params: dict = {},
        timeout: int | None = None,
        info: str | None = None,
        adds: bool = True
    ) -> None:
    if filename.exists():
        print(f"Package already exists: {filename}")
    else:
        print(f"Collecting {filename if info is None else info}...")

        ret = _get(url, filename, params, timeout)

        if isinstance(ret, int):
            if ret == 404:
                print("\033[0;31mNo version had found!\033[0m")
            elif ret == -1:
                print("\033[0;31mInternet Connection Failed!\033[0m")
            elif ret == -2:
                print("\033[0;31mTimeout!\033[0m")
            elif ret == -3:
                print("\033[0;31mUnknown error occured!\033[0m")
            else:
                print(f"\033[0;31mDownload Failed! (Status Code: {ret})\033[0m")
            exit(1)

    print("Launching installer...")
    exit_code = pysetup(filename, switch)

    match exit_code:
        case 0:
            print("Install Success!")
            whereisver = localprograms / "Python" / pythonfolder
            writemanage(pyver, whereisver, "x64", adds)
            exit(0)
        case 1223 | 1602:
            print("\033[0;31mInstallation cancelled by user\033[0m")
            exit(1)
        case 1638:
            print(f"\033[0;31mAnother version had installed\033[0m")
            exit(1)
        case _:
            print(f"\033[0;31mAn error occured (exit code {exit_code})\033[0m")
            exit(1)

def remove(
        filename: str,
        info: str | None = None
    ) -> None:
    print(f"Removing {info if info is not None else filename}")
    if not DeleteFileW(L(filename)):
        print("\033[0;31mAn error occured while remove installer\033[0m")
        exit(1)
    else:
        print("Remove Success!")
        exit(0)

def build_args(argv: list) -> str:
    parts: list = []
    i = 2
    while i < len(argv):
        if argv[i] == "-c" and i + 1 < len(argv):
            parts.append("-c")
            parts.append(f'"{argv[i + 1]}"')
            i += 2
        else:
            parts.append(argv[i])
            i += 1
    return " ".join(parts)

def run_python(exe_template: str, freethread: bool = False, use_pythont: bool = False) -> None:
    where = homepath / "versions.json"
    if not where.exists():
        old = getjson()
    else:
        with open(where, "r") as f:
            old = load(f)

    try:
        v = args[1]
        freethread = freethread if freethread else v.endswith("t")
        exe_template = "python{v0}.{v1}t.exe" if freethread else exe_template
        v = v.removesuffix("t") if v.endswith("t") else v
    except IndexError:
        print("\033[0;31mInvalid syntax, if you need some help, try \"impy help\"!\033[0m")
        exit(1)

    v = old["alias"][v] if v in old["alias"] else v

    if freethread:
        if use_pythont:
            print("\033[0;33m\"pythont\" is deprecated!\033[0m")
        if v not in old["freethread"]:
            print("\033[0;31mFree-threaded is only on Python 3.13+\033[0m")
            exit(1)
        print(f"\033[0;33mIf failed, try \"impy install {args[1].removesuffix("t")}t\" to modify it!\033[0m")

    whereisjson: Path = homepath / "manage.json"
    if not whereisjson.exists():
        print("\033[0;31mTry to install or add a version first!\033[0m")
        exit(1)

    with open(whereisjson, "r") as f:
        pyaaa: dict = loads(f.read())
    
    try:
        w = pyaaa[v]["path"]
    except KeyError:
        print("\033[0;31mInvalid format!\033[0m")
        exit(1)

    v0, v1 = v.split(".")[0], v.split(".")[1]
    exe_name = exe_template.format(v0 = v0, v1 = v1)
    arg = build_args(args)

    si = STARTUPINFOW()
    pi = PROCESS_INFORMATION()

    if not CreateProcessW(
        None,
        L(f"\"{w}\\{exe_name}\" {arg}"),
        None,
        None,
        True,
        DWORD(0),
        None,
        None,
        et(si),
        et(pi)
    ):
        print(f"\033[0;31mAn error occured while create process: {WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31mAn error occured while get exit code: {WinError()}\033[0m")
            exit(1)
        if exit_code.value != 0:
            print(f"\033[0;31m\"{" ".join(args)}\" does not work! (exit code {exit_code.value})\033[0m")
    finally:
        CloseHandle(pi.hProcess)
        CloseHandle(pi.hThread)

if __name__ == "__main__":
    if args == []:
        print("\033[0;31mCannot be empty, if you need some help, try \"impy help\"!\033[0m")
        exit(1)

    match args[0]:
        case "help":
            print("help\tShow all available commands")
            print("about\tImPy version")
            print("update\tCheck update")
            print("reload\tReload versions.json")
            print("install\tInstall Python")
            print("\thelp\tShow all available Python")
            print("\t\t-s\tSkip all versions that end of life (or --skip-eol)")
            print("\t(V)\tInstall Python")
            print("\t(V)t\tInstall Python with free-threaded build (only for 3.13+)")
            print("\t(V) -u\tUninstall Python (or --uninstall)")
            print("insted\tInstalled Python")
            print("rminst\tRemove installer")
            print("\t(V)\tRemove installer")
            print("python\tRun Python (like \"impy python 3.13 -m pip install pygame\")")
            print("\t(V)\tRun Python")
            print("\t(V)t\tRun Python free-threaded build")
            print("pythonw\tRun Python with no window")
            print("\t(V)\tRun Python with no window")

        case "about":
            print(f"ImPy {impt} [Inno Setup 7.1.0, MSVC 19.51.36256, Python 3.13.15]\nCopyright © 2026 MBLC7. All rights reserved.")

        case "update":
            old = getjson()
            match impt:
                case x if x == old["update"]["dev"]:
                    print(f"\033[1;36m‼ Your ImPy is come from future! (dev-build {x})\033[0m")
                case x if x == old["update"]["new"]:
                    print(f"\033[0;32m√ Your ImPy is up to date! (build {x})\033[0m")
                case x if impt in old["update"]["compate"]:
                    print(f"\033[0;33m! Your ImPy is still compatible, but we recommend to update it to latest {old['update']['new']}!\033[0m")
                case x if impt in old["update"]["expires"]:
                    print(f"\033[0;31m× Your ImPy is end of life, update it to latest {old['update']['new']}!\033[0m")
                case _:
                    print(f"\033[0;31m× Oops! Your ImPy is not in our history!\033[0m")

        case "install":
            old = getjson()
            try:
                a = args[1]
            except IndexError:
                print("\033[0;31mInvalid syntax, if you need some help, try \"impy help\"!\033[0m")
                exit(1)
            if a == "help":
                try:
                    if args[2] in ("--skip-eol", "-s"):
                        skip_eol = True
                    else:
                        skip_eol = False
                except IndexError:
                    skip_eol = False
                a: list = old["eol"] + old["security"] + old["active"]
                print("Alias\tRefer to\n-----\t--------")
                for k, v in old["alias"].items():
                    if v in old["eol"] and skip_eol:
                        continue
                    if len(k) > 7:
                        print(f"{k[:6]}-\t{v}")
                        print(k[6:])
                    else:
                        print(f"{k}\t{v}")
                print("\n\"-\" is gap, not part of version!\ne.g. 3.15.0-↵rc1 -> 3.15.0rc1")
                print("\nCategory\tVersion\n--------\t-------")

                s: int = 0
                for i in a:
                    match i:
                        case x if x in old["eol"]:
                            if skip_eol:
                                continue
                            cat = "\033[0;31m× End of Life\033[0m"
                            s += 1
                        case x if x in old["active"]:
                            if x in old["latest"]:
                                cat = "\033[1;36m‼ Latest\033[0m"
                            else:
                                cat = "\033[0;32m√ Active\033[0m"
                            s += 1
                        case x if x in old["security"]:
                            cat = "\033[0;33m! Security\033[0m"
                            s += 1
                        case _:
                            print("\033[0;31mInvalid format!\033[0m")
                            exit(1)
                    print(f"{cat}\t{i}")
                print(f"{s} version in total")
                for c in old["credits"]:
                    print(f"\nThanks {c['name']} for {c['info']}!")
            else:
                try:
                    v = args[1]
                except:
                    print("\033[0;31mInvalid syntax, if you need some help, try \"impy help\"!\033[0m")
                    exit(1)
                v = v.removesuffix("t") if v.endswith("t") else v
                tswit = True
                syn = old["eol"] + old["security"] + old["active"]

                v = old["alias"][v] if v in old["alias"] else v
                if v not in syn:
                    print("\033[0;31mUnknown version, try \"impy reload\" to fetch latest version updates or get available version list by \"impy install help\"!\033[0m")
                    exit(1)
                fn = f"python-{v}-amd64.exe"
                shouldfn = setups / fn
                ques: bool = True
                try:
                    match args[2:]:
                        case x if "--uninstall" in x or "-u" in x:
                            switch = " /uninstall"
                            ques = False
                        case x if "-i" in x:
                            print("\033[0;33m\"-i\" is deprecated!\033[0m")
                            switch = " /passive Include_pip=1"
                        case x if "--install" in x:
                            print("\033[0;33m\"--install\" is deprecated!\033[0m")
                            switch = " /passive Include_pip=1"
                        case x if "--thread" in x or "-t" in x:
                            switch = " /passive Include_pip=1 Include_freethreaded=1"
                        case x if tswit:
                            switch = " /passive Include_pip=1 Include_freethreaded=1"
                        case _:
                            switch = " /passive Include_pip=1"
                except IndexError:
                    switch = " /passive Include_pip=1"
                
                if v in old["eol"]:
                    spec = v + " (EOL)"
                elif v in old["security"]:
                    spec = v + " (Security)"
                else:
                    spec = v

                insturl = getjson("route.json")["python"][v]
                install(
                    insturl,
                    shouldfn,
                    switch,
                    v,
                    f"Python{v.split(".")[0]}{v.split(".")[1]}",
                    {},
                    None,
                    f"Python {spec}",
                    ques
                )

        case "insted":
            whereisjson: Path = homepath / "manage.json"
            if not whereisjson.exists():
                print("\033[0;31mTry to install or add a version first!\033[0m")
                exit(1)

            with open(whereisjson, "r") as f:
                c: dict = loads(f.read())
            if c == {}:
                print("\033[0;31mInvalid format!\033[0m")
                exit(1)
            print("Version\tArch\tPath\n-------\t----\t----")
            s = list(c.keys())
            s.sort()
                
            for i in s:
                try:
                    a = c[i]["arch"]
                except KeyError:
                    a = "?"

                try:
                    p = c[i]["path"]
                except KeyError:
                    p = "?"
                if len(i) > 7:
                    print(f"{i[:6]}-\t{a}\t{p}")
                    print(i[6:])
                else:
                    print(f"{i}\t{a}\t{p}")

            print("\n\"-\" is gap, not part of version!\ne.g. 3.15.0-↵rc2 -> 3.15.0rc2")

        case "reload":
            try:
                getjson()
                print("Reload success!")

            except Exception as e:
                print(f"\033[0;31mUnknown error occured! ({e})\033[0m")

        case "python":
            run_python("python.exe")

        case "pythonw":
            run_python("pythonw.exe")

        case "pythont":
            run_python("python{v0}.{v1}t.exe", freethread = True, use_pythont = True)

        case "rminst":
            where = homepath / "versions.json"
            if not where.exists():
                old = getjson()
            else:
                with open(where, "r") as f:
                    old = load(f)
            try:
                v = args[1]
            except:
                print("\033[0;31mInvalid syntax, if you need some help, try \"impy help\"!\033[0m")
                exit(1)

            v = old["alias"][v] if v in old["alias"] else v
            instr = setups / f"python-{v}-amd64.exe"
            if v in old["eol"]:
                spec = v + " (EOL)"
            elif v in old["security"]:
                spec = v + " (Security)"
            else:
                spec = v
            remove(str(instr), f"installer of Python {spec}")
    
        case _:
            print("\033[0;31mInvalid syntax, if you need some help, try \"impy help\"!\033[0m")
            exit(1)