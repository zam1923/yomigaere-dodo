import sys,random,math,json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import logos2 as Lg
from logos2 import *
def palm(u,x,y,h,lean,seed,sc=1):
    r=random.Random(seed); s=''
    tx=x+lean; ty=y-h
    s+=pen(u,f'M{x} {y} Q{x+lean*0.3} {y-h*0.6} {tx} {ty}',7*sc,'#7a5e44',op=.95)
    s+=pen(u,f'M{x} {y} Q{x+lean*0.3} {y-h*0.6} {tx} {ty}',3.5*sc,'#a3825e',op=.9)
    for i in range(int(h/14)):  # 幹の節
        t=i/(h/14); px=x+lean*0.3*2*t*(1-t)+lean*t*t; py=y-h*t
        s+=pen(u,f'M{px-4*sc:.0f} {py:.0f} l{8*sc:.0f} -2',1.2,op=.6)
    for k in range(9):
        a=-math.pi/2+(k-4)*0.42+r.uniform(-.1,.1); L=r.uniform(60,90)*sc
        ex=tx+math.cos(a)*L; ey=ty+math.sin(a)*L*0.7+L*0.35
        mx=tx+math.cos(a)*L*0.55; my=ty+math.sin(a)*L*0.55-12*sc
        leaf=f'M{tx:.0f} {ty:.0f} Q{mx:.0f} {my-8*sc:.0f} {ex:.0f} {ey:.0f} Q{mx:.0f} {my+10*sc:.0f} {tx:.0f} {ty:.0f}Z'
        s+=wash(u,leaf,r.choice(['#7f9e68','#8aa872','#6f8f5c']))+pen(u,f'M{tx:.0f} {ty:.0f} Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}',1.6,op=.8)
        for j in range(1,7):
            t=j/7; qx=(1-t)**2*tx+2*(1-t)*t*mx+t*t*ex; qy=(1-t)**2*ty+2*(1-t)*t*my+t*t*ey
            s+=pen(u,f'M{qx:.0f} {qy:.0f} l{r.uniform(-6,6):.0f} {10*sc:.0f}',1,'#55704a',op=.6)
    return s
def ship(u,x,y,s=1):
    ink='#5d4a3a'
    h=f'M{x-40*s} {y-10*s} Q{x} {y+6*s} {x+44*s} {y-14*s} L{x+36*s} {y} Q{x} {y+8*s} {x-32*s} {y}Z'
    o=wash(u,h,'#8b6a4c')+pen(u,h,1.6,ink)
    for mx,mh in [(-16,58),(4,70),(24,50)]:
        o+=pen(u,f'M{x+mx*s} {y-8*s} L{x+mx*s} {y-(8+mh)*s}',1.4,ink)
        for k,(w,hh) in enumerate([(14,16),(11,13)]):
            yy=y-(14+k*22)*s - (mh-50)*s*0.5
            sail=f'M{x+(mx-w)*s} {yy-hh*s} Q{x+mx*s} {yy-hh*s-3} {x+(mx+w)*s} {yy-hh*s} Q{x+(mx+w+3)*s} {yy} {x+(mx+w)*s} {yy} L{x+(mx-w)*s} {yy}Q{x+(mx-w+3)*s} {yy-hh*s/2} {x+(mx-w)*s} {yy-hh*s}Z'
            o+=f'<path d="{sail}" fill="#f6efdc" stroke="{ink}" stroke-width="1.2"/>'
    o+=f'<path d="M{x+4*s} {y-78*s} l12 3 l-12 3Z" fill="#c4473a"/>'
    o+=pen(u,f'M{x-40*s} {y-10*s} L{x-56*s} {y-22*s}',1.2,ink)
    return o
