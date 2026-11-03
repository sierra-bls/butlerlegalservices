"""Builds favicons, social image and site logo files from brand/*.png.  Usage: make_assets.py <site-dir>"""
import sys, shutil, os, glob
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__)); brand = os.path.join(here, 'brand')
BG = (250,246,240)
for f in ('logo.png','monogram.png','logo-horizontal.png'):
    shutil.copy(os.path.join(brand,f), os.path.join(out,f))
mono = Image.open(os.path.join(brand,'monogram.png'))
def square(img, size, bg=None, pad=0.12):
    s = Image.new('RGBA',(size,size), bg or (0,0,0,0))
    w = int(size*(1-2*pad)); h = round(img.height*w/img.width)
    if h > size*(1-2*pad): h = int(size*(1-2*pad)); w = round(img.width*h/img.height)
    r = img.resize((w,h), Image.LANCZOS); s.paste(r,((size-w)//2,(size-h)//2),r); return s
for n,name,bg in ((16,'favicon-16x16.png',None),(32,'favicon-32x32.png',None),(48,'favicon-48x48.png',None),
                  (180,'apple-touch-icon.png',BG+(255,)),(192,'android-chrome-192x192.png',BG+(255,)),(512,'android-chrome-512x512.png',BG+(255,))):
    sq = square(mono, n*4 if n<64 else n, bg, 0.06 if n<64 else 0.14)
    sq = sq.resize((n,n), Image.LANCZOS) if n<64 else sq
    (sq.convert('RGB') if bg else sq).save(os.path.join(out,name))
square(mono,256,None,0.04).save(os.path.join(out,'favicon.ico'), sizes=[(16,16),(32,32),(48,48)])
# og image 1200x630
og = Image.new('RGB',(1200,630),BG); d = ImageDraw.Draw(og)
d.rectangle((24,24,1175,605), outline=(184,146,58), width=3)
full = Image.open(os.path.join(brand,'logo.png')); fh = 360; fw = round(full.width*fh/full.height)
f2 = full.resize((fw,fh), Image.LANCZOS); og.paste(f2,((1200-fw)//2,60),f2)
def sf(sz):
    p = glob.glob('/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf')
    if p:
        f = ImageFont.truetype(p[0], sz)
        try: f.set_variation_by_name('Bold')
        except Exception: pass
        return f
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', sz)
t = 'Small Claims | Traffic Tickets | Charges'
tw = d.textlength(t, font=sf(38)); d.text(((1200-tw)/2, 470), t, font=sf(38), fill=(122,31,61))
t2 = 'Licensed paralegal representing clients across Ontario'
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24); tw = d.textlength(t2, font=f)
d.text(((1200-tw)/2, 535), t2, font=f, fill=(90,80,86))
og.save(os.path.join(out,'og-image.jpg'), quality=90)
print('assets ok')
