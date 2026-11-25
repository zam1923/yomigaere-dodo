"""漫画のコマから、縦長(1080x1920)のリール動画を作る。
使い方: python3 kit/reel.py ep01 "第1話　よみがえれ、ドードー" "図鑑メモの文" → reels/ep01.mp4
"""
import sys,os,asyncio,subprocess,tempfile,importlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.insert(0,os.path.join(ROOT,'kit')); sys.path.insert(0,os.path.join(ROOT,'episodes'))
W,H=1080,1920; FPS=30; SEC=2.6; FADE=0.35
BG=(246,239,226); INK=(91,70,54)
def font(size):
    for p in ['/tmp/ZenMaruGothic-Black.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
async def render_panels(P,tmp,title,memo):
    from playwright.async_api import async_playwright
    out=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1000,'height':560},device_scale_factor=1.08)
        for i,s in enumerate(P):
            await pg.set_content('<html><head><link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap" rel="stylesheet"></head><body style="margin:0">'+s+'</body></html>')
            await pg.wait_for_timeout(1200); f=f'{tmp}/p{i:02d}.png'; await pg.screenshot(path=f); out.append(f)
        F='<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap" rel="stylesheet">'
        head=f'<div style="position:absolute;top:190px;width:1080px;text-align:center"><div style="font-size:66px;font-weight:900;color:#a9bdb6;-webkit-text-stroke:8px #5b4636;paint-order:stroke fill;letter-spacing:6px">よみがえれ、ドードー</div><div style="margin-top:26px;font-size:44px;font-weight:900;color:#5b4636">{title}</div></div>'
        pg2=await b.new_page(viewport={'width':1080,'height':1920})
        await pg2.set_content(f'<html><head>{F}</head><body style="margin:0;width:1080px;height:1920px;background:#f6efe2;font-family:Zen Maru Gothic;position:relative">{head}</body></html>')
        await pg2.wait_for_timeout(1500); await pg2.screenshot(path=f'{tmp}/base.png')
        await pg2.set_content(f'<html><head>{F}</head><body style="margin:0;width:1080px;height:1920px;background:#f6efe2;font-family:Zen Maru Gothic;position:relative;color:#5b4636">{head}<div style="position:absolute;top:760px;left:80px;width:840px;padding:40px;background:#fff8ee;border-radius:30px;font-size:42px;line-height:1.65"><b>図鑑メモ</b><br>{memo}</div><div style="position:absolute;top:1360px;width:1080px;text-align:center;font-size:58px;font-weight:900;color:#9a8572">つづく</div></body></html>')
        await pg2.wait_for_timeout(1500); await pg2.screenshot(path=f'{tmp}/end.png')
        await b.close()
    return out
def ensure_font():
    p='/tmp/ZenMaruGothic-Black.ttf'
    if not os.path.exists(p):
        subprocess.run(['curl','-sL','-o',p,'https://github.com/google/fonts/raw/main/ofl/zenmarugothic/ZenMaruGothic-Black.ttf'],check=False)
def base_old(title):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((W//2,250),'よみがえれ、ドードー',font=font(64),fill=(169,189,182),anchor='mm',stroke_width=8,stroke_fill=INK)
    d.text((W//2,350),title,font=font(44),fill=INK,anchor='mm')
    return im
def frames(panels,title,memo,tmp):
    k=0; bg=Image.open(f'{tmp}/base.png').convert('RGB')
    def put(im):
        nonlocal k; im.save(f'{tmp}/f{k:05d}.jpg',quality=90); k+=1
    for i,pf in enumerate(panels):
        p=Image.open(pf).convert('RGB'); pw=1040; ph=int(p.height*pw/p.width)
        n=int(SEC*FPS)
        for t in range(n):
            z=1.0+0.035*t/n
            q=p.resize((int(pw*z),int(ph*z)),Image.LANCZOS)
            cx=(q.width-pw)//2; cy=(q.height-ph)//2; q=q.crop((cx,cy,cx+pw,cy+ph))
            fr=bg.copy(); fr.paste(q,((W-pw)//2,(H-ph)//2+60))
            a=min(1,t/(FADE*FPS))
            if i>0 and a<1: fr=Image.blend(prev,fr,a)
            put(fr)
        prev=fr
    end=Image.open(f'{tmp}/end.png').convert('RGB')
    for t in range(int(3.5*FPS)): put(Image.blend(prev,end,min(1,t/(FADE*FPS))))
    return k
def main(ep,title,memo):
    mod=importlib.import_module(ep); P=mod.P
    os.makedirs(os.path.join(ROOT,'reels'),exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        panels=asyncio.run(render_panels(P,tmp,title,memo))
        frames(panels,title,memo,tmp)
        out=os.path.join(ROOT,'reels',f'{ep}.mp4')
        subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{tmp}/f%05d.jpg','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest',
                        '-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-movflags','+faststart',out],check=True)
    print(out)
if __name__=='__main__': main(*sys.argv[1:4])
