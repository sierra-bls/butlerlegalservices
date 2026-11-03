import sys, glob
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]
BURG=(122,31,61); GOLD=(184,146,58); BG=(250,246,240); DARK=(90,21,48)

def font(size, bold=True):
    for p in glob.glob('/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'):
        f = ImageFont.truetype(p, size)
        try: f.set_variation_by_name('Bold' if bold else 'Regular')
        except Exception: pass
        return f
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', size)

def sans(size):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)

def monogram(size):
    im = Image.new('RGBA',(size,size),(0,0,0,0))
    d = ImageDraw.Draw(im)
    d.ellipse((0,0,size-1,size-1), fill=BURG)
    m = int(size*0.045)
    d.ellipse((m*2,m*2,size-1-m*2,size-1-m*2), outline=GOLD, width=max(2,m))
    f = font(int(size*0.56))
    bb = d.textbbox((0,0),'B',font=f)
    d.text(((size-(bb[2]-bb[0]))/2-bb[0], (size-(bb[3]-bb[1]))/2-bb[1]-size*0.01),'B',font=f,fill=(255,255,255))
    return im

# favicons
mono = monogram(1024)
for n in (16,32,48,180,192,512):
    name = {180:'apple-touch-icon.png',192:'android-chrome-192x192.png',512:'android-chrome-512x512.png'}.get(n, f'favicon-{n}x{n}.png' if n<48 else 'favicon-48x48.png')
    im = mono.resize((n,n), Image.LANCZOS)
    if n==180:  # opaque for apple
        bg = Image.new('RGB',(n,n),BG); bg.paste(im,(0,0),im); im=bg
    im.save(f'{out}/{name}')
mono.resize((48,48),Image.LANCZOS).save(f'{out}/favicon.ico', sizes=[(16,16),(32,32),(48,48)])

# logo wordmark (2x)
H=240
tmp = Image.new('RGBA',(1400,H),(0,0,0,0)); d=ImageDraw.Draw(tmp)
m = monogram(H-20); tmp.paste(m,(0,10),m)
x = H+10
f1=font(112); f2=sans(30)
d.text((x,18),'Butler',font=f1,fill=BURG)
# letterspaced subtitle
sx=x+4; y=148
for ch in 'LEGAL SERVICES':
    d.text((sx,y),ch,font=f2,fill=GOLD)
    sx += d.textlength(ch,font=f2)+9
w = int(max(sx, x+d.textlength('Butler',font=f1)))+24
tmp.crop((0,0,w,H)).save(f'{out}/logo.png')

# og image 1200x630
og = Image.new('RGB',(1200,630),BG); d=ImageDraw.Draw(og)
d.rectangle((0,0,1200,630),fill=DARK)
d.rectangle((0,0,1200,630),fill=BURG)
d.rectangle((60,60,1140,570),outline=GOLD,width=3)
mm = monogram(150); og.paste(mm,(90,100),mm)
d.text((270,100),'Butler Legal Services',font=font(64),fill=(255,255,255))
d.text((270,185),'LICENSED PARALEGAL  |  ONTARIO',font=sans(24),fill=(232,207,143))
d.text((90,320),'Provincial Offences &',font=font(70),fill=(255,255,255))
d.text((90,405),'Small Claims Court',font=font(70),fill=(255,255,255))
d.text((90,505),'butlerlegalservices.ca',font=sans(28),fill=(232,207,143))
og.save(f'{out}/og-image.jpg', quality=90)
print('assets ok')
