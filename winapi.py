import ctypes as __CTYPES

ptr = __CTYPES.POINTER
struct = __CTYPES.Structure
et = __CTYPES.byref
sizeof = __CTYPES.sizeof
WinError = __CTYPES.WinError
def L(value: str, size: int | None = None) -> __CTYPES.c_wchar_p:
    return __CTYPES.cast(
        __CTYPES.create_unicode_buffer(value, size),
        __CTYPES.c_wchar_p
    )

__KERNEL32 = __CTYPES.windll.kernel32
__DWMAPI = __CTYPES.windll.dwmapi
__USER32 = __CTYPES.windll.user32
__SHELL32 = __CTYPES.windll.shell32

CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_CONSOLE = 0x00000010
DETACHED_PROCESS = 0x00000008
CREATE_UNICODE_ENVIRONMENT = 0x00000400
DEBUG_ONLY_THIS_PROCESS = 0x00000002
CREATE_SUSPENDED = 0x00000004
DEBUG_PROCESS = 0x00000001
MAX_PATH = 0x00000104
INFINITY = 0xFFFFFFFF

INT = __CTYPES.c_int
UINT = __CTYPES.c_uint
WORD = __CTYPES.c_ushort
DWORD = __CTYPES.c_ulong
LPDWORD = ptr(DWORD)
LPWSTR = __CTYPES.c_wchar_p
LPCWSTR = __CTYPES.c_wchar_p
BOOL = __CTYPES.c_int
LPVOID = __CTYPES.c_void_p
LPCVOID = __CTYPES.c_void_p
BYTE = __CTYPES.c_byte
LPBYTE = ptr(BYTE)
WCHAR = __CTYPES.c_wchar
HANDLE = __CTYPES.c_void_p
HWND = HANDLE
LONG = __CTYPES.c_long
HRESULT = LONG
LONG_PTR = __CTYPES.c_longlong
LRESULT = LONG
ULONG_PTR = __CTYPES.c_ulonglong
WPARAM = ULONG_PTR
LPARAM = LONG_PTR
PCWSTR = __CTYPES.c_wchar_p
COLORREF = DWORD
LONGLONG = __CTYPES.c_longlong
ULONGLONG = __CTYPES.c_ulonglong

class tagRECT(struct):
    _fields_ = [
        ("left", LONG),
        ("top", LONG),
        ("right", LONG),
        ("bottom", LONG)
    ]
RECT = tagRECT
LPRECT = ptr(RECT)

class _MARGINS(struct):
    _fields_ = [
        ("cxLeftWidth", INT),
        ("cxRightWidth", INT),
        ("cyTopHeight", INT),
        ("cyBottomHeight", INT)
    ]
MARGINS = _MARGINS
PMARGINS = ptr(MARGINS)

class _SECURITY_ATTRIBUTES(struct):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", LPVOID),
        ("bInheritHandle", BOOL)
    ]
SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = ptr(SECURITY_ATTRIBUTES)

class _STARTUPINFOW(struct):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR),
        ("lpTitle", LPWSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE)
    ]
STARTUPINFOW = _STARTUPINFOW
LPSTARTUPINFOW = ptr(STARTUPINFOW)

class _PROCESS_INFORMATION(struct):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]
PROCESS_INFORMATION = _PROCESS_INFORMATION
LPPROCESS_INFORMATION = ptr(PROCESS_INFORMATION)

class _FILETIME(struct):
    _fields_ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD)
    ]
FILETIME = _FILETIME

class _WIN32_FIND_DATAW(struct):
    _fields_ = [
        ("dwFileAttributes", DWORD),
        ("ftCreationTime", FILETIME),
        ("ftLastAccessTime", FILETIME),
        ("ftLastWriteTime", FILETIME),
        ("nFileSizeHigh", DWORD),
        ("nFileSizeLow", DWORD),
        ("dwReserved0", DWORD),
        ("dwReserved1", DWORD),
        ("cFileName", WCHAR * MAX_PATH),
        ("cAlternateFileName", WCHAR * 14),
        # ("dwFileType", DWORD),
        # ("dwCreatorType", DWORD),
        # ("wFinderFlags", WORD)
    ]
WIN32_FIND_DATAW = _WIN32_FIND_DATAW
LPWIN32_FIND_DATAW = ptr(WIN32_FIND_DATAW)

