#define MyAppName "FraudGuard Community"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "tuxmasterlnx13-art"
#define MyAppExeName "FraudGuardCommunity.exe"

[Setup]
AppId={{78A917A0-12C1-4BD0-A38A-247B20A6E496}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\FraudGuard Community
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=FraudGuard-Community-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\LICENSE
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "dist\FraudGuardCommunity\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FraudGuard Community"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\FraudGuard — acceso de empresa"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--lan"
Name: "{group}\FraudGuard — restablecer clave de empresa"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--lan --reset-access-key"
Name: "{autodesktop}\FraudGuard Community"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir FraudGuard Community"; Flags: nowait postinstall skipifsilent

