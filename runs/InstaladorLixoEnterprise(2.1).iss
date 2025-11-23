; Inno Setup script — instala Cthulhu + fonte + pasta de fichas com arquivos

[Setup]
AppName=LixoEnterprise Cthulhu
AppVersion=2.2
DefaultDirName={commonpf}\LixoEnterprise
DefaultGroupName=LixoEnterprise
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=LixoEnterpriseSetup
Compression=zip
SolidCompression=no
PrivilegesRequired=admin

; --- Arquivos ---
[Files]
; Executável principal
Source: "../dist/cthulhu.exe"; DestDir: "{app}"; Flags: ignoreversion

; Fonte TrueType (instala no Windows\Fonts)
Source: "MetalMania.ttf"; DestDir: "{commonfonts}"; FontInstall: "Metal Mania"; Flags: onlyifdoesntexist uninsneveruninstall

; Arquivos de fichas
Source: "../fichas\*"; DestDir: "{app}\fichas"; Flags: ignoreversion recursesubdirs

; --- Ícones ---
[Icons]
; Atalho no Menu Iniciar
Name: "{group}\Cthulhu"; Filename: "{app}\cthulhu.exe"; WorkingDir: "{app}"; IconFilename: "{app}\cthulhu.exe"
; Atalho na Área de Trabalho
Name: "{commondesktop}\Cthulhu"; Filename: "{app}\cthulhu.exe"; WorkingDir: "{app}"; IconFilename: "{app}\cthulhu.exe"

; --- Execução pós-instalação ---
[Run]
Filename: "{app}\cthulhu.exe"; Description: "Executar Cthulhu agora"; Flags: nowait postinstall skipifsilent
