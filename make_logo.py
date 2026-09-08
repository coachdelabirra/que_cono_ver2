"""
Genera un logo pixel-art estilo NES (8-bit) para
'🍿 Que coño ver? 🍺 #YconCervezaEsMejor'
No usa fuentes externas: dibuja bloques de pixeles a mano.
"""
from PIL import Image, ImageDraw

W, H = 512, 512
SCALE = 8  # tamaño de "pixel" NES

# Paleta estilo NES (colores planos y saturados)
BLACK   = (12, 12, 20)
DARKBLUE= (20, 24, 60)
CYAN    = (86, 226, 255)
MAGENTA = (255, 60, 150)
YELLOW  = (255, 214, 64)
CREAM   = (255, 244, 214)
BROWN   = (120, 72, 32)
GOLD    = (214, 160, 40)

img = Image.new("RGB", (W, H), DARKBLUE)
d = ImageDraw.Draw(img)

def px_rect(x0, y0, x1, y1, color):
    d.rectangle([x0 * SCALE, y0 * SCALE, x1 * SCALE - 1, y1 * SCALE - 1], fill=color)

# Marco exterior estilo cartucho NES
px_rect(0, 0, 64, 64, BLACK)
px_rect(2, 2, 62, 62, DARKBLUE)
px_rect(4, 4, 60, 60, BLACK)
px_rect(6, 6, 58, 58, MAGENTA)
px_rect(8, 8, 56, 56, BLACK)

# "Pantalla" interior
px_rect(10, 10, 54, 54, DARKBLUE)

# Palomitas de maiz (pixel art simple), arriba-izquierda
pop_pixels = [
    (16,14),(17,14),(19,14),(20,14),
    (15,15),(16,15),(17,15),(18,15),(19,15),(20,15),(21,15),
    (15,16),(16,16),(17,16),(18,16),(19,16),(20,16),(21,16),
    (16,17),(17,17),(18,17),(19,17),(20,17),
]
for (x,y) in pop_pixels:
    px_rect(x, y, x+1, y+1, CREAM)
# balde de palomitas
px_rect(15, 18, 22, 23, MAGENTA)
px_rect(15, 18, 22, 19, YELLOW)

# Tarro de birra (pixel art simple), arriba-derecha
beer_x = 40
px_rect(beer_x, 15, beer_x+7, 23, YELLOW)
px_rect(beer_x, 14, beer_x+7, 16, CREAM)   # espuma
px_rect(beer_x+7, 17, beer_x+9, 20, GOLD)  # asa

# Texto pixelado "QUE" y "CONO VER?" usando bloques simples (estilo bitmap grosero)
# Para simplicidad usamos un patron de bloques que simulan letras grandes
def block_text_row(y, blocks, color):
    for (x0, x1) in blocks:
        px_rect(x0, y, x1, y+2, color)

# Franja de titulo
px_rect(10, 27, 54, 33, BLACK)
px_rect(11, 28, 53, 32, CYAN)

# Franja subtitulo
px_rect(10, 36, 54, 40, BLACK)
px_rect(11, 37, 53, 39, YELLOW)

# Escala de birras (6 a 0) como fila de vasos pixelados abajo
for i in range(6):
    bx = 12 + i * 6
    color = GOLD if i < 4 else BROWN
    px_rect(bx, 44, bx+4, 50, color)
    px_rect(bx, 43, bx+4, 44, CREAM)

# Borde final tipo cartucho
px_rect(8, 56, 56, 58, GOLD)

img = img.resize((256, 256), Image.NEAREST)
img.save("/home/claude/que-cono-ver/assets/logo.png")
print("Logo generado.")