__KERNEL32.CreateProcessW.argtypes = [
    LPCWSTR,
    LPWSTR,
    LPSECURITY_ATTRIBUTES,
    LPSECURITY_ATTRIBUTES,
    BOOL,
    DWORD,
    LPVOID,
    LPCWSTR,
    LPSTARTUPINFOW,
    LPPROCESS_INFORMATION
]
__KERNEL32.CreateProcessW.restype = BOOL
def CreateProcessW(
        lpApplicationName: LPCWSTR,
        lpCommandLine: LPWSTR,
        lpProcessAttributes: LPSECURITY_ATTRIBUTES, # type: ignore
        lpThreadAttributes: LPSECURITY_ATTRIBUTES, # type: ignore
        bInheritHandles: BOOL,
        dwCreationFlags: DWORD,
        lpEnvironment: LPVOID,
        lpCurrentDirectory: LPCWSTR,
        lpStartupInfo: LPSTARTUPINFOW, # type: ignore
        lpProcessInformation: LPPROCESS_INFORMATION # type: ignore
) -> BOOL:
    return __KERNEL32.CreateProcessW(
        lpApplicationName,
        lpCommandLine,
        lpProcessAttributes,
        lpThreadAttributes,
        bInheritHandles,
        dwCreationFlags,
        lpEnvironment,
        lpCurrentDirectory,
        lpStartupInfo,
        lpProcessInformation
    )

__KERNEL32.WaitForSingleObject.argtypes = [
    HANDLE,
    DWORD
]
__KERNEL32.WaitForSingleObject.restype = DWORD
def WaitForSingleObject(
        hHandle: HANDLE,
        dwMilliseconds: DWORD
) -> DWORD:
    return __KERNEL32.WaitForSingleObject(
        hHandle,
        dwMilliseconds
    )

__KERNEL32.TerminateProcess.argtypes = [
    HANDLE,
    UINT
]
__KERNEL32.TerminateProcess.restype = BOOL
def TerminateProcess(
        hProcess: HANDLE,
        uExitCode: UINT
) -> BOOL:
    return __KERNEL32.TerminateProcess(
        hProcess,
        uExitCode
    )

__KERNEL32.FindFirstFileW.argtypes = [
    LPCWSTR,
    LPWIN32_FIND_DATAW
]
__KERNEL32.FindFirstFileW.restype = HANDLE
def FindFirstFileW(
        lpFileName: LPCWSTR,
        lpFindFileData: LPWIN32_FIND_DATAW # type: ignore
) -> HANDLE:
    return __KERNEL32.FindFirstFileW(
        lpFileName,
        lpFindFileData
    )

__KERNEL32.RemoveDirectoryW.argtypes = [
    LPCWSTR
]
__KERNEL32.RemoveDirectoryW.restype = BOOL
def RemoveDirectoryW(
        lpPathName: LPCWSTR
) -> BOOL:
    return __KERNEL32.RemoveDirectoryW(
        lpPathName
    )

__KERNEL32.CreateDirectoryW.argtypes = [
    LPCWSTR,
    LPSECURITY_ATTRIBUTES
]
__KERNEL32.CreateDirectoryW.restype = BOOL
def CreateDirectoryW(
        lpPathName: LPCWSTR,
        lpSecurityAttributes: LPSECURITY_ATTRIBUTES # type: ignore
) -> BOOL:
    return __KERNEL32.CreateDirectoryW(
        lpPathName,
        lpSecurityAttributes
    )

__KERNEL32.DeleteFileW.argtypes = [
    LPCWSTR
]
__KERNEL32.DeleteFileW.restype = BOOL
def DeleteFileW(
        lpFileName: LPCWSTR
) -> BOOL:
    return __KERNEL32.DeleteFileW(
        lpFileName
    )

__KERNEL32.CreateFileW.argtypes = [
    LPCWSTR,
    DWORD,
    DWORD,
    LPSECURITY_ATTRIBUTES,
    DWORD,
    DWORD,
    HANDLE
]
__KERNEL32.CreateFileW.restype = HANDLE
def CreateFileW(
        lpFileName: LPCWSTR,
        dwDesiredAccess: DWORD,
        dwShareMode: DWORD,
        lpSecurityAttributes: LPSECURITY_ATTRIBUTES, # type: ignore
        dwCreationDisposition: DWORD,
        dwFlagsAndAttributes: DWORD,
        hTemplateFile: HANDLE
) -> HANDLE:
    return __KERNEL32.CreateFileW(
        lpFileName,
        dwDesiredAccess,
        dwShareMode,
        lpSecurityAttributes,
        dwCreationDisposition,
        dwFlagsAndAttributes,
        hTemplateFile
    )

__KERNEL32.FindClose.argtypes = [
    HANDLE
]
__KERNEL32.FindClose.restype = BOOL
def FindClose(
        hFindFile: HANDLE
) -> BOOL:
    return __KERNEL32.FindClose(
        hFindFile
    )

__KERNEL32.FindNextFileW.argtypes = [
    HANDLE,
    LPWIN32_FIND_DATAW
]
__KERNEL32.FindNextFileW.restype = BOOL
def FindNextFileW(
        hFindFile: HANDLE,
        lpFindFileData: LPWIN32_FIND_DATAW # type: ignore
) -> BOOL:
    return __KERNEL32.FindNextFileW(
        hFindFile,
        lpFindFileData
    )

__KERNEL32.CloseHandle.argtypes = [
    HANDLE
]
__KERNEL32.CloseHandle.restype = BOOL
def CloseHandle(
        hObject: HANDLE
) -> BOOL:
    return __KERNEL32.CloseHandle(
        hObject
    )

