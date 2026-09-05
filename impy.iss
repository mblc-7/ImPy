[Setup]
AppName=ImPy
AppVersion=26.1
VersionInfoVersion=26.1.0.0
AppPublisher=MBLC7
AppCopyright=Copyright (C) 2026 MBLC7
DefaultDirName={commonpf}\ImPy
DefaultGroupName=ImPy
OutputDir=Output
OutputBaseFilename=ImPy-{#SetupSetting("AppVersion")}-x64
Compression=lzma2
SolidCompression=yes
ChangesEnvironment=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
SetupIconFile=impy.ico
UninstallDisplayIcon={app}\impy.exe

[Types]
Name: "full"; Description: "Full Installation"
Name: "compact"; Description: "Compact Installation"
Name: "custom"; Description: "Custom Installation"; Flags: iscustom

[Components]
Name: "main"; Description: "ImPy main source"; Types: full compact custom; Flags: fixed
Name: "build"; Description: "ImPy build source"; Types: full custom

[Files]
Source: "impy.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "build\*"; Components: main
Source: "impy.build\*"; DestDir: "{app}\build"; Flags: ignoreversion recursesubdirs; Components: build

[Icons]
Name: "{group}\Uninstall ImPy"; Filename: "{uninstallexe}"
Name: "{group}\ImPy"; Filename: "{app}\impy.exe"
Name: "{group}\ImPy Command Prompt Tools"; \
    Filename: "{cmd}"; \
    Parameters: "/k ""{app}\cpt.bat"""; \
    WorkingDir: "{app}"; \
    IconFilename: "{app}\impy.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"