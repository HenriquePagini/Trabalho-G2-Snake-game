##########################################################
####     R A Y Q U A Z A   S N A K E                  ####
####     Baseado em ProfessorFilipo/Trabalho02         ####
##########################################################
import pygame
import sys
import random
import os

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    # Ambiente sem dispositivo de áudio disponível (ex.: alguns servidores
    # ou CI). O jogo deve continuar funcionando normalmente, só sem som.
    pass
pygame.font.init()

# ─────────────────────────────────────────────
#  Janela
# ─────────────────────────────────────────────
LARGURA_TELA  = 600
ALTURA_TELA   = 640
TAMANHO_GRADE = 32          # maior para o Rayquaza ficar bem visível
COLUNAS       = LARGURA_TELA  // TAMANHO_GRADE   # 18
LINHAS        = (ALTURA_TELA - 48) // TAMANHO_GRADE  # 18

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Rayquaza Snake  –  Trabalho02")
relogio = pygame.time.Clock()

# ─────────────────────────────────────────────
#  Cores – tema Pokémon / Rayquaza
# ─────────────────────────────────────────────
COR_FUNDO       = (10, 18, 30)        # céu noturno profundo
COR_GRADE       = (18, 30, 48)
COR_PAINEL      = (8, 14, 24)
BRANCO          = (240, 248, 255)
AMARELO_RAY     = (255, 220, 40)      # amarelo do Rayquaza
VERDE_RAY       = (60, 180, 60)       # verde do Rayquaza
VERMELHO_RAY    = (200, 40, 40)       # detalhes vermelhos
LARANJA         = (255, 140, 0)
ROXO            = (160, 80, 220)
CIANO           = (0, 200, 220)
AZUL_CLARO      = (80, 160, 255)
ROSA            = (255, 100, 180)

# ─────────────────────────────────────────────
#  Fontes estilo pixel/retro
# ─────────────────────────────────────────────
fonte_grande  = pygame.font.SysFont("Courier New", 56, bold=True)
fonte_media   = pygame.font.SysFont("Courier New", 32, bold=True)
fonte_pequena = pygame.font.SysFont("Courier New", 18)
fonte_ui      = pygame.font.SysFont("Courier New", 18, bold=True)
fonte_toast   = pygame.font.SysFont("Courier New", 24, bold=True)

# ─────────────────────────────────────────────
#  Direções
# ─────────────────────────────────────────────
CIMA     = ( 0, -1)
BAIXO    = ( 0,  1)
ESQUERDA = (-1,  0)
DIREITA  = ( 1,  0)

FPS_BASE = 6

# ─────────────────────────────────────────────
#  Pastas de assets
# ─────────────────────────────────────────────
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMG  = os.path.join(PASTA_BASE, "imagens")
PASTA_SOM  = os.path.join(PASTA_BASE, "sons")
try:
    os.makedirs(PASTA_IMG, exist_ok=True)
    os.makedirs(PASTA_SOM, exist_ok=True)
except OSError:
    # Se não houver permissão de escrita (ex: jogo instalado em pasta
    # somente leitura), seguimos em frente — as pastas já vêm prontas
    # no repositório, então não são estritamente necessárias aqui.
    pass

