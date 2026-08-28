"""Genera img/portada.jpg (1200x630, Open Graph) y los iconos de la PWA."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = 'img/portada-hero.jpg'
SERIF  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# ---------- portada 1200x630 ----------
W, H = 1200, 630
im = Image.open(BASE).convert('RGB')
r = max(W/im.width, H/im.height)
im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
im = im.crop(((im.width-W)//2, (im.height-H)//3, (im.width-W)//2+W, (im.height-H)//3+H))

# degradado oscuro de abajo arriba, para que se lea el texto
grad = Image.new('L', (1, H))
for y in range(H):
    t = y / H
    grad.putpixel((0, y), int(20 + 205 * max(0, (t-0.25)/0.75) ** 1.4))
capa = Image.new('RGB', (W, H), (6, 26, 38))
im = Image.composite(capa, im, grad.resize((W, H)))

d = ImageDraw.Draw(im)
d.text((64, 372), 'PARA EDU, SARA Y JULIA · DESDE EL 29 DE AGOSTO',
       font=ImageFont.truetype(SANS_B, 22), fill=(214, 231, 240))
d.text((60, 414), 'Londres, a vuestro aire',
       font=ImageFont.truetype(SERIF, 76), fill='white')
d.text((64, 522), 'Dónde comer, qué hacer con la niña y por dónde pasear',
       font=ImageFont.truetype(SERIF, 33), fill=(226, 236, 240))
im.save('img/portada.jpg', quality=90, optimize=True)
print('img/portada.jpg', im.size)

# ---------- iconos 192 / 512 ----------
for lado in (192, 512):
    base = Image.open(BASE).convert('RGB')
    r = max(lado/base.width, lado/base.height)
    b = base.resize((round(base.width*r), round(base.height*r)), Image.LANCZOS)
    b = b.crop(((b.width-lado)//2, 0, (b.width-lado)//2+lado, lado))
    # banda inferior con el nombre
    d = ImageDraw.Draw(b, 'RGBA')
    alto = int(lado*0.30)
    d.rectangle([0, lado-alto, lado, lado], fill=(23, 69, 110, 232))
    f = ImageFont.truetype(SANS_B, int(lado*0.125))
    txt = 'LONDRES'
    x0, y0, x1, y1 = d.textbbox((0, 0), txt, font=f)
    d.text(((lado-(x1-x0))//2 - x0, lado-alto + (alto-(y1-y0))//2 - y0), txt, font=f, fill='white')
    b.save(f'img/icono-{lado}.png')
    print(f'img/icono-{lado}.png', b.size)
