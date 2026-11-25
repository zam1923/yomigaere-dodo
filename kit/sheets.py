import json,sys,asyncio
from playwright.async_api import async_playwright
O='#5b4636'
HEAD='''<div style="padding:30px 40px 0;display:flex;align-items:flex-end;gap:18px"><svg viewBox="0 0 420 110" width="420" height="110"><text x="4" y="40" font-family="Zen Maru Gothic" font-weight="900" font-size="30" fill="#fff8ee" stroke="#5b4636" stroke-width="7" stroke-linejoin="round" paint-order="stroke" letter-spacing="4">よみがえれ、</text><text x="2" y="102" font-family="Zen Maru Gothic" font-weight="900" font-size="62" fill="#a9bdb6" stroke="#5b4636" stroke-width="9" stroke-linejoin="round" paint-order="stroke" letter-spacing="6">ドードー</text></svg></div>'''
def page(panels,head,foot,n,tot):
    return f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap" rel="stylesheet"></head><body style="margin:0;background:#f6efe2;width:1080px;font-family:'Zen Maru Gothic',sans-serif;color:{O}">
{head}<div style="display:flex;flex-direction:column;gap:22px;padding:{'8' if head else '36'}px 40px 0">{''.join(panels)}</div>{foot}
<div style="text-align:right;padding:0 44px 26px;font-size:20px;font-weight:700;color:#9a8572">{n} / {tot}</div></body></html>'''
async def render(name,P,title,memo,logo_head=True,per=4):
    pages=[P[i:i+per] for i in range(0,len(P),per)]; tot=len(pages)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':800}); out=[]
        for i,pp in enumerate(pages,1):
            head=((HEAD if logo_head else '')+f'<div style="padding:{"10" if logo_head else "30"}px 44px 6px;font-size:28px;font-weight:900">{title}</div>') if i==1 else ''
            foot=(f'<div style="margin:24px 40px 14px;padding:18px 24px;background:#fff8ee;border-radius:18px;font-size:22px;line-height:1.7"><b>図鑑メモ</b><br>{memo}</div>' if i==tot else '<div style="text-align:center;padding:22px 0 4px;font-size:26px;font-weight:900;color:#9a8572">つづく →</div>')
            open('/tmp/sh.html','w').write(page(pp,head,foot,i,tot))
            await pg.goto('file:///tmp/sh.html'); await pg.wait_for_timeout(2200)
            f=f'out/{name}_{i}.png'; await pg.screenshot(path=f,full_page=True); out.append(f)
        await b.close(); return out
