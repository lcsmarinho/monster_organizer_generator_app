# Gerenciador de Monstros D&D

Bem-vindo, aventureiro! Este projeto é um aplicativo Python com interface gráfica (Tkinter) que auxilia na gestão e edição dos monstros que habitam suas campanhas de Dungeons & Dragons. Entre nesse calabouço digital e prepare-se para organizar, modificar e expandir o seu bestiário com praticidade e estilo (sem exageros temáticos, afinal, a magia está na funcionalidade).

## Funcionalidades

- **Carregamento Automático do Histórico:**  
  Ao iniciar, o aplicativo procura pelo arquivo `historico_monstros.json` e carrega os monstros previamente salvos, permitindo que você continue suas aventuras sem perder registros.

- **Seleção e Carregamento de Arquivo JSON:**  
  Escolha o arquivo base (ex.: `monstros.json`) que contém os monstros atuais e visualize-os na aba "Monstros do Arquivo".

- **Formulário para Adição de Monstros:**  
  Preencha os dados de cada monstro por meio de um formulário intuitivo. Cada campo possui uma checkbox "Não tem" que, quando marcada, insere um valor padrão (por exemplo, "0" para campos numéricos e "nenhum" para os demais), garantindo que nenhum atributo seja deixado vazio.

- **Edição via Pop-Up:**  
  Dê um duplo clique em um monstro (seja na lista do JSON atual ou no histórico) para abrir uma janela de edição. Atualize os atributos conforme necessário e salve as alterações com facilidade.

- **Gerenciamento do Bestiário:**  
  - Na aba "Monstros do Arquivo": Você pode excluir monstros diretamente do JSON atual.
  - Na aba "Monstros Adicionados": Utilize os botões "Adicionar ao JSON" para inserir um monstro do histórico no arquivo atual ou "Excluir" para removê-lo do histórico.

- **Geração de Novo Arquivo:**  
  Ao finalizar suas modificações, clique em "Gerar Arquivo". Um resumo amigável das alterações (monstros modificados e adicionados) será apresentado em um pop-up, confirmando que o arquivo original não será sobrescrito, mas sim que um novo arquivo será criado.

- **Suporte ao Scroll do Mouse:**  
  Navegue facilmente pelos formulários e pop-ups usando o scroll do mouse, garantindo uma experiência de uso confortável mesmo em sessões intensas de edição.

## Como Usar

1. **Inicie o Aplicativo:**  
   Execute o script Python. Se o arquivo `historico_monstros.json` existir, seus monstros serão carregados automaticamente na aba "Monstros Adicionados".

2. **Selecione o Arquivo Base:**  
   Clique no botão **"Selecionar Arquivo .json"** e escolha o arquivo que contém seus monstros atuais. Os monstros serão exibidos na aba "Monstros do Arquivo".

3. **Adicione um Novo Monstro:**  
   Preencha o formulário à esquerda com os atributos do monstro. Marque a checkbox "Não tem" para os campos que não se aplicam, e clique em **"Adicionar Monstro"** para salvá-lo no histórico.

4. **Edite os Monstros:**  
   Dê duplo clique em qualquer monstro (na lista do arquivo ou do histórico) para editar seus atributos por meio do pop-up de edição.

5. **Gerencie o Bestiário:**  
   Use os botões **"Excluir"** e **"Adicionar ao JSON"** nas respectivas abas para remover ou incorporar monstros conforme a necessidade da sua campanha.

6. **Gere o Novo Arquivo:**  
   Clique em **"Gerar Arquivo"**. Um resumo das alterações será exibido e, ao confirmar, um novo arquivo será criado (com o nome original acrescido de `_novos_monstros.json`), preservando o arquivo original.

7. **Finalizando a Jornada:**  
   Ao fechar o aplicativo, o histórico dos monstros adicionados será salvo automaticamente em `historico_monstros.json`.

## Requisitos

- **Python 3.x**  
- **Tkinter** (geralmente incluído na instalação padrão do Python)  
- Um editor de texto ou IDE de sua preferência para visualizar e editar o código.

## Como Executar

1. Clone ou baixe o repositório.
2. Abra o terminal (ou prompt de comando) na pasta do projeto.
3. Execute o comando:

   ```bash
   python main.py
