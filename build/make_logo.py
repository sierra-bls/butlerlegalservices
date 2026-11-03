import numpy as np, sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(float)
fgs = np.array([[117,22,50],[197,155,90],[35,35,35]], float)
mn = im.min(axis=2)
a = np.clip((250 - mn) / 70.0, 0, 1)
# unmix direction vs white to pick nearest brand colour
d = 255 - im; dn = d / (np.linalg.norm(d, axis=2, keepdims=True) + 1e-6)
fd = 255 - fgs; fdn = fd / np.linalg.norm(fd, axis=1, keepdims=True)
idx = np.argmax(dn @ fdn.T, axis=2)
rgb = fgs[idx]
rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
full = Image.fromarray(rgba, 'RGBA')
def trim(img, pad=8):
    bb = img.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()
    c = img.crop(bb)
    n = Image.new('RGBA', (c.width + 2*pad, c.height + 2*pad), (0,0,0,0)); n.paste(c, (pad, pad)); return n
H = full.height
# find row gap between monogram and wordmark
alpha = np.asarray(full)[:,:,3] > 40
rows = alpha.any(axis=1)
gaps=[]; start=None
for y,v in enumerate(rows):
    if not v and start is None: start=y
    if v and start is not None: gaps.append((start,y)); start=None
big = max([g for g in gaps if g[0]>100 and g[1]<H-100], key=lambda g:g[1]-g[0])
cut = (big[0]+big[1])//2
mono = trim(full.crop((0,0,full.width,cut)))
word = trim(full.crop((0,cut,full.width,H)))
fullt = trim(full)
fullt.save(f'{out}/logo.png'); mono.save(f'{out}/monogram.png')
# horizontal lockup: monogram left, wordmark right
mh = 300
m2 = mono.resize((round(mono.width*mh/mono.height), mh), Image.LANCZOS)
wh = 190
w2 = word.resize((round(word.width*wh/word.height), wh), Image.LANCZOS)
gap = 40
lock = Image.new('RGBA', (m2.width+gap+w2.width, mh), (0,0,0,0))
lock.paste(m2,(0,0),m2); lock.paste(w2,(m2.width+gap,(mh-wh)//2),w2)
trim(lock,4).save(f'{out}/logo-horizontal.png')
print('full',fullt.size,'mono',mono.size,'word',word.size,'lock',trim(lock,4).size)
