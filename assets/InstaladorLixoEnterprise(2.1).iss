; Inno Setup script — instala Cthulhu + fonte + pasta de fichas com arquivos

[Setup]
AppName=LixoEnterprise Cthulhu
AppVersion=2.1
DefaultDirName={pf}\LixoEnterprise
DefaultGroupName=LixoEnterprise
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=LixoEnterpriseSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; Executável principal
Source: "../dist/cthulhu.exe"; DestDir: "{app}"; Flags: ignoreversion

; Fonte TrueType (instala no Windows\Fonts)
Source: "MetalMania.ttf"; DestDir: "{fonts}"; FontInstall: "Metal Mania"; Flags: onlyifdoesntexist uninsneveruninstall

; Arquivos de fichas (exemplo com selected.json)
Source: "../fichas/selected.json"; DestDir: "{app}\fichas"; Flags: ignoreversion

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\Cthulhu"; Filename: "{app}\cthulhu.exe"; WorkingDir: "{app}"; IconFilename: "{app}\cthulhu.exe"
; Atalho na Área de Trabalho
Name: "{commondesktop}\Cthulhu"; Filename: "{app}\cthulhu.exe"; WorkingDir: "{app}"; IconFilename: "{app}\cthulhu.exe"

[Run]
; Executa opcionalmente após instalação
Filename: "{app}\cthulhu.exe"; Description: "Executar Cthulhu agora"; Flags: nowait postinstall skipifsilent
