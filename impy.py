from locale import getdefaultlocale
from sys import exit, getwindowsversion, argv, stdout
from platform import machine
from json import dump, loads, load

stdout.reconfigure(line_buffering=True)
loc = getdefaultlocale()[0]
loc = "en_US" if loc not in ["en_US", "zh_CN", "zh_TW"] else loc

locmap: dict = {
    "unsarch": {
        "zh_CN": "不支持的架构：",
        "zh_TW": "不支援的架構：",
        "en_US": "Unsupport architecture: "
    },

    "unsupport": {
        "zh_CN": "不支持",
        "zh_TW": "不支援",
        "en_US": "Unsupport on"
    },

    "winverinvalid": {
        "zh_CN": "无效的 Windows 版本！",
        "zh_TW": "無效的 Windows 版本！",
        "en_US": "Invalid Windows version!"
    },

    "uselocal": {
        "zh_CN": "使用本地存档：",
        "zh_TW": "使用本地存檔：",
        "en_US": "Use local saved: "
    },

    "collectin": {
        "zh_CN": "正在下载 ",
        "zh_TW": "正在下載 ",
        "en_US": "Collecting "
    },

    "noverfd": {
        "zh_CN": "找不到！",
        "zh_TW": "找不到！",
        "en_US": "Not found!"
    },

    "noie": {
        "zh_CN": "未连接到互联网！",
        "zh_TW": "未連接到互聯網！",
        "en_US": "No internet connection!"
    },

    "timeout": {
        "zh_CN": "超时！",
        "zh_TW": "超時！",
        "en_US": "Timeout!"
    },

    "unkerr": {
        "zh_CN": "发生未知错误！",
        "zh_TW": "發生未知錯誤！",
        "en_US": "Unknown error occurred!"
    },

    "dlfail": {
        "zh_CN": "下载失败！",
        "zh_TW": "下載失敗！",
        "en_US": "Download failed!"
    },

    "stat": {
        "zh_CN": "状态码：",
        "zh_TW": "狀態碼：",
        "en_US": "status code: "
    },

    "procerr": {
        "zh_CN": "在创建进程时发生错误：",
        "zh_TW": "在創建進程時發生錯誤：",
        "en_US": "An error occurred while create process: "
    },

    "exiterr": {
        "zh_CN": "在获取返回码时发生错误：",
        "zh_TW": "在獲取返回碼時發生錯誤：",
        "en_US": "An error occurred while get exit code: "
    },

    "pkgexist": {
        "zh_CN": "安装包已存在：",
        "zh_TW": "安裝包已存在：",
        "en_US": "Installer already exists: "
    },

    "lainst": {
        "zh_CN": "启动安装包中",
        "zh_TW": "啓動安裝包中",
        "en_US": "Launching installer"
    },

    "uninstsuc": {
        "zh_CN": "卸载成功！",
        "zh_TW": "解除安裝成功！",
        "en_US": "Uninstall success!"
    },

    "instsuc": {
        "zh_CN": "安装成功！",
        "zh_TW": "安裝成功！",
        "en_US": "Install success!"
    },

    "instcancel": {
        "zh_CN": "安装进程被用户取消！",
        "zh_TW": "安裝進程被用戶取消！",
        "en_US": "Installation cancelled by user!"
    },

    "anoinst": {
        "zh_CN": "另一个更新的版本已经安装过了！",
        "zh_TW": "另一個更新的版本已經安裝過了！",
        "en_US": "Another newer version had installed"
    },

    "occur": {
        "zh_CN": "发生错误！",
        "zh_TW": "發生錯誤！",
        "en_US": "An error occurred!"
    },

    "exit": {
        "zh_CN": "返回码：",
        "zh_TW": "返回碼：",
        "en_US": "exit code: "
    },

    "removin": {
        "zh_CN": "正在删除 ",
        "zh_TW": "正在刪除 ",
        "en_US": "Removing "
    },

    "rminsterr": {
        "zh_CN": "在删除安装包时发生错误！",
        "zh_TW": "在刪除安裝包時發生錯誤！",
        "en_US": "An error occurred while remove installer!"
    },

    "rmsuc": {
        "zh_CN": "删除成功！",
        "zh_TW": "刪除成功！",
        "en_US": "Remove success!"
    },

    "invsyn": {
        "zh_CN": "无效语法！如果您需要帮助，请尝试 \"impy help\" ！",
        "zh_TW": "無效語法！如果您需要幫助，請嘗試 \"impy help\" ！",
        "en_US": "Invalid syntax! If you need some help, try \"impy help\"!"
    },

    "threadnote": {
        "zh_CN": "自由线程仅支持 Python 3.13+",
        "zh_TW": "自由綫程僅支持 Python 3.13+",
        "en_US": "Free-threaded is only on Python 3.13+"
    },

    "ifaild": {
        "zh_CN": "如果失败，请尝试",
        "zh_TW": "如果失敗，請嘗試",
        "en_US": "If failed, try"
    },

    "modit": {
        "zh_CN": "来修改它！",
        "zh_TW": "來修改它！",
        "en_US": "to modify it!"
    },

    "instst": {
        "zh_CN": "请先尝试安装或添加一个版本！",
        "zh_TW": "請先嘗試安裝或添加一個版本！",
        "en_US": "Try to install or add a version first!"
    },

    "ferr": {
        "zh_CN": "格式无效！",
        "zh_TW": "格式無效！",
        "en_US": "Invalid format!"
    },

    "nwork": {
        "zh_CN": "无效！",
        "zh_TW": "無效！",
        "en_US": "does not work!"
    },

    "cantempty": {
        "zh_CN": "不能是空的！如果您需要帮助，请尝试 \"impy help\" ！",
        "zh_TW": "不能是空的！如果您需要幫助，請嘗試 \"impy help\" ！",
        "en_US": "Cannot be empty, if you need some help, try \"impy help\"!"
    },

    "showcmd": {
        "zh_CN": "显示所有可用的命令",
        "zh_TW": "顯示所有可用的命令",
        "en_US": "Show all available commands"
    },

    "impt": {
        "zh_CN": "ImPy 版本",
        "zh_TW": "ImPy 版本",
        "en_US": "ImPy version"
    },

    "cupd": {
        "zh_CN": "检查更新",
        "zh_TW": "檢查更新",
        "en_US": "Check update"
    },

    "rjson": {
        "zh_CN": "刷新 versions.json",
        "zh_TW": "刷新 versions.json",
        "en_US": "Reload versions.json"
    },

    "instpy": {
        "zh_CN": "安装 Python",
        "zh_TW": "安裝 Python",
        "en_US": "Install Python"
    },

    "allpy": {
        "zh_CN": "显示所有可用的 Python 版本",
        "zh_TW": "顯示所有可用的 Python 版本",
        "en_US": "Show all available Python"
    },

    "skipeol": {
        "zh_CN": "跳过所有停止支持的版本 (--skip-eol 也行)",
        "zh_TW": "跳過所有停止更新的版本 (--skip-eol 也行)",
        "en_US": "Skip all versions that end of life (or --skip-eol)"
    },

    "insthread": {
        "zh_CN": "安装包含自由线程的 Python (仅限 Python 3.13+)",
        "zh_TW": "安裝包含自由綫程的 Python (僅限 Python 3.13+)",
        "en_US": "Install Python with free-threaded build (only for Python 3.13+)"
    },

    "uninstpy": {
        "zh_CN": "卸载 Python (--uninstall 也行)",
        "zh_TW": "解除安裝 Python (--uninstall 也行)",
        "en_US": "Uninstall Python (or --uninstall)"
    },

    "insted": {
        "zh_CN": "已安装的 Python",
        "zh_TW": "已安裝的 Python",
        "en_US": "Installed Python"
    },

    "rminst": {
        "zh_CN": "删除安装包",
        "zh_TW": "刪除安裝包",
        "en_US": "Remove installer"
    },

    "runpy": {
        "zh_CN": "运行 Python",
        "zh_TW": "執行 Python",
        "en_US": "Run Python"
    },

    "like": {
        "zh_CN": "像",
        "zh_TW": "像",
        "en_US": "like"
    },

    "runpyt": {
        "zh_CN": "运行 Python 的自由线程构建",
        "zh_TW": "執行 Python 的自由綫程構建",
        "en_US": "Run Python free-threaded build"
    },

    "runpyw": {
        "zh_CN": "运行无弹窗的 Python",
        "zh_TW": "執行無彈窗的 Python",
        "en_US": "Run Python with no window"
    },

    "copy": {
        "zh_CN": "版权所有 © 2026 MBLC7. 保留所有权利.",
        "zh_TW": "版權所有 © 2026 MBLC7. 保留所有權利.",
        "en_US": "Copyright © 2026 MBLC7. All rights reserved."
    },

    "uptodate": {
        "zh_CN": "您的 ImPy 已是最新版本！",
        "zh_TW": "您的 ImPy 已是最新版本！",
        "en_US": "Your ImPy is up to date!"
    },

    "build": {
        "zh_CN": "构建 ",
        "zh_TW": "構建 ",
        "en_US": "build "
    },

    "future": {
        "zh_CN": "您的 ImPy 已是最新测试版！",
        "zh_TW": "您的 ImPy 已是最新測試版！",
        "en_US": "Your ImPy is the latest dev build!"
    },

    "compate": {
        "zh_CN": "您的 ImPy 虽然还兼容，但是还是推荐下载最新",
        "zh_TW": "您的 ImPy 雖然還兼容，但是還是推薦下載最新",
        "en_US": "Your ImPy is still compatible, but we recommend to update it to latest"
    },

    "excl": {
        "zh_CN": " ！",
        "zh_TW": " ！",
        "en_US": "!"
    },

    "iseol": {
        "zh_CN": "您的 ImPy 已停止支持，下载最新",
        "zh_TW": "您的 ImPy 已終止支援，下載最新",
        "en_US": "Your ImPy is end of life, update it to latest"
    },

    "oops": {
        "zh_CN": "哎呀！您的 ImPy 不在我们的更新历史上！",
        "zh_TW": "哎呀！您的 ImPy 不在我們的更新歷史上！",
        "en_US": "Oops! Your ImPy is not in our update history!"
    },

    "insthelpbar": {
        "zh_CN": "别名\t指向\n-----\t--------",
        "zh_TW": "別名\t指向\n-----\t--------",
        "en_US": "Alias\tRefer to\n-----\t--------"
    },

    "ngap": {
        "zh_CN": "\n\"-\" 只是间隔，不是版本号的一部分！\n例子：3.15.0-↵rc1 -> 3.15.0rc1",
        "zh_TW": "\n\"-\" 只是間隔，不是版本號的一部分！\n例子：3.15.0-↵rc1 -> 3.15.0rc1",
        "en_US": "\n\"-\" is gap, not part of version!\ne.g. 3.15.0-↵rc1 -> 3.15.0rc1"
    },

    "instverbar": {
        "zh_CN": "\n版本类别\t版本\n----------\t-------",
        "zh_TW": "\n版本類別\t版本\n----------\t-------",
        "en_US": "\nCategory\tVersion\n--------\t-------"
    },

    "eolw": {
        "zh_CN": "停止支持",
        "zh_TW": "終止支援",
        "en_US": "End of Life"
    },

    "latestw": {
        "zh_CN": "最新版本",
        "zh_TW": "最新版本",
        "en_US": "Latest"
    },

    "activew": {
        "zh_CN": "全面支持",
        "zh_TW": "全面支援",
        "en_US": "Active"
    },

    "securityw": {
        "zh_CN": "仅安全性",
        "zh_TW": "僅安全性",
        "en_US": "Security"
    },

    "unkver": {
        "zh_CN": "未知版本！请尝试 \"impy reld\" 来获取最新信息或 \"impy inst help\" 来获取所有可用版本列表！",
        "zh_TW": "未知版本！請嘗試 \"impy reld\" 來獲取最新訊息或 \"impy inst help\" 來獲取所有可用版本列表！",
        "en_US": "Unknown version! Try \"impy reld\" to fetch latest version updates or get available version list by \"impy inst help\"!"
    },

    "lsvap": {
        "zh_CN": "版本\t架构\t路径\n-------\t----\t----",
        "zh_TW": "版本\t架構\t路徑\n-------\t----\t----",
        "en_US": "Version\tArch\tPath\n-------\t----\t----"
    },

    "relsuc": {
        "zh_CN": "刷新成功！",
        "zh_TW": "刷新成功！",
        "en_US": "Reload success!"
    },

    "nothingrm": {
        "zh_CN": "无可删除项",
        "zh_TW": "無可刪除項",
        "en_US": "Nothing to remove"
    },

    "instofpy": {
        "zh_CN": "Python {} 的安装包",
        "zh_TW": "Python {} 的安裝包",
        "en_US": "installer of Python {}"
    },

    "brkeol": {
        "zh_CN": " (停止支持)",
        "zh_TW": " (終止支援)",
        "en_US": " (EOL)"
    },

    "brksec": {
        "zh_CN": " (仅安全性)",
        "zh_TW": " (僅安全性)",
        "en_US": " (Security)"
    }
}

