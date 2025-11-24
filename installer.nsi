!include "MUI2.nsh"

Name "LixoEnterprise"
OutFile "LixoEnterpriseInstaller.exe"
InstallDir "$PROGRAMFILES\LixoEnterprise"
RequestExecutionLevel admin

Icon "assets\cthulhu.ico"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "Install"
  SetOutPath "$INSTDIR"

  ; Copia o executável compilado
  File "LixoEnterprise\cthulhu.exe"

  ; Copia assets inteiros (ícone, imagens, fonte etc)
  SetOutPath "$INSTDIR\assets"
  File /r "LixoEnterprise\assets\*.*"

  ; Instala fonte MetalMania
  SetOutPath "$FONTS"
  File "LixoEnterprise\assets\MetalMania-Regular.ttf"
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
    "Metal Mania (TrueType)" "MetalMania-Regular.ttf"

  ; Atalho no menu iniciar
  CreateDirectory "$SMPROGRAMS\LixoEnterprise"
  CreateShortCut "$SMPROGRAMS\LixoEnterprise\Cthulhu.lnk" "$INSTDIR\cthulhu.exe"

  ; Atalho na área de trabalho (opcional)
  CreateShortCut "$DESKTOP\Cthulhu.lnk" "$INSTDIR\cthulhu.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\cthulhu.exe"
  RMDir /r "$INSTDIR\assets"
  
  ; Remove fonte
  Delete "$FONTS\MetalMania-Regular.ttf"
  DeleteRegValue HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
    "Metal Mania (TrueType)"

  ; Remove atalhos
  Delete "$SMPROGRAMS\LixoEnterprise\Cthulhu.lnk"
  RMDir "$SMPROGRAMS\LixoEnterprise"
  Delete "$DESKTOP\Cthulhu.lnk"

  RMDir "$INSTDIR"
SectionEnd