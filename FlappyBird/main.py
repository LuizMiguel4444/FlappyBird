import pygame
import os
import random
import datetime

pygame.init()
pygame.font.init()

TELA_LARGURA = 500
TELA_ALTURA = 700

pygame.display.set_caption("FlappyBird")
icone = pygame.image.load("./FlappyBird/imgs/bird1.png")
icone_caption = pygame.image.load("./FlappyBird/imgs/bird4.png")
pygame.display.set_icon(icone_caption)
hora = datetime.datetime.now()

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "base.png")))
if hora.hour <= 17 and hora.hour >= 6:
    IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "bg.png")))
else:
    IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "bgnight.png")))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs", "bird3.png"))),
]


fonte_botao = pygame.font.Font("./FlappyBird/imgs/font.ttf", 20)
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
cor_texto = (255, 255, 255)



class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do pássaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do pássaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o pássaro tiver caindo, eu não vou bater a asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)



class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicao_topo = 0
        self.posicao_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_topo = self.altura - self.CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.posicao_topo))
        tela.blit(self.CANO_BASE, (self.x, self.posicao_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x,self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x,self.posicao_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False



class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))



class Botao():
    def __init__(self, imagem, pos, texto, fonte, cor1, cor2):
        self.imagem = imagem
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.fonte = fonte
        self.cor1, self.cor2 = cor1, cor2
        self.texto = texto
        self.texto1 = fonte_botao.render(self.texto, True, self.cor1)
        if self.imagem is None:
            self.imagem = self.texto1
        self.rect = self.imagem.get_rect(center=(self.x_pos, self.y_pos))
        self.texto1_rect = self.texto1.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, tela):
        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
        tela.blit(self.texto1, self.texto1_rect)

    def checar_entrada(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def cor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.texto1 = fonte_botao.render(self.texto, True, self.cor2)
        else:
            self.texto1 = fonte_botao.render(self.texto, True, self.cor1)



def tela_inicial(texto, FONTE_PONTOS, cor_texto, x, y ):
    imagem = FONTE_PONTOS.render(texto, True, cor_texto)
    tela.blit(imagem, (x, y))    

def desenhar_tela(tela, passaros, canos, chao, pontos):
    game_texto = fonte(12).render("Press R to Restart // Press M to Menu", True, "Black")
    game_rect = game_texto.get_rect(center=(250, 678))
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto_pontos = fontePoints(50).render(f"{pontos}", 1, (255, 255, 255))
    tela.blit(texto_pontos, (250, 80))
    chao.desenhar(tela)
    tela.blit(game_texto, game_rect)
    pygame.display.update()

def fonte(tamanho):
    return pygame.font.Font("./FlappyBird/imgs/font.ttf", tamanho)

def fontePoints(tamanho):
    return pygame.font.Font("./FlappyBird/imgs/fonte.ttf", tamanho)

def credits():

    iniciar = True
    while iniciar:

        if hora.hour <= 17 and hora.hour >= 6:
            bg = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs/bg.png")))
        else:
            bg = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs/bgnight.png")))
        if hora.hour <= 17 and hora.hour >= 6:
            credits_texto = fonte(12).render("Jogo baseado no famoso FlappyBird.", True, "Black")
            credits_texto1 = fonte(12).render("Reconstruído e criado por Luiz Miguel.", True, "Black")
            credits_rect = credits_texto.get_rect(center=(250, 150))
            credits_rect1 = credits_texto.get_rect(center=(230, 175))
        else:
            credits_texto = fonte(12).render("Jogo baseado no famoso FlappyBird.", True, "#b68f40")
            credits_texto1 = fonte(12).render("Reconstruído e criado por Luiz Miguel.", True, "#b68f40")
            credits_rect = credits_texto.get_rect(center=(250, 150))
            credits_rect1 = credits_texto.get_rect(center=(230, 175))
        tela.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()    
        
        botao_back = Botao(imagem=pygame.image.load("./FlappyBird/imgs/botão.png"), pos=(250, 380),
                            texto="BACK", fonte=fonte, cor1="#d7fcd4", cor2="#0F0F0F")
        
        tela.blit(credits_texto, credits_rect)
        tela.blit(credits_texto1, credits_rect1)
        tela.blit(icone, (230, 250))

        for botao in [botao_back]:
            botao.cor(mouse_pos)
            botao.update(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_back.checar_entrada(mouse_pos):
                    menu()

        pygame.display.update()

def menu():

    iniciar = True
    while iniciar:
        
        if hora.hour <= 17 and hora.hour >= 6:
            bg = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs/bg.png")))
        else:
            bg = pygame.transform.scale2x(pygame.image.load(os.path.join("./FlappyBird/imgs/bgnight.png")))
        tela.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        menu_texto = fonte(38).render("FlappyBird", True, "#b68f40")
        menu_texto1 = fonte(16).render("Menu Principal", True, "#b68f40")
        menu_texto2 = fonte(12).render("Criado por Luiz Miguel", True, "Black")
        menu_rect = menu_texto.get_rect(center=(250, 100))
        menu_rect1 = menu_texto1.get_rect(center=(250, 150))
        menu_rect2 = menu_texto2.get_rect(center=(250, 630))
        

        botao_iniciar = Botao(imagem=pygame.image.load("./FlappyBird/imgs/botão.png"), pos=(250, 300),
                            texto="PLAY", fonte=fonte, cor1="#d7fcd4", cor2="#0F0F0F")
        botao_cred = Botao(imagem=pygame.image.load("./FlappyBird/imgs/botão.png"), pos=(250, 380),
                            texto="CREDITS", fonte=fonte, cor1="#d7fcd4", cor2="#0F0F0F")
        botao_sair = Botao(imagem=pygame.image.load("./FlappyBird/imgs/botão.png"), pos=(250, 460),
                            texto="EXIT", fonte=fonte, cor1="#d7fcd4", cor2="#0F0F0F")

        tela.blit(menu_texto, menu_rect)
        tela.blit(menu_texto1, menu_rect1)
        tela.blit(icone, (230, 200))
        tela.blit(icone, (230, 545))
        tela.blit(menu_texto2, menu_rect2)

        for botao in [botao_iniciar, botao_cred, botao_sair]:
            botao.cor(mouse_pos)
            botao.update(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.checar_entrada(mouse_pos):
                    run()
                if botao_cred.checar_entrada(mouse_pos):
                    credits()
                if botao_sair.checar_entrada(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

def run():
    passaros = [Passaro(230, 220)]
    chao = Chao(620)
    canos = [Cano(600)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        click = pygame.mouse.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                exit()
            
            # interação com espaço e setinha pra cima    
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    for passaro in passaros:
                        passaro.pular()            
            # interação com clique esquerdo do mouse            
            if click[0]:
                for passaro in passaros:
                    passaro.pular()

            # interação para resetar o jogo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    menu()    
                if evento.key == pygame.K_r:
                    run()

        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(500))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)
        pygame.display.update()

if __name__ == "__main__":
    menu()