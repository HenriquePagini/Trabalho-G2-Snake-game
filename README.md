# 🐍 Rayquaza Snake

Jogo da cobrinha desenvolvido em **Python 3** com **PyGame** pelos alunos **Henrique Pagini** e **Pedro Algayer**, com tema
inspirado em Pokémon, como trabalho da disciplina de **Algoritmos e programação** (Python Crash — Prof. Filipo Novo Mór).

![status](https://img.shields.io/badge/status-funcionando-brightgreen)
![python](https://img.shields.io/badge/python-3.x-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

## 👥 Autores

- Henrique Pagini
- Pedro Algayer

## 🎮 Sobre o jogo

Controle o Rayquaza (a cobra) por um plano bidimensional, coma frutas para
crescer e ganhar pontos, e evite colidir com as bordas do mapa ou com o
próprio corpo. O jogo possui:

- **Movimento contínuo** via teclado (setas ou WASD).
- **Frutas aleatórias** com efeitos diferentes (crescimento, velocidade,
  pontos em dobro, encolhimento).
- **Item secundário opcional** que aparece de vez em quando na tela,
  incluindo a temida **Pokébomba** — pega quem quer arriscar mais pontos
  ou efeitos, mas **nunca obriga** o jogador a interagir com ela.
- **Placar em tempo real** e recorde da sessão.
- **Níveis de dificuldade crescente** (velocidade aumenta conforme a
  pontuação sobe) — *bônus do trabalho*.
- **Efeitos sonoros** para comer, colidir e pegar itens especiais —
  *bônus do trabalho*.
- Tela inicial, tela de pausa e tela de game over com opção de reinício.

## 🛠 Requisitos técnicos

- Python 3.x
- [PyGame](https://www.pygame.org/) para os gráficos e o loop do jogo
- [Pillow](https://pillow.readthedocs.io/) — usado apenas para *gerar
  sprites de fallback* automaticamente caso alguma imagem em `imagens/`
  esteja faltando (o jogo já roda 100% sem depender disso, mas ajuda a
  garantir que o projeto nunca quebre por falta de um arquivo)
- Listas (para representar o corpo da cobra) e laços `while` (para o game
  loop), conforme pedido no enunciado

Todas as dependências estão listadas em [`requirements.txt`](requirements.txt).

## ▶️ Como rodar

Você **não precisa criar nenhuma pasta manualmente antes** — o comando de
clone (`git clone`) já cria a pasta do projeto sozinho, com tudo dentro
dela (código, imagens, sons). Escolha um dos dois métodos abaixo.

### Opção A — Direto pelo PyCharm (recomendado, mais simples)

1. **Escolha onde o projeto vai ficar.** Não precisa criar a pasta você
   mesmo — só decida o local, por exemplo a Área de Trabalho
   (`C:\Users\SeuUsuario\Desktop`) ou `Documentos`. O Git vai criar a
   pasta `Trabalho-G2-Snake-game` sozinho dentro do local escolhido.
2. Abra o **PyCharm**.
3. Na tela inicial, clique em **Get from VCS** (ou, com um projeto já
   aberto, vá em **File → New → Project from Version Control**).
4. Em **URL**, cole:
   ```
   https://github.com/HenriquePagini/Trabalho-G2-Snake-game
   ```
5. Em **Directory**, escolha a pasta onde quer salvar (ex: a Área de
   Trabalho) — o PyCharm cria a subpasta do projeto automaticamente ali
   dentro. Clique em **Clone**.
6. Quando o PyCharm terminar de abrir o projeto, ele normalmente detecta
   sozinho o arquivo `requirements.txt` e mostra uma barra amarela no
   topo perguntando **"Install requirements"** — clique nela e espere
   instalar (`pygame` e `Pillow`).
   - Se essa barra não aparecer, instale manualmente: abra o terminal
     do próprio PyCharm (aba **Terminal**, embaixo da tela) e rode:
     ```
     pip install -r requirements.txt
     ```
7. Abra o arquivo `jogoCobrinha.py` na árvore de arquivos à esquerda,
   clique com o botão direito nele e escolha **Run 'jogoCobrinha'**
   (ou clique no botão ▶️ verde no canto superior direito).
8. A janela do jogo deve abrir normalmente. Nenhuma outra configuração é
   necessária.

### Opção B — Pelo terminal (Windows, PowerShell/CMD)

1. Escolha uma pasta para trabalhar, por exemplo a Área de Trabalho.
   Abra o terminal (PowerShell ou Prompt de Comando) e navegue até lá:
   ```powershell
   cd Desktop
   ```
2. Clone o repositório (isso já cria a pasta do projeto sozinho, não
   precisa criar nada antes):
   ```powershell
   git clone https://github.com/HenriquePagini/Trabalho-G2-Snake-game
   cd Trabalho-G2-Snake-game
   ```
3. (Opcional, mas recomendado) crie um ambiente virtual, para não
   misturar essas dependências com outras instaladas no sistema:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   Se aparecer erro de permissão ao ativar no PowerShell, rode antes:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
4. Instale as dependências (**obrigatório antes de executar**):
   ```powershell
   pip install -r requirements.txt
   ```
5. Rode o jogo:
   ```powershell
   python jogoCobrinha.py
   ```

### Linux / macOS (terminal)

```bash
cd ~/Desktop        # ou qualquer pasta de sua preferência
git clone https://github.com/HenriquePagini/Trabalho-G2-Snake-game
cd Trabalho-G2-Snake-game
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python jogoCobrinha.py
```

### ❓ Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | Dependências não instaladas | Rode `pip install -r requirements.txt` na mesma pasta do projeto |
| `git` não é reconhecido como comando | Git não instalado | Instale o [Git para Windows](https://git-scm.com/download/win) ou baixe o repositório como ZIP pelo botão verde **Code → Download ZIP** no GitHub |
| `python` não é reconhecido como comando | Python não instalado / não está no PATH | Instale o [Python](https://www.python.org/downloads/) marcando a opção "Add python.exe to PATH" durante a instalação |
| Jogo abre sem som | Ambiente sem placa de som (raro) | Normal — o jogo continua 100% jogável, só sem áudio |

Nenhum ajuste de código, caminho de arquivo ou configuração adicional é
necessário em qualquer um dos métodos acima — só clonar, instalar as
duas dependências e executar.

## 🕹️ Controles

| Tecla            | Ação                  |
|-------------------|-----------------------|
| ↑ / W             | Mover para cima       |
| ↓ / S             | Mover para baixo      |
| ← / A             | Mover para esquerda   |
| → / D             | Mover para direita    |
| P                 | Pausar / continuar    |
| ENTER             | Confirmar / reiniciar |
| ESC               | Sair do jogo / menu   |

## 🍎 Itens do jogo

| Item        | Efeito                                   |
|-------------|-------------------------------------------|
| Doce Raro   | Cresce e soma pontos                       |
| Candy 2x    | Cresce duas vezes de uma vez                |
| Raio        | Acelera a cobra por alguns segundos         |
| Relógio     | Desacelera a cobra por alguns segundos      |
| Estrela     | Pontuação em dobro por um tempo             |
| Corte       | Encolhe o corpo da cobra                    |
| Pokébomba   | Mata a cobra se for comida — **evite!**     |

> A fruta principal (a que aparece sozinha e precisa ser perseguida)
> **nunca** é uma bomba. A Pokébomba só aparece como item secundário,
> de forma opcional, e some sozinha depois de alguns segundos caso não
> seja comida.

## 📁 Estrutura do projeto

```
Trabalho-G2-Snake-game/
├── jogoCobrinha.py      # código principal do jogo
├── imagens/              # sprites usados no jogo
├── sons/                  # efeitos sonoros
├── requirements.txt      # dependências do projeto
├── LICENSE                # licença MIT do repositório
└── README.md              # este arquivo
```

## 📜 Créditos e direitos autorais dos assets

### Imagens (`imagens/`)

Todos os sprites abaixo (`head_right.png`, `body.png`, `tail.png`,
`apple_red.png`, `apple_green.png`, `bomb.png`, `speed.png`, `slow.png`,
`star.png`, `shrink.png`, `dead.png`) foram **desenhados manualmente
pelos próprios autores (Henrique Pagini e Pedro Algayer)** utilizando o
editor de pixel art gratuito e open-source **[Piskel](https://www.piskelapp.com/)**.
Os arquivos `.png` em si são, portanto, de autoria dos alunos.

> ⚠️ **Observação sobre o personagem:** os sprites representam uma
> releitura em pixel art do **Rayquaza**, personagem cujo design é
> propriedade da Game Freak / Nintendo / The Pokémon Company. Embora os
> arquivos tenham sido desenhados à mão pelos autores (e não copiados de
> nenhuma fonte externa), o desenho do personagem em si constitui uma
> obra derivada dessa franquia. Este projeto é de **uso estritamente
> acadêmico e não comercial**, desenvolvido como trabalho da disciplina
> de Algoritmos e Programação, sem qualquer intenção de violar ou se
> apropriar dos direitos da Pokémon Company/Nintendo/Game Freak.

### Sons (`sons/`)

| Arquivo | Origem / autor | Licença |
|---|---|---|
| `beep.mp3` | [Epidemic Sound](https://www.epidemicsound.com/) | Licença de assinatura Epidemic Sound |
| `morreu.mp3` | [Epidemic Sound](https://www.epidemicsound.com/) | Licença de assinatura Epidemic Sound |
| `notificacao.mp3` | [Epidemic Sound](https://www.epidemicsound.com/) | Licença de assinatura Epidemic Sound |

> ⚠️ **Observação sobre a licença:** os efeitos sonoros foram baixados da
> plataforma Epidemic Sound. É importante ressaltar que a licença da
> Epidemic Sound é pensada principalmente para uso em **conteúdo
> audiovisual finalizado** (vídeos, podcasts, streams) por assinantes
> ativos, e não necessariamente para **redistribuição do arquivo de áudio
> em si** dentro de um repositório de código público, que qualquer pessoa
> pode baixar separadamente do restante do jogo. Este uso aqui é de
> caráter estritamente acadêmico e não comercial. Caso haja qualquer
> dúvida sobre essa licença cobrir este cenário específico, a alternativa
> mais segura é substituir esses três arquivos por sons de licença livre
> (ex: [freesound.org](https://freesound.org), filtrando por CC0) antes
> da entrega final.

## 📄 Licença

Este repositório está licenciado sob a licença **MIT** — veja o arquivo
[LICENSE](LICENSE) para mais detalhes. A licença MIT cobre o **código-fonte**
escrito pelos autores; ela não concede automaticamente direitos sobre
assets de terceiros eventualmente utilizados — daí a importância da
seção de créditos acima.

## 🐛 Correções aplicadas nesta versão

Durante a revisão deste trabalho, foi identificado e corrigido um bug
crítico de funcionalidade:

- **Bug:** quando o item especial sorteado era a bomba e ela ficava
  sozinha na tela, o jogo travava — o jogador era obrigado a comer a
  bomba (e morrer) para a partida prosseguir, pois não existia outra
  fruta disponível nem forma da bomba desaparecer sozinha.
- **Correção:** a bomba agora só pode aparecer como **item secundário
  opcional** (nunca como a fruta principal, que é sempre obrigatória) e
  todo item secundário — incluindo a bomba — **expira sozinho** após
  alguns segundos na tela, com uma barrinha visual indicando o tempo
  restante. Assim, o jogador nunca é forçado a interagir com a bomba.

Outras melhorias de robustez:
- Inicialização do áudio (`pygame.mixer`) protegida contra falhas em
  ambientes sem dispositivo de som disponível.
- Geração de pastas de assets protegida contra erros de permissão.
- A fruta principal nunca é mais gerada em cima do item especial atual
  (e vice-versa), evitando sobreposição de sprites.

## 📋 Sobre o trabalho

Projeto desenvolvido para a disciplina de Ciência da Computação,
atendendo aos requisitos do enunciado **Python Crash**:
movimentação por teclado, corpo da cobra representado por lista,
geração aleatória de comida, contagem de pontos, detecção de colisão
com bordas e com o próprio corpo, e encerramento de partida (game over).

**Prazo de entrega:** 03/07/2026
