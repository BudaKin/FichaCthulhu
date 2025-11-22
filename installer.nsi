;--------------------------------
; NSIS Installer para cthulhu.exe
;--------------------------------

; Nome do instalador
OutFile "installer.exe"

; Diretório padrão de instalação
InstallDir "$PROGRAMFILES\LixoEnterprise"

; Solicitar permissão de administrador
RequestExecutionLevel admin

; Página de boas-vindas e seleção de diretório
Page directory
Page instfiles

; Seção principal
Section "Install"

  ; Cria pasta de instalação
  SetOutPath "$INSTDIR"

  ; Copia o executável
  File "dist\cthulhu.exe"

  ; Cria atalho no menu iniciar
  CreateShortCut "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk" "$INSTDIR\cthulhu.exe"

SectionEnd

; Seção de desinstalação
Section "Uninstall"

  ; Remove executável
  Delete "$INSTDIR\cthulhu.exe"

  ; Remove atalho
  Delete "$SMPROGRAMS\LixoEnterprise\cthulhu.lnk"

  ; Remove pasta de instalação se estiver vazia
  RMDir "$INSTDIR"
  RMDir "$SMPROGRAMS\LixoEnterprise"

SectionEnd
