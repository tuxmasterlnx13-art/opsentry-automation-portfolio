#define MyAppName "GUARDIAN Community"
#define MyAppVersion "0.3.0"
#define MyAppPublisher "tuxmasterlnx13-art"
#define MyAppExeName "FraudGuardCommunity.exe"

[Setup]
AppId={{78A917A0-12C1-4BD0-A38A-247B20A6E496}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\GUARDIAN Community
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=Guardian-Community-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=LICENSE_INSTALLER_ES.txt
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Messages]
WelcomeLabel1=Bienvenido a GUARDIAN Community
WelcomeLabel2=GUARDIAN revisa archivos de operaciones y muestra señales que merecen investigación.%n%nFunciona localmente: tus datos no se envían a Internet.%n%nPulsa Siguiente para instalarlo. No necesitas saber programación.
LicenseLabel3=Resumen: GUARDIAN es gratuito y de código abierto. Marca «Acepto el acuerdo» para continuar. El texto legal MIT aparece debajo.

[Files]
Source: "dist\FraudGuardCommunity\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GUARDIAN Community"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\GUARDIAN — acceso de empresa"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--lan"
Name: "{group}\GUARDIAN — restablecer clave de empresa"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--lan --reset-access-key"
Name: "{autodesktop}\GUARDIAN Community"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir GUARDIAN Community"; Flags: nowait postinstall skipifsilent