# ─────────────────────────────────────────────
#  Geração de imagens fallback via Pillow
# ─────────────────────────────────────────────
def _gerar_fallbacks():
    try:
        from PIL import Image, ImageDraw
        import math
    except ImportError:
        return
    T = TAMANHO_GRADE

    def _salva(nome, fn):
        p = os.path.join(PASTA_IMG, nome)
        if not os.path.exists(p):
            img = Image.new("RGBA", (T, T), (0, 0, 0, 0))
            fn(ImageDraw.Draw(img))
            img.save(p)

    # Cabeça Rayquaza fallback
    def _cabeca(d):
        d.rounded_rectangle([1,1,T-1,T-1], radius=6, fill=(60,180,60,255))
        d.ellipse([T-10,4,T-2,12], fill=(255,220,40,255))
        d.ellipse([T-9,5,T-3,11], fill=(20,20,20,255))
        d.rectangle([T-6,T//2,T-1,T-2], fill=(200,40,40,255))
    _salva("head_right.png", _cabeca)

    # Corpo Rayquaza fallback
    def _corpo(d):
        d.rounded_rectangle([1,1,T-1,T-1], radius=4, fill=(60,180,60,255))
        d.rectangle([2,T//2-2,T-2,T//2+2], fill=(255,220,40,255))
        d.rectangle([2,4,T-2,8], fill=(200,40,40,180))
        d.rectangle([2,T-8,T-2,T-4], fill=(200,40,40,180))
    _salva("body.png", _corpo)

    # Cauda Rayquaza fallback
    def _cauda(d):
        d.polygon([(2,T//2),(T-2,2),(T-2,T-2)], fill=(60,180,60,255))
        d.rectangle([T//2,T//2-2,T-2,T//2+2], fill=(255,220,40,255))
    _salva("tail.png", _cauda)

    # Doce raro (placeholder – estrela dourada com brilho)
    def _doce(d):
        d.ellipse([1,1,T-1,T-1], fill=(255,200,0,255))
        d.ellipse([4,4,T-4,T-4], fill=(255,230,80,255))
        # estrela
        cx, cy = T//2, T//2
        import math
        pts = []
        for i in range(5):
            a_out = math.radians(-90 + i*72)
            a_in  = math.radians(-90 + i*72 + 36)
            pts += [(cx + (T//2-3)*math.cos(a_out), cy + (T//2-3)*math.sin(a_out)),
                    (cx + (T//4)*math.cos(a_in),    cy + (T//4)*math.sin(a_in))]
        d.polygon(pts, fill=(255,140,0,255))
    _salva("apple_red.png", _doce)

    # Maçã verde (cresce 2x) – Candy raro verde
    def _doce_verde(d):
        d.ellipse([1,1,T-1,T-1], fill=(40,200,80,255))
        d.ellipse([4,4,T-4,T-4], fill=(80,240,120,255))
        d.text((T//2-4, T//2-6), "2x", fill=(255,255,255,255))
    _salva("apple_green.png", _doce_verde)

    # Bomba
    def _bomba(d):
        d.ellipse([3,5,T-3,T-1], fill=(30,30,30,255))
        d.ellipse([5,7,T-5,T-3], fill=(60,60,60,255))
        d.line([(T//2,1),(T//2,5)], fill=(200,150,20,255), width=3)
        d.ellipse([T//2-2,0,T//2+2,4], fill=(255,200,0,255))
    _salva("bomb.png", _bomba)

    # Raio (acelera)
    def _raio(d):
        d.ellipse([1,1,T-1,T-1], fill=(160,80,220,255))
        pts = [(T//2+3,2),(T//2-3,T//2),(T//2+3,T//2),(T//2-3,T-2),
               (T//2+5,T//2+3),(T//2,T//2+3)]
        d.polygon(pts, fill=(255,230,0,255))
    _salva("speed.png", _raio)

    # Relógio (desacelera)
    def _relogio(d):
        d.ellipse([2,2,T-2,T-2], fill=(80,160,255,255))
        d.ellipse([5,5,T-5,T-5], fill=(30,80,200,255))
        d.line([(T//2,T//2),(T//2,6)], fill=(255,255,255,255), width=2)
        d.line([(T//2,T//2),(T-7,T//2)], fill=(255,255,255,255), width=2)
    _salva("slow.png", _relogio)

    # Estrela (pontos 2x)
    def _estrela(d):
        d.ellipse([1,1,T-1,T-1], fill=(0,200,220,255))
        cx, cy = T//2, T//2
        pts = []
        for i in range(5):
            a_out = math.radians(-90 + i*72)
            a_in  = math.radians(-90 + i*72 + 36)
            pts += [(cx+(T//2-3)*math.cos(a_out), cy+(T//2-3)*math.sin(a_out)),
                    (cx+(T//4)*math.cos(a_in),    cy+(T//4)*math.sin(a_in))]
        d.polygon(pts, fill=(255,220,50,255))
    _salva("star.png", _estrela)

    # Encolhe
    def _encolhe(d):
        d.ellipse([1,1,T-1,T-1], fill=(255,100,180,255))
        d.ellipse([5,5,T-5,T-5], fill=(255,160,200,255))
        d.line([(8,T//2),(T-8,T//2)], fill=(200,0,80,255), width=3)
    _salva("shrink.png", _encolhe)

    # Cobra morta
    def _morta(d):
        d.rounded_rectangle([1,1,T-1,T-1], radius=6, fill=(80,80,80,255))
        for sx, sy in [(5,5),(10,10),(10,5),(5,10),(T-10,5),(T-5,10),(T-5,5),(T-10,10)]:
            d.line([(sx,sy),(sx+5,sy+5)], fill=(220,50,50,255), width=2)
    _salva("dead.png", _morta)

_gerar_fallbacks()

# ─────────────────────────────────────────────
#  Helpers de carregamento
# ─────────────────────────────────────────────
def _surf_fb(cor, raio=4):
    s = pygame.Surface((TAMANHO_GRADE, TAMANHO_GRADE), pygame.SRCALPHA)
    pygame.draw.rect(s, cor, (1,1,TAMANHO_GRADE-2,TAMANHO_GRADE-2), border_radius=raio)
    return s

def _load(nome, cor_fb=(100,100,100), raio=4):
    p = os.path.join(PASTA_IMG, nome)
    if os.path.exists(p):
        try:
            img = pygame.image.load(p).convert_alpha()
            return pygame.transform.smoothscale(img, (TAMANHO_GRADE, TAMANHO_GRADE))
        except Exception:
            pass
    return _surf_fb(cor_fb, raio)

def _load_som(nome):
    p = os.path.join(PASTA_SOM, nome)
    if os.path.exists(p):
        try:
            return pygame.mixer.Sound(p)
        except Exception:
            pass
    return None

# ─────────────────────────────────────────────
#  Sprites do Rayquaza
# ─────────────────────────────────────────────
spr_cabeca = _load("head_right.png", VERDE_RAY)
spr_corpo  = _load("body.png",       VERDE_RAY)
spr_cauda  = _load("tail.png",       VERDE_RAY)
spr_morta  = _load("dead.png",       (80,80,80))

# Pré-rotações (head_right = olhando DIREITA)
def _rots(spr):
    return {
        DIREITA : spr,
        CIMA    : pygame.transform.rotate(spr,  90),
        ESQUERDA: pygame.transform.rotate(spr, 180),
        BAIXO   : pygame.transform.rotate(spr, -90),
    }

rot_cabeca = _rots(spr_cabeca)
rot_morta  = _rots(spr_morta)
rot_cauda  = _rots(spr_cauda)
corpo_h    = spr_corpo
corpo_v    = pygame.transform.rotate(spr_corpo, 90)

# ─────────────────────────────────────────────
#  Sons
# ─────────────────────────────────────────────
som_come     = _load_som("beep.mp3")
som_morte    = _load_som("morreu.mp3")
som_especial = _load_som("notificacao.mp3")

# ─────────────────────────────────────────────
#  Frutas / itens
# ─────────────────────────────────────────────
TIPOS_FRUTA = {
    "normal": {
        "sprite"   : _load("apple_red.png",   AMARELO_RAY, raio=12),
        "cor"      : AMARELO_RAY,
        "pontos"   : 10,
        "label"    : "+10  Doce Raro!",
        "cor_label": AMARELO_RAY,
    },
    "dupla": {
        "sprite"   : _load("apple_green.png", VERDE_RAY,   raio=12),
        "cor"      : VERDE_RAY,
        "pontos"   : 10,
        "label"    : "Cresce 2x! +10",
        "cor_label": VERDE_RAY,
    },
    "acelera": {
        "sprite"   : _load("speed.png",  ROXO, raio=12),
        "cor"      : ROXO,
        "pontos"   : 20,
        "label"    : "VELOCIDADE! +20",
        "cor_label": ROXO,
        "efeito_dur": 5000,
    },
    "desacelera": {
        "sprite"   : _load("slow.png",   AZUL_CLARO, raio=12),
        "cor"      : AZUL_CLARO,
        "pontos"   : 15,
        "label"    : "Mais devagar... +15",
        "cor_label": AZUL_CLARO,
        "efeito_dur": 5000,
    },
    "pontos2x": {
        "sprite"   : _load("star.png",   CIANO, raio=12),
        "cor"      : CIANO,
        "pontos"   : 30,
        "label"    : "PONTOS 2x! +30",
        "cor_label": CIANO,
        "efeito_dur": 8000,
    },
    "encolhe": {
        "sprite"   : _load("shrink.png", ROSA, raio=12),
        "cor"      : ROSA,
        "pontos"   : 25,
        "label"    : "Encolheu! +25",
        "cor_label": ROSA,
        "efeito_dur": 0,
    },
    "bomba": {
        "sprite"   : _load("bomb.png",   (40,40,40), raio=12),
        "cor"      : (200,50,50),
        "pontos"   : -1,
        "label"    : "BOOM!",
        "cor_label": (255,80,80),
    },
}

PESOS = (["normal"]*55 + ["dupla"]*12 + ["acelera"]*8 +
         ["desacelera"]*10 + ["pontos2x"]*8 + ["encolhe"]*7)

# Tipos que podem aparecer como item SECUNDÁRIO (bônus opcional na tela).
# A bomba SÓ pode aparecer aqui — nunca como a fruta principal — pois o
# item secundário é opcional (tem tempo de vida e não bloqueia o jogo).
PESOS_ESPECIAL = ["acelera", "desacelera", "pontos2x", "encolhe", "dupla", "bomba"]

DURACAO_ESPECIAL_MS = 6000  # item secundário some sozinho após 6s se não for comido

def sortear_tipo_principal(nivel):
    """Sorteia o tipo da fruta PRINCIPAL (obrigatória/única na tela).
    Nunca retorna 'bomba', pois essa fruta não tem como ser evitada."""
    return random.choice(PESOS)

# ─────────────────────────────────────────────
#  Efeito ativo
# ─────────────────────────────────────────────
class Efeito:
    def __init__(self):
        self.tipo = None; self.fim_ms = 0
        self.pontos2x = False; self.fps_bonus = 0
    def aplicar(self, tipo, agora):
        self.tipo = tipo
        self.fim_ms = agora + TIPOS_FRUTA[tipo].get("efeito_dur", 0)
        self.pontos2x  = (tipo == "pontos2x")
        self.fps_bonus = 4 if tipo == "acelera" else (-3 if tipo == "desacelera" else 0)
    def atualizar(self, agora):
        if self.tipo and agora > self.fim_ms:
            self.tipo = None; self.pontos2x = False; self.fps_bonus = 0
    def ativo(self): return self.tipo is not None

efeito_ativo = Efeito()

# ─────────────────────────────────────────────
#  Toast
# ─────────────────────────────────────────────
class Toast:
    def __init__(self): self.texto=""; self.cor=BRANCO; self.fim_ms=0; self.y0=300
    def mostrar(self, texto, cor, dur=1400):
        self.texto=texto; self.cor=cor
        self.fim_ms=pygame.time.get_ticks()+dur; self.y0=ALTURA_TELA//2
    def desenhar(self):
        agora=pygame.time.get_ticks()
        if agora>=self.fim_ms: return
        prog=(self.fim_ms-agora)/1400
        y=int(self.y0-( 1-prog)*90)
        s=fonte_toast.render(self.texto,True,self.cor)
        s.set_alpha(int(255*prog))
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2, y))

toast = Toast()

# ─────────────────────────────────────────────
#  Estrelas de fundo (efeito parallax simples)
# ─────────────────────────────────────────────
estrelas = [(random.randint(0,LARGURA_TELA), random.randint(48,ALTURA_TELA),
             random.randint(1,3)) for _ in range(80)]

def desenha_fundo(frame):
    tela.fill(COR_FUNDO)
    for (x, y, brilho) in estrelas:
        alpha = int(120 + 100 * abs(((frame + x*3) % 60) - 30) / 30)
        s = pygame.Surface((brilho, brilho))
        s.fill((alpha, alpha, alpha))
        tela.blit(s, (x, y))

# ─────────────────────────────────────────────
#  Funções de desenho
# ─────────────────────────────────────────────
def desenha_grade():
    for x in range(0, LARGURA_TELA, TAMANHO_GRADE):
        pygame.draw.line(tela, COR_GRADE, (x, 48), (x, ALTURA_TELA))
    for y in range(48, ALTURA_TELA, TAMANHO_GRADE):
        pygame.draw.line(tela, COR_GRADE, (0, y), (LARGURA_TELA, y))

def cel(col, lin):
    return col * TAMANHO_GRADE, 48 + lin * TAMANHO_GRADE

def dir_seg(cobra, i):
    dc = cobra[i-1][0] - cobra[i][0]
    dl = cobra[i-1][1] - cobra[i][1]
    if dc== 1: return DIREITA
    if dc==-1: return ESQUERDA
    if dl== 1: return BAIXO
    return CIMA

def desenha_cobra(cobra, direcao, morta=False):
    n = len(cobra)
    for i,(col,lin) in enumerate(cobra):
        x,y = cel(col,lin)
        if i==0:
            tela.blit(rot_morta[direcao] if morta else rot_cabeca[direcao], (x,y))
        elif i==n-1 and n>1:
            tela.blit(rot_cauda[dir_seg(cobra,i)], (x,y))
        else:
            d = dir_seg(cobra,i)
            tela.blit(corpo_v if d in (CIMA,BAIXO) else corpo_h, (x,y))

def desenha_fruta(col, lin, tipo, frame):
    x,y = cel(col,lin)
    pulso  = abs(frame%50-25)/25
    escala = int(TAMANHO_GRADE + pulso*5)
    offset = (TAMANHO_GRADE - escala)//2
    spr    = pygame.transform.scale(TIPOS_FRUTA[tipo]["sprite"], (escala,escala))
    tela.blit(spr, (x+offset, y+offset))
    # brilho ao redor das frutas especiais
    if tipo not in ("normal","bomba"):
        cor = TIPOS_FRUTA[tipo]["cor"]
        pygame.draw.rect(tela, (*cor, 60),
                         (x+1, y+1, TAMANHO_GRADE-2, TAMANHO_GRADE-2),
                         width=2, border_radius=6)

def desenha_tempo_especial(especial, fim_ms, agora):
    """Mostra uma barrinha de tempo restante acima do item secundário,
    deixando claro (sobretudo na bomba) que ele é opcional e vai sumir."""
    if especial is None:
        return
    col, lin, tipo = especial
    x, y = cel(col, lin)
    restante = max(0, fim_ms - agora)
    prog = restante / DURACAO_ESPECIAL_MS
    largura = int((TAMANHO_GRADE - 4) * prog)
    cor = (220, 60, 60) if tipo == "bomba" else TIPOS_FRUTA[tipo]["cor"]
    pygame.draw.rect(tela, COR_PAINEL, (x+2, y-6, TAMANHO_GRADE-4, 4))
    pygame.draw.rect(tela, cor, (x+2, y-6, largura, 4))

def desenha_painel(pts, rec, nivel, ef):
    pygame.draw.rect(tela, COR_PAINEL, (0,0,LARGURA_TELA,48))
    pygame.draw.line(tela, AMARELO_RAY, (0,48), (LARGURA_TELA,48), 2)

    tela.blit(fonte_ui.render(f"PTS:{pts}",  True, AMARELO_RAY),  (6, 8))
    tela.blit(fonte_ui.render(f"REC:{rec}",  True, LARANJA),      (6,28))
    tela.blit(fonte_ui.render(f"NV:{nivel}", True, VERDE_RAY),    (200,18))

    if ef.ativo():
        agora=pygame.time.get_ticks()
        rest=max(0,(ef.fim_ms-agora)//1000)
        nome={"acelera":f"RAPIDO {rest}s","desacelera":f"LENTO {rest}s",
              "pontos2x":f"2x PONTOS {rest}s"}.get(ef.tipo,"")
        if nome:
            tela.blit(fonte_ui.render(nome, True, TIPOS_FRUTA[ef.tipo]["cor"]), (300,18))

    # Titulo no painel
    titulo = fonte_ui.render("RAYQUAZA SNAKE", True, VERDE_RAY)
    tela.blit(titulo, (LARGURA_TELA - titulo.get_width() - 8, 18))

# ═════════════════════════════════════════════
#  TELA INICIAL
# ═════════════════════════════════════════════
def tela_inicial(recorde):
    frame=0
    while True:
        desenha_fundo(frame)
        desenha_grade()

        # Título com sombra
        for dx,dy,cor in [(3,3,VERDE_RAY),(0,0,AMARELO_RAY)]:
            s=fonte_grande.render("RAYQUAZA", cor==AMARELO_RAY, cor)
            tela.blit(s,(LARGURA_TELA//2-s.get_width()//2+dx, 60+dy))
        s=fonte_media.render("SNAKE", True, BRANCO)
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2, 120))

        # Cobra decorativa
        cobra_demo=[(13-i,8) for i in range(6)]
        desenha_cobra(cobra_demo, DIREITA)
        desenha_fruta(14,8,"normal",frame)

        # Legenda das frutas
        itens=[
            ("apple_red.png",  AMARELO_RAY, "Doce Raro  – come e cresce"),
            ("apple_green.png",VERDE_RAY,   "Candy 2x   – cresce 2 vezes"),
            ("speed.png",      ROXO,        "Raio       – acelera (5s)"),
            ("slow.png",       AZUL_CLARO,  "Relogio    – desacelera (5s)"),
            ("star.png",       CIANO,       "Estrela    – pontos 2x (8s)"),
            ("shrink.png",     ROSA,        "Corte      – encolhe -3"),
            ("bomb.png",       (220,60,60), "Pokebomba  – EVITE! (some sozinha)"),
        ]
        y0=230
        for arq,cor,desc in itens:
            spr=pygame.transform.scale(_load(arq,cor),( 22,22))
            tela.blit(spr,(LARGURA_TELA//2-160, y0))
            tela.blit(fonte_pequena.render(desc,True,cor),(LARGURA_TELA//2-132,y0+2))
            y0+=26

        alpha=int(128+127*abs((frame%60)-30)/30)
        s=fonte_media.render("ENTER para jogar",True,(alpha,255,alpha))
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA-80))

        if recorde>0:
            s=fonte_pequena.render(f"Recorde: {recorde} pts",True,LARANJA)
            tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA-44))

        pygame.display.flip()
        relogio.tick(60); frame+=1

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key in(pygame.K_RETURN,pygame.K_KP_ENTER): return

# ═════════════════════════════════════════════
#  TELA GAME OVER
# ═════════════════════════════════════════════
def tela_game_over(pts, rec):
    frame=0
    while True:
        desenha_fundo(frame)
        s=fonte_grande.render("GAME OVER",True,(220,50,50))
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA//2-180))
        if pts>=rec and pts>0:
            s=fonte_media.render("NOVO RECORDE!",True,AMARELO_RAY)
            tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA//2-100))
        s=fonte_media.render(f"Pontuacao: {pts}",True,BRANCO)
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA//2-55))
        s=fonte_pequena.render(f"Recorde: {rec} pts",True,LARANJA)
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA//2-10))
        alpha=int(128+127*abs((frame%60)-30)/30)
        s=fonte_media.render("ENTER = Jogar de novo   ESC = Sair",
                             True,(alpha,alpha,255))
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA-80))
        pygame.display.flip(); relogio.tick(60); frame+=1
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: return False
            if ev.type==pygame.KEYDOWN:
                if ev.key in(pygame.K_RETURN,pygame.K_KP_ENTER): return True
                if ev.key==pygame.K_ESCAPE: return False

# ═════════════════════════════════════════════
#  JOGO PRINCIPAL
# ═════════════════════════════════════════════
def nova_pos(cobra, ocupadas=()):
    while True:
        p=(random.randint(0,COLUNAS-1),random.randint(0,LINHAS-1))
        if p not in cobra and p not in ocupadas: return p

def calcular_nivel(pts): return min(10,1+pts//60)
def calcular_fps(nivel): return max(3,FPS_BASE+(nivel-1)*2+efeito_ativo.fps_bonus)

def gerar_fruta(cobra,nivel,ocupadas=()):
    return (*nova_pos(cobra,ocupadas), sortear_tipo_principal(nivel))

def jogar(recorde):
    global efeito_ativo
    efeito_ativo=Efeito()

    cobra   =[(COLUNAS//2,LINHAS//2)]
    direcao =DIREITA; prox_dir=DIREITA
    pts=0; frame=0; pausado=False; morta=False; timer_morte=0

    nivel=1
    fruta_col,fruta_lin,fruta_tipo=gerar_fruta(cobra,nivel)
    especial=None        # (col,lin,tipo) ou None
    especial_fim=0        # timestamp (ms) em que o item especial expira

    while True:
        agora=pygame.time.get_ticks()
        nivel=calcular_nivel(pts)
        fps=calcular_fps(nivel)
        efeito_ativo.atualizar(agora)

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE: return pts
                if ev.key==pygame.K_p: pausado=not pausado
                if ev.key in(pygame.K_UP,   pygame.K_w) and direcao!=BAIXO:    prox_dir=CIMA
                if ev.key in(pygame.K_DOWN, pygame.K_s) and direcao!=CIMA:     prox_dir=BAIXO
                if ev.key in(pygame.K_LEFT, pygame.K_a) and direcao!=DIREITA:  prox_dir=ESQUERDA
                if ev.key in(pygame.K_RIGHT,pygame.K_d) and direcao!=ESQUERDA: prox_dir=DIREITA

        if pausado:
            s=fonte_media.render("PAUSADO  –  P para continuar",True,AMARELO_RAY)
            tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,ALTURA_TELA//2-20))
            pygame.display.flip(); relogio.tick(30); continue

        # Animação de morte
        if morta:
            desenha_fundo(frame); desenha_grade()
            desenha_fruta(fruta_col,fruta_lin,fruta_tipo,frame)
            if especial: desenha_fruta(*especial,frame)
            desenha_cobra(cobra,direcao,morta=True)
            desenha_painel(pts,max(pts,recorde),nivel,efeito_ativo)
            pygame.display.flip(); relogio.tick(30)
            if agora-timer_morte>900: return pts
            frame+=1; continue

        # Movimenta
        direcao=prox_dir
        cabeca=(cobra[0][0]+direcao[0], cobra[0][1]+direcao[1])

        if not(0<=cabeca[0]<COLUNAS and 0<=cabeca[1]<LINHAS):
            if som_morte: som_morte.play()
            morta=True; timer_morte=agora; continue
        if cabeca in cobra:
            if som_morte: som_morte.play()
            morta=True; timer_morte=agora; continue

        cobra.insert(0,cabeca)
        cresceu=False

        def processar(tipo):
            nonlocal pts,cresceu
            info=TIPOS_FRUTA[tipo]
            if tipo=="bomba":
                if som_morte: som_morte.play()
                return "morte"
            p=info["pontos"]
            if efeito_ativo.pontos2x: p*=2
            pts+=p
            toast.mostrar(info["label"],info["cor_label"])

            if tipo=="normal":
                if som_come: som_come.play()
                cresceu=True
            elif tipo=="dupla":
                if som_come: som_come.play()
                cobra.append(cobra[-1])
                cresceu=True
            elif tipo=="encolhe":
                if som_especial: som_especial.play()
                for _ in range(min(3,len(cobra)-1)): cobra.pop()
            else:
                if som_especial: som_especial.play()
                efeito_ativo.aplicar(tipo,agora)
                cresceu=True
            return "ok"

        resultado=None
        if cabeca==(fruta_col,fruta_lin):
            resultado=processar(fruta_tipo)
            ocupadas = (especial[:2],) if especial else ()
            fruta_col,fruta_lin,fruta_tipo=gerar_fruta(cobra,nivel,ocupadas)
            if especial is None and random.random()<0.30:
                te=random.choice(PESOS_ESPECIAL)
                especial=(*nova_pos(cobra,((fruta_col,fruta_lin),)),te)
                especial_fim=agora+DURACAO_ESPECIAL_MS

        if especial and cabeca==(especial[0],especial[1]):
            resultado=processar(especial[2]); especial=None

        # Item especial (incluindo bombas) some sozinho depois de um tempo,
        # assim ele nunca obriga o jogador a precisar comê-lo.
        if especial and agora>=especial_fim:
            especial=None

        if resultado=="morte": morta=True; timer_morte=agora

        if not cresceu: cobra.pop()

        # Desenha
        desenha_fundo(frame); desenha_grade()
        desenha_fruta(fruta_col,fruta_lin,fruta_tipo,frame)
        if especial:
            desenha_fruta(*especial,frame)
            desenha_tempo_especial(especial, especial_fim, agora)
        desenha_cobra(cobra,direcao)
        desenha_painel(pts,max(pts,recorde),nivel,efeito_ativo)
        toast.desenhar()
        pygame.display.flip()
        relogio.tick(fps); frame+=1

    return pts

# ═════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════
def main():
    recorde=0
    tela_inicial(recorde)
    while True:
        pts=jogar(recorde)
        if pts>recorde: recorde=pts
        if not tela_game_over(pts,recorde): break
    pygame.quit(); sys.exit()

if __name__=="__main__":
    main()