def B3i(u,bare=False):
    r=random.Random(21); s=''
    s+=f'''<defs><linearGradient id="skB{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efe2c2"/><stop offset=".55" stop-color="#f6ecd4"/><stop offset="1" stop-color="#f3e6c6"/></linearGradient>
<radialGradient id="vg{u}" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#5a4128" stop-opacity=".35"/></radialGradient>
<radialGradient id="egB{u}" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#fffdf6"/><stop offset=".7" stop-color="#f4ead4"/><stop offset="1" stop-color="#dccaa4"/></radialGradient></defs>
<rect width="900" height="440" fill="url(#skB{u})"/>'''
    # 雲(にじみ)
    for x,y,w in [(140,60,140),(520,40,120),(760,80,100)]:
        s+=wash(u,f'M{x-w/2} {y} Q{x-w/3} {y-24} {x} {y-16} Q{x+w/3} {y-30} {x+w/2} {y} Z','#fbf6ea',.9)
    hz=302
    # 遠い山(モーリシャスの尖った峰と親指の岩)
    mt=f'M20 {hz} L70 {hz-34} L110 {hz-28} L150 {hz-60} L176 {hz-98} L186 {hz-112} L196 {hz-98} L214 {hz-62} L260 {hz-44} L300 {hz-52} L330 {hz-70} L346 {hz-84} L360 {hz-70} L400 {hz-38} L460 {hz-22} L520 {hz} Z'
    s+=wash(u,mt,'#a9b7b0',.85)+pen(u,mt.replace(' Z',''),1.6,'#6f6a5c',op=.7)
    s+=f'<circle cx="186" cy="{hz-118}" r="7" fill="#a9b7b0" filter="url(#wc{u})"/>'+pen(u,f'M179 {hz-118} a7 7 0 1 0 14 0 a7 7 0 1 0 -14 0',1.4,'#6f6a5c',op=.7)
    for i in range(18):  # 山のハッチング
        x=60+i*22; s+=pen(u,f'M{x} {hz-4} l{8} -{r.uniform(10,26):.0f}',0.9,'#6f6a5c',op=.35)
    # 海
    s+=wash(u,f'M0 {hz} L900 {hz} L900 {hz+44} L0 {hz+44}Z','#b9cfc8',.9)+pen(u,f'M0 {hz} L900 {hz}',1.6,'#6f6a5c',op=.8)
    for _ in range(26):
        x=r.uniform(0,880); y=r.uniform(hz+6,hz+40); w=r.uniform(10,26)
        s+=pen(u,f'M{x:.0f} {y:.0f} q{w/4:.0f} -3 {w/2:.0f} 0 q{w/4:.0f} 3 {w/2:.0f} 0',1,'#6f8b85',op=.6)
    # 沖の帆船(人間がやってきた)
    s+=ship(u,470,hz+2,0.55)
    # 浜と地面
    s+=wash(u,band(-20,900,hz+40,440,5,7),'#eadbb6')+pen(u,wavy(-20,920,hz+40,5,7),1.8,op=.7)
    s+=wash(u,band(-20,900,hz+62,440,6,8),'#b8cf98')+pen(u,wavy(-20,920,hz+62,6,8),2.4)
    for x in range(10,900,42): s+=grass(u,x,hz+66,6,20,x)
    # ヤシ(左端と右端で画面をはさむ)
    s+=palm(u,30,440,250,40,1,1.0)+palm(u,880,440,270,-50,2,1.05)
    # シダ・低木
    for x,y in [(110,420),(540,430),(860,420)]:
        for k in range(6):
            a=-math.pi/2+(k-2.5)*0.4
            s+=pen(u,f'M{x} {y} q{math.cos(a)*20:.0f} {math.sin(a)*30:.0f} {math.cos(a)*44:.0f} {math.sin(a)*34:.0f}',2,'#6b8a58',op=.9)
    # ---- 前景: 巣・たまご・トト(前と同じ) ----
    fg=''
    nest=''
    for i in range(70):
        cx=700+r.uniform(-130,130); cy=372+r.uniform(-12,14); L=r.uniform(40,90); a=r.uniform(-0.35,0.35)
        x1=cx-math.cos(a)*L/2; y1=cy-math.sin(a)*L/2; x2=cx+math.cos(a)*L/2; y2=cy+math.sin(a)*L/2
        col=r.choice(['#9b7a52','#b08d62','#86684a','#c2a074'])
        nest+=f'<path d="M{x1:.0f} {y1:.0f} Q{cx:.0f} {cy+r.uniform(-8,8):.0f} {x2:.0f} {y2:.0f}" stroke="{col}" stroke-width="{r.uniform(2,4):.1f}" fill="none" stroke-linecap="round"/>'
    fg+=f'<ellipse cx="700" cy="390" rx="150" ry="18" fill="#6b5444" opacity=".35" filter="url(#bl{u})"/>'+wash(u,'M570 362 Q700 330 830 362 Q840 392 700 398 Q560 392 570 362Z','#a8865c')
    zig='M604 232 L628 214 L646 236 L668 206 L690 234 L712 204 L734 232 L756 210 L782 236 L798 220'
    eggd=f'{zig} Q808 300 748 352 Q704 374 658 352 Q596 300 604 232Z'
    EG='M0 -125 C70 -125 104 -20 100 30 C96 95 50 125 0 125 C-50 125 -96 95 -100 30 C-104 -20 -70 -125 0 -125Z'
    sp=''
    rr=random.Random(8)
    for _ in range(14):
        a=rr.uniform(0,6.28); d=rr.uniform(.25,.9); px=math.cos(a)*88*d; py=math.sin(a)*110*d
        if px*px+(py-10)**2<50**2: continue
        sp+=f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rr.uniform(3,8):.1f}" ry="{rr.uniform(2,5):.1f}" fill="#b89766" opacity=".75" filter="url(#wc{u})"/>'
    st=f'<g transform="rotate(-12 0 10)"><circle cx="0" cy="10" r="42" fill="none" stroke="#c4473a" stroke-width="5"/><circle cx="0" cy="10" r="33" fill="none" stroke="#c4473a" stroke-width="2"/><text x="0" y="23" text-anchor="middle" font-family="{F}" font-weight="900" font-size="31" fill="#c4473a">絶滅</text></g>'
    fg+=f'<g transform="translate(700 250) rotate(6) scale(.95)"><path d="{EG}" fill="url(#egB{u})"/>{sp}<g filter="url(#ink{u})" opacity=".9">{st}</g><path d="{EG}" fill="none" stroke="{O}" stroke-width="4.2" filter="url(#pn{u})"/><path d="M58 -40 Q74 0 64 40" fill="none" stroke="#fffdf6" stroke-width="5" stroke-linecap="round" opacity=".8"/></g>'
    fg+=f'<g>{nest}</g>'
    s+=('' if bare else f'<g transform="translate(0 30)">{fg}</g>')
    s+=f'<rect width="900" height="440" fill="url(#vg{u})"/>'
    # 古い版画の枠
    s+=f'<rect x="12" y="12" width="876" height="416" rx="18" fill="none" stroke="#6b5444" stroke-width="2" opacity=".55"/><rect x="20" y="20" width="860" height="400" rx="14" fill="none" stroke="#6b5444" stroke-width="1" opacity=".45"/>'
    top=T(290,120,'よみがえれ、',56,'#fff8ee',11,6)+T(300,240,'ドードー',116,'#a9bdb6',14,4)+tw(70,80,.9)+tw(540,70,.8)
    return wrap(u,s,'#f3e6c6','' if bare else top)