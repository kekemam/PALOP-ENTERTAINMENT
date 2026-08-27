#!/usr/bin/env python3
"""
Prepara uma fotografia para o site: corta, redimensiona e grava em WebP
com o nome certo. Não é preciso saber que tamanho leva cada sítio.

    python3 ferramentas/foto.py <ficheiro> <sítio> [--foco cima|centro|baixo]

Exemplos
    python3 ferramentas/foto.py ~/Desktop/IMG_9021.jpg ceo --foco cima
    python3 ferramentas/foto.py ~/Desktop/festival.png festival
    python3 ferramentas/foto.py --lista

Aceita JPEG, PNG, HEIC (do iPhone), WebP — o que a máquina fotográfica der.
"""
import sys, os
from PIL import Image, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sítio → (ficheiro, largura, altura, descrição)
SITIOS = {
 'hero':     ('rosto.webp',         760, 1220, 'painel do ecrã de abertura (vertical)'),
 'sobre':    ('direcao.webp',      1000, 1250, '«Quem Somos» (vertical, 4:5)'),
 'ceo':      ('carlos-uissa.webp',  760, 1013, 'retrato do CEO (vertical, 3:4)'),
 'verdades': ('verdades.webp',     1200,  862, 'cartão Irmãos Verdades (horizontal)'),
 'cartaz':   ('cartaz-te-amo.webp', 620, 1400, 'cartaz do destaque musical (muito vertical)'),
 'festival': ('multidao.webp',      700, 1050, 'cartão PALOP Festival (vertical)'),
 'miss':     ('miss-palop.webp',    900,  990, 'cartão Miss PALOP (quase quadrado)'),
 'tv':       ('palop-tv.webp',      880, 1270, 'cartão PALOP TV (vertical)'),
 'agencia':  ('agencia.webp',      1000,  990, 'cartão Agência de Artistas (quadrado)'),
 'turismo':  ('turismo.webp',      1400,  678, 'cartão Turismo (panorâmico)'),
 'jobs':     ('jobs.webp',         1100, 1394, 'cartão PALOP Jobs (vertical)'),
 'equipa':   ('equipa.webp',       1600, 1067, 'fundo da secção final (horizontal)'),
 'og':       ('og.jpg',            1200,  630, 'imagem de partilha em redes sociais'),
}

def lista():
    print('\nSítios disponíveis:\n')
    for k,(f,w,h,d) in SITIOS.items():
        print(f'  {k:10} {w}x{h:<6} {d}')
    print('\nUso: python3 ferramentas/foto.py <ficheiro> <sítio> [--foco cima|centro|baixo]\n')

def main():
    a = sys.argv[1:]
    if not a or '--lista' in a or '-l' in a: lista(); return
    if len(a) < 2: print('Faltam argumentos.\n'); lista(); sys.exit(1)

    origem, sitio = a[0], a[1].lower()
    foco = 'centro'
    if '--foco' in a: foco = a[a.index('--foco')+1].lower()

    if sitio not in SITIOS:
        print(f'Sítio desconhecido: «{sitio}»\n'); lista(); sys.exit(1)
    if not os.path.isfile(origem):
        print(f'Não encontrei o ficheiro: {origem}'); sys.exit(1)

    nome, LARG, ALT, desc = SITIOS[sitio]
    destino = os.path.join(RAIZ, 'img', nome)

    try:
        im = Image.open(origem)
    except Exception as e:
        print(f'Não consegui abrir a imagem: {e}')
        print('Se for um HEIC do iPhone, exporte primeiro como JPEG.'); sys.exit(1)
    im = im.convert('RGB')

    # corta ao formato do sítio, sem deformar
    alvo, actual = LARG/ALT, im.width/im.height
    if actual > alvo:                       # larga de mais → corta dos lados
        nova = int(im.height*alvo)
        x = (im.width-nova)//2
        im = im.crop((x, 0, x+nova, im.height))
    elif actual < alvo:                     # alta de mais → corta em cima/baixo
        nova = int(im.width/alvo)
        y = {'cima':0, 'baixo':im.height-nova}.get(foco, (im.height-nova)//2)
        im = im.crop((0, y, im.width, y+nova))

    ampliada = im.width < LARG
    im = im.resize((LARG, ALT), Image.LANCZOS)
    if ampliada:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=80, threshold=3))

    if nome.endswith('.jpg'):
        im.save(destino, 'JPEG', quality=82, optimize=True, progressive=True)
    else:
        im.save(destino, 'WEBP', quality=80, method=6)

    kb = os.path.getsize(destino)//1024
    print(f'\n  ✓ {desc}')
    print(f'    gravado em  img/{nome}  ({LARG}x{ALT}, {kb} KB)')
    if ampliada:
        print(f'    ⚠ o original era mais pequeno que {LARG}px de largura — a foto vai sair menos nítida')
    print('\n  Falta publicar:')
    print('    git add img && git commit -m "Nova foto: '+sitio+'" && git push\n')

if __name__ == '__main__':
    main()
