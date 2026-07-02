# 🐍 Rayquaza Snake

Jogo da cobrinha desenvolvido em **Python 3** com **PyGame** pelos alunos Henrique Pagini e Pedro Algayer, com tema
inspirado em Pokémon, como trabalho da disciplina de **Algoritmos e programação** (Python Crash — Prof. Filipo Novo Mór).

![status](https://img.shields.io/badge/status-funcionando-brightgreen)
![python](https://img.shields.io/badge/python-3.x-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)

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

## ▶️ Como rodar

```bash
# 1. Clone o repositório
git clone <url-do-seu-repositorio>
cd <pasta-do-repositorio>

# 2. (Recomendado) crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o jogo
python jogoCobrinha.py
```

Também funciona normalmente abrindo o projeto direto no **PyCharm** e
executando `jogoCobrinha.py`.

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
snake_game2/
├── jogoCobrinha.py      # código principal do jogo
├── imagens/              # sprites usados no jogo
├── sons/                  # efeitos sonoros
├── requirements.txt      # dependências do projeto
└── README.md              # este arquivo
```

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
