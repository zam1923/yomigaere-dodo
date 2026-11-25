"""LINEスタンプ第1弾: トトの8種(文字なし)。python3 stamps/make_set1.py で stamps/set1/ にPNGができる"""
import sys,os,asyncio
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','kit'))
import gen
from ep1b import heart, twinkle, bang
from epkit import sweat, zzz, qmark, O
def body(k): return gen.A_body(k)
anger=f'<path transform="translate(150 40) scale(1.2)" d="M-10 -4 Q-4 -4 -4 -10 M4 -10 Q4 -4 10 -4 M10 4 Q4 4 4 10 M-4 10 Q-4 4 -10 4" fill="none" stroke="#d9573f" stroke-width="4.5" stroke-linecap="round"/>'
tear='<path d="M70 108 Q78 126 70 134 Q62 126 70 108Z" fill="#9fd0ec" stroke="#5b4636" stroke-width="2.5"/>'
SET=[('01_hello','n',twinkle(160,40,.8)+'<path d="M168 92 q14 -14 20 -2 M172 108 q16 -6 18 6" fill="none" stroke="#5b4636" stroke-width="3.5" stroke-linecap="round"/>'),
     ('02_yay','smile',heart(165,45,1.0,12)+heart(35,55,.7,-12)),
     ('03_sleep','sleep',zzz(140,60,.7)),
     ('04_angry','angry',anger),
     ('05_sad','sad',tear),
     ('06_wow','wow',bang(165,40,.6,10)+twinkle(30,40,.7)),
     ('07_shy','shy','<path d="M40 30 l8 -12 M54 26 l6 -12 M148 26 l-6 -12 M160 30 l-8 -12" stroke="#5b4636" stroke-width="3" stroke-linecap="round"/>'),
     ('08_trouble','trouble',sweat(160,60,1.1)+qmark(20,70,.5))]
def svg(inner,w,h,vb):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">{inner}</svg>'
async def main():
    from playwright.async_api import async_playwright
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'set1')
    async with async_playwright() as p:
        b=await p.chromium.launch()
        async def shot(inner,w,h,vb,path):
            pg=await b.new_page(viewport={'width':w,'height':h})
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{svg(inner,w,h,vb)}</body></html>')
            await pg.screenshot(path=path,omit_background=True); await pg.close()
        for name,k,fx in SET:
            # 370x320、上下左右に10px以上の余白。キャラは中央
            await shot(body(k)+fx,370,320,'-32 -22 264 228',f'{out}/{name}.png')
        await shot(body('smile')+heart(165,45,1.0,12),240,240,'-12 -14 224 224',f'{out}/main.png')
        await shot(gen.CREST+gen.HEAD+gen.BEAK+gen.face('n') if hasattr(gen,'face') else body('n'),96,74,'-14 24 228 176',f'{out}/tab.png')
        await b.close()
asyncio.run(main())