__DWMAPI.DwmSetWindowAttribute.argtypes = [
    HWND,
    DWORD,
    LPCVOID,
    DWORD
]
__DWMAPI.DwmSetWindowAttribute.restype = HRESULT
def DwmSetWindowAttribute(
        hwnd: HWND,
        dwAttribute: DWORD,
        pvAttribute: LPCVOID,
        cbAttribute: DWORD
) -> HRESULT:
    return __DWMAPI.DwmSetWindowAttribute(
        hwnd,
        dwAttribute,
        pvAttribute,
        cbAttribute
    )

__USER32.ReleaseCapture.argtypes = []
__USER32.ReleaseCapture.restype = BOOL
def ReleaseCapture() -> BOOL:
    return __USER32.ReleaseCapture()

__USER32.SendMessageW.argtypes = [
    HWND,
    UINT,
    WPARAM,
    LPARAM
]
__USER32.SendMessageW.restype = LRESULT
def SendMessageW(
        hWnd: HWND,
        Msg: UINT,
        wParam: WPARAM,
        lParam: LPARAM
) -> LRESULT:
    return __USER32.SendMessageW(
        hWnd,
        Msg,
        wParam,
        lParam
    )

__USER32.GetWindowRect.argtypes = [
    HWND,
    LPRECT
]
__USER32.GetWindowRect.restype = BOOL
def GetWindowRect(
        hWnd: HWND,
        lpRect: LPRECT, # type: ignore
) -> BOOL:
    return __USER32.GetWindowRect(
        hWnd,
        lpRect
    )

__USER32.DefWindowProcW.argtypes = [
    HWND,
    UINT,
    WPARAM,
    LPARAM
]
__USER32.DefWindowProcW.restype = LRESULT
def DefWindowProcW(
        hWnd: HWND,
        Msg: UINT,
        wParam: WPARAM,
        lParam: LPARAM
) -> LRESULT:
    return __USER32.DefWindowProcW(
        hWnd,
        Msg,
        wParam,
        lParam
    )

__USER32.SetWindowLongPtrW.argtypes = [
    HWND,
    INT,
    LONG_PTR
]
__USER32.SetWindowLongPtrW.restype = LONG_PTR
def SetWindowLongPtrW(
        hWnd: HWND,
        nIndex: INT,
        dwNewLong: LONG_PTR
) -> LONG_PTR:
    return __USER32.SetWindowLongPtrW(
        hWnd,
        nIndex,
        dwNewLong
    )

__SHELL32.SetCurrentProcessExplicitAppUserModelID.argtypes = [
    PCWSTR
]
__SHELL32.SetCurrentProcessExplicitAppUserModelID.restype = HRESULT
def SetCurrentProcessExplicitAppUserModelID(
        AppID: PCWSTR
) -> HRESULT:
    return __SHELL32.SetCurrentProcessExplicitAppUserModelID(
        AppID
    )

__DWMAPI.DwmExtendFrameIntoClientArea.argtypes = [
    HWND,
    PMARGINS
]
__DWMAPI.DwmExtendFrameIntoClientArea.restype = HRESULT
def DwmExtendFrameIntoClientArea(
        hWnd: HWND,
        pMarInset: PMARGINS # type: ignore
) -> HRESULT:
    return __DWMAPI.DwmExtendFrameIntoClientArea(
        hWnd,
        pMarInset
    )

__USER32.SetLayeredWindowAttributes.argtypes = [
    HWND,
    COLORREF,
    BYTE,
    DWORD
]
__USER32.SetLayeredWindowAttributes.restype = BOOL
def SetLayeredWindowAttributes(
        hwnd: HWND,
        crKey: COLORREF,
        bAlpha: BYTE,
        dwFlags: DWORD
) -> BOOL:
    return __USER32.SetLayeredWindowAttributes(
        hwnd,
        crKey,
        bAlpha,
        dwFlags
    )

__USER32.GetWindowLongW.argtypes = [
    HWND,
    INT
]
__USER32.GetWindowLongW.restype = LONG
def GetWindowLongW(
        hWnd: HWND,
        nIndex: INT
) -> LONG:
    return __USER32.GetWindowLongW(
        hWnd,
        nIndex
    )

__USER32.SetWindowLongW.argtypes = [
    HWND,
    INT,
    LONG
]
__USER32.SetWindowLongW.restype = LONG
def SetWindowLongW(
        hWnd: HWND,
        nIndex: INT,
        dwNewLong: LONG
) -> LONG:
    return __USER32.SetWindowLongW(
        hWnd,
        nIndex,
        dwNewLong
    )

__KERNEL32.GetExitCodeProcess.argtypes = [
    HANDLE,
    LPDWORD
]
__KERNEL32.GetExitCodeProcess.restype = BOOL
def GetExitCodeProcess(
        hProcess: HANDLE,
        lpExitCode: LPDWORD # type: ignore
) -> BOOL:
    return __KERNEL32.GetExitCodeProcess(
        hProcess,
        lpExitCode
    )