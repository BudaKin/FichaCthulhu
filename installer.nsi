OutFile "installer.exe"
InstallDir "$PROGRAMFILES\LixoEnterprise"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"

  ; Copia o executável
  File "LixoEnterprise\cthulhu.exe"

  ; Copia a pasta de assets se existir arquivos
  IfFileExists "LixoEnterprise\assets\*.*" +2 0
    File /r /nonfatal "LixoEnterprise\assets\*.*"

  ; Cria atalho no menu iniciar
  CreateShortCut "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk" "$INSTDIR\cthulhu.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\cthulhu.exe"
  RMDir /r "$INSTDIR\assets"
  Delete "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk"
  RMDir "$INSTDIR"
  RMDir "$SMPROGRAMS\LixoEnterprise"
SectionEnd