def trans(id: str) -> str:
    return locmap[id][loc]

if machine().lower() not in ["amd64", "arm64"]:
    print(f"\033[0;33m{trans("unsarch")}{machine()}\033[0m")

v = getwindowsversion()
match (v.major, v.minor, v.build):
    case (5, 1, _):
        print(f"\033[0;33m{trans("unsupport")} Windows XP build {v.build}\033[0m")
    case (5, 2, _):
        print(f"\033[0;33m{trans("unsupport")} Windows XP build {v.build}\033[0m")
    case (6, 0, _):
        print(f"\033[0;33m{trans("unsupport")} Windows Vista build {v.build}\033[0m")
    case (6, 1, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 7 build {v.build}\033[0m")
    case (6, 2, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 8 build {v.build}\033[0m")
    case (6, 3, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 8.1 build {v.build}\033[0m")
    case (6, 4, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 10 build {v.build}\033[0m")
    case (10, 0, _):
        pass
    case _:
        print(f"\033[0;31m{trans("winverinvalid")}\033[0m")
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
impt = "26.1.1"

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
        with open(whereisjson, "r", encoding = "utf-8") as f:
            orig: dict = loads(f.read())

        if adds:
            orig |= creator
        else:
            orig.pop(version, None)
        with open(whereisjson, "w", encoding = "utf-8") as g:
            dump(orig, g, indent = 4)
    else:
        if adds:
            with open(whereisjson, "w", encoding = "utf-8") as f:
                dump(creator, f, indent = 4)
        else:
            with open(whereisjson, "w", encoding = "utf-8") as f:
                dump({}, f, indent = 4)

def getjson(jsonnm: str = "versions.json"):
    where = homepath / jsonnm
    wjson = f"{homeurl}/{jsonnm}"
    if where.exists():
        with open(where, "r", encoding = "utf-8") as f:
            old = load(f)
        
        try:
            d: dict = get(wjson).json()
            if d["meta"] > old["meta"]:
                print(f"{trans("collectin")}{jsonnm} ({d["meta"]})...")
                ret = _get(wjson, where, None)

                if isinstance(ret, int):
                    print(f"{trans("uselocal")}{where} ({old["meta"]})")
        except (exceptions.ConnectionError, exceptions.Timeout):
            print(f"{trans("uselocal")}{where} ({old["meta"]})")
    else:
        d = get(wjson).json()
        print(f"{trans("collectin")}{where} ({d["meta"]})")
        
        ret = _get(wjson, where, None)

        if isinstance(ret, int):
            if ret == 404:
                print(f"\033[0;31m{trans("noverfd")}\033[0m")
            elif ret == -1:
                print(f"\033[0;31m{trans("noie")}\033[0m")
            elif ret == -2:
                print(f"\033[0;31m{trans("timeout")}\033[0m")
            elif ret == -3:
                print(f"\033[0;31m{trans("unkerr")}\033[0m")
            else:
                print(f"\033[0;31m{trans("dlfail")} ({trans("stat")}{ret})\033[0m")
            exit(1)

    with open(where, "r", encoding = "utf-8") as f:
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
        print(f"\033[0;31m{trans("procerr")}{WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31m{trans("exiterr")}{WinError()}\033[0m")
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
        adds: bool = True,
        uninst: bool = False
    ) -> None:
    if filename.exists():
        print(f"{trans("pkgexist")}{filename}")
    else:
        print(f"{trans("collectin")}{filename if info is None else info}...")

        ret = _get(url, filename, params, timeout)
        
        if isinstance(ret, int):
            if ret == 404:
                print(f"\033[0;31m{trans("noverfd")}\033[0m")
            elif ret == -1:
                print(f"\033[0;31m{trans("noie")}\033[0m")
            elif ret == -2:
                print(f"\033[0;31m{trans("timeout")}\033[0m")
            elif ret == -3:
                print(f"\033[0;31m{trans("unkerr")}\033[0m")
            else:
                print(f"\033[0;31m{trans("dlfail")} ({trans("stat")}{ret})\033[0m")
            exit(1)

    print(f"{trans("lainst")}...")
    exit_code = pysetup(filename, switch)

    match exit_code:
        case 0:
            if uninst:
                print(trans("uninstsuc"))
            else:
                print(trans("instsuc"))
            whereisver = localprograms / "Python" / pythonfolder
            writemanage(pyver, whereisver, "x64", adds)
            exit(0)
        case 1223 | 1602:
            print(f"\033[0;31m{trans("instcancel")}\033[0m")
            exit(1)
        case 1638:
            print(f"\033[0;31m{trans("anoinst")}\033[0m")
            exit(1)
        case _:
            print(f"\033[0;31m{trans("occur")} ({trans("exit")}{exit_code})\033[0m")
            exit(1)

def remove(
        filename: str,
        info: str | None = None
    ) -> None:
    print(f"{trans("removin")}{info if info is not None else filename}")
    if not DeleteFileW(L(filename)):
        print(f"\033[0;31m{trans("rminsterr")}\033[0m")
        exit(1)
    else:
        print(trans("rmsuc"))
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

def run_python(exe_template: str, freethread: bool = False) -> None:
    where = homepath / "versions.json"
    if not where.exists():
        old = getjson()
    else:
        with open(where, "r", encoding = "utf-8") as f:
            old = load(f)

    try:
        v = args[1]
        freethread = freethread if freethread else v.endswith("t")
        exe_template = "python{v0}.{v1}t.exe" if freethread else exe_template
        v = v.removesuffix("t") if v.endswith("t") else v
    except IndexError:
        print(f"\033[0;31m{trans("invsyn")}\033[0m")
        exit(1)

    v = old["alias"][v] if v in old["alias"] else v

    if freethread:
        if v not in old["freethread"]:
            print(f"\033[0;31m{trans("threadnote")}\033[0m")
            exit(1)
        print(f"\033[0;33m{trans("ifaild")} \"impy install {args[1].removesuffix("t")}t\" {trans("modit")}\033[0m")

    whereisjson: Path = homepath / "manage.json"
    if not whereisjson.exists():
        print(f"\033[0;31m{trans("instst")}\033[0m")
        exit(1)

    with open(whereisjson, "r", encoding = "utf-8") as f:
        pyaaa: dict = loads(f.read())
    
    try:
        w = pyaaa[v]["path"]
    except KeyError:
        print(f"\033[0;31m{trans("ferr")}\033[0m")
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
        print(f"\033[0;31m{trans("procerr")}{WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31m{trans("exiterr")}{WinError()}\033[0m")
            exit(1)
        if exit_code.value != 0:
            print(f"\033[0;31m\"{" ".join(args)}\"{trans("nwork")} ({trans("exit")} {exit_code.value})\033[0m")
    finally:
        CloseHandle(pi.hProcess)
        CloseHandle(pi.hThread)

if __name__ == "__main__":
    if args == []:
        print(f"\033[0;31m{trans("cantempty")}\033[0m")
        exit(1)

    match args[0]:
        case "help":
            print(f"help\t{trans("showcmd")}")
            print(f"about\t{trans("impt")}")
            print(f"upd\t{trans("cupd")}")
            print(f"reld\t{trans("rjson")}")
            print(f"inst\t{trans("instpy")}")
            print(f"\thelp\t{trans("allpy")}")
            print(f"\t\t-s\t{trans("skipeol")}")
            print(f"\t(V)\t{trans("instpy")}")
            print(f"\t(V)t\t{trans("insthread")}")
            print(f"\t(V) -u\t{trans("uninstpy")}")
            print(f"ls\t{trans("insted")}")
            print(f"del\t{trans("rminst")}")
            print(f"\t(V)\t{trans("rminst")}")
            print(f"py\t{trans("runpy")} ({trans("like")} \"impy python 3.13 -m pip install pygame\")")
            print(f"\t(V)\t{trans("runpy")}")
            print(f"\t(V)t\t{trans("runpyt")}")
            print(f"pyw\t{trans("runpyw")}")
            print(f"\t(V)\t{trans("runpyw")}")

        case "about":
            print(f"ImPy {impt} [Inno Setup 7.1.0, MSVC 19.51.36256, Python 3.13.15]\n{trans("copy")}")

        case "upd":
            old = getjson()
            match impt:
                case x if x == old["update"]["dev"]:
                    print(f"\033[1;36m‼ {trans("future")} ({trans("build")} {x})\033[0m")
                case x if x == old["update"]["new"]:
                    print(f"\033[0;32m√ {trans("uptodate")} ({trans("build")}{x})\033[0m")
                case x if impt in old["update"]["compate"]:
                    print(f"\033[0;33m! {trans("compate")} {old['update']['new']}{trans("excl")}\033[0m")
                case x if impt in old["update"]["expires"]:
                    print(f"\033[0;31m× {trans("iseol")} {old['update']['new']}{trans("excl")}\033[0m")
                case _:
                    print(f"\033[0;31m× {trans("oops")}\033[0m")

        case "inst":
            old = getjson()
            try:
                a = args[1]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
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
                print(trans("insthelpbar"))
                for k, v in old["alias"].items():
                    if v in old["eol"] and skip_eol:
                        continue
                    if len(k) > 7:
                        print(f"{k[:6]}-\t{v}")
                        print(k[6:])
                    else:
                        print(f"{k}\t{v}")
                print(trans("ngap"))
                print(trans("instverbar"))

                s: int = 0
                for i in a:
                    match i:
                        case x if x in old["eol"]:
                            if skip_eol:
                                continue
                            cat = f"\033[0;31m× {trans("eolw")}\033[0m"
                            s += 1
                        case x if x in old["active"]:
                            if x in old["latest"]:
                                cat = f"\033[1;36m‼ {trans("latestw")}\033[0m"
                            else:
                                cat = f"\033[0;32m√ {trans("activew")}\033[0m"
                            s += 1
                        case x if x in old["security"]:
                            cat = f"\033[0;33m! {trans("securityw")}\033[0m"
                            s += 1
                        case _:
                            print(f"\033[0;31m{trans("ferr")}\033[0m")
                            exit(1)
                    print(f"{cat}\t{i}")
                print(f"{s} version in total")
                for c in old["credits"][loc]:
                    match loc:
                        case "zh_CN":
                            print(f"\n感谢 {c['name']} {c['info']}！")
                        case "zh_TW":
                            print(f"\n感謝 {c['name']} {c['info']}！")
                        case _:
                            print(f"\nThanks {c['name']} for {c['info']}!")
            else:
                try:
                    v = args[1]
                except:
                    print(f"\033[0;31m{trans("invsyn")}\033[0m")
                    exit(1)
                tswit = v.endswith("t")
                v = v.removesuffix("t") if v.endswith("t") else v
                syn = old["eol"] + old["security"] + old["active"]

                v = old["alias"][v] if v in old["alias"] else v
                if v not in syn:
                    print(f"\033[0;31m{trans("unkver")}\033[0m")
                    exit(1)
                fn = f"python-{v}-amd64.exe"
                shouldfn = setups / fn
                ques: bool = True
                uninst: bool = False
                try:
                    match args[2:]:
                        case x if "--uninstall" in x or "-u" in x:
                            switch = " /uninstall"
                            uninst = True
                            ques = False
                        case x if tswit:
                            switch = " /passive Include_pip=1 Include_freethreaded=1"
                        case _:
                            switch = " /passive Include_pip=1"
                except IndexError:
                    switch = " /passive Include_pip=1"
                
                if v in old["eol"]:
                    spec = v + trans("brkeol")
                elif v in old["security"]:
                    spec = v + trans("brksec")
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
                    ques,
                    uninst
                )

        case "ls":
            whereisjson: Path = homepath / "manage.json"
            if not whereisjson.exists():
                print(f"\033[0;31m{trans("instst")}\033[0m")
                exit(1)

            with open(whereisjson, "r", encoding = "utf-8") as f:
                c: dict = loads(f.read())
            if c == {}:
                print(f"\033[0;31m{trans("ferr")}\033[0m")
                exit(1)
            print(trans("lsvap"))
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

            print(trans("ngap"))

        case "reld":
            try:
                getjson()
                print(trans("relsuc"))

            except Exception as e:
                print(f"\033[0;31m{trans("unkerr")} ({e})\033[0m")

        case "py":
            run_python("python.exe")

        case "pyw":
            run_python("pythonw.exe")

        case "del":
            where = homepath / "versions.json"
            if not where.exists():
                old = getjson()
            else:
                with open(where, "r", encoding = "utf-8") as f:
                    old = load(f)
            try:
                v = args[1]
            except:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)

            v = old["alias"][v] if v in old["alias"] else v
            instr = setups / f"python-{v}-amd64.exe"
            if not instr.exists():
                print(trans("nothingrm"))
            else:
                if v in old["eol"]:
                    spec = v + trans("brkeol")
                elif v in old["security"]:
                    spec = v + trans("brksec")
                else:
                    spec = v
                remove(str(instr), trans("instofpy").format(spec))
    
        case _:
            print(f"\033[0;31m{trans("invsyn")}\033[0m")
            exit(1)