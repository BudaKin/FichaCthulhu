;--------------------------------
; NSIS Installer para cthulhu.exe
;--------------------------------

; Nome do instalador final
OutFile "installer.exe"

; Diretório padrão de instalação
InstallDir "$PROGRAMFILES\LixoEnterprise"

; Solicitar permissão de administrador
RequestExecutionLevel admin

; Páginas do instalador
Page directory
Page instfiles

; Seção principal
Section "Install"

  ; Cria pasta de instalação
  SetOutPath "$INSTDIR"

  ; Copia o executável
  File "dist\cthulhu.exe"

  ; Copia a pasta de assets
  File /r "dist\assets\*.*"

  ; Cria atalho no menu iniciar
  CreateShortCut "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk" "$INSTDIR\cthulhu.exe"

SectionEnd

; Seção de desinstalação
Section "Uninstall"

  ; Remove executável
  Delete "$INSTDIR\cthulhu.exe"

  ; Remove pasta de assets
  RMDir /r "$INSTDIR\assets"

  ; Remove atalho
  Delete "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk"

  ; Remove pasta de instalação se estiver vazia
  RMDir "$INSTDIR"
  RMDir "$SMPROGRAMS\LixoEnterprise"

SectionEnd
