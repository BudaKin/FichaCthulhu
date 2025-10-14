# FichasCthulhu

Obs: feito inteiramente em IA, porém revisado por mim, o dono do repositório.

Este projeto é um editor de fichas para RPG que utiliza um sistema baseado em Call of Cthulhu, feito em Python com interface gráfica usando Tkinter e ttkbootstrap. Abaixo está a explicação das principais partes do projeto:

## Estrutura de Pastas

- **main.py**: Arquivo principal que inicializa a aplicação.
- **README.md**: Este arquivo de documentação.
- **assets/**: Pasta para arquivos estáticos, como ícones.
- **core/**: Lógica central do sistema.
  - `data.py`: Define atributos e perícias do sistema.
  - `dice.py`: Funções para rolagem e avaliação de dados.
  - `storage.py`: Funções para salvar e carregar dados das fichas.
- **fichas/**: Pasta onde as fichas dos personagens são salvas.
- **temp/**: Protótipos e versões antigas de telas e funcionalidades.
  - `main_window.py`: Versão antiga da janela principal.
  - `novo.py`: Protótipos de novas funcionalidades.
- **ui/**: Interface gráfica do usuário.
  - `main_window.py`: Janela principal do sistema, agora com abas para cada tela.
  - `autocomplete.py`: Campo de texto com autocompletar para facilitar preenchimento.
  - `components.py`: Componentes reutilizáveis da interface (ex: caixas de texto com rolagem).
  - `dialogs.py`: Diálogos personalizados para interação com o usuário.
  - `tela_ficha.py`: Tela de edição da ficha principal do personagem.
  - `tela_info.py`: Tela de informações adicionais do personagem.
  - `tela_rituais.py`: Tela para gerenciamento de rituais do personagem.

## Funcionalidades

- **Editor de Fichas**: Permite criar, editar, salvar e carregar fichas de personagens.
- **Abas**: As telas principais (Ficha, Info, Rituais) são divididas em abas para facilitar a navegação.
- **Rolagem de Dados**: Função para rolar dados diretamente pela interface, com histórico de rolagens.
- **Autocompletar**: Campos de texto inteligentes para agilizar o preenchimento de informações.
- **Exportação**: Permite exportar a ficha em formato texto.
- **Armazenamento**: As fichas são salvas em arquivos JSON na pasta `fichas`.

## Como usar

1. Execute o `main.py` para abrir o editor.
2. Preencha os dados do personagem nas abas.
3. Use os botões para salvar, carregar, exportar ou rolar dados.

---