import sys,re,math,random
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import gen, turn
random.seed(4)
O='#5b4636'
S=f'stroke="{O}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
L='fill="none" '+S
W,H=1000,560
def g(svg,x,y,s=1.0,rot=0,flip=False):
    f=' translate(200 0) scale(-1 1)' if flip else ''
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate(-100 -110){f}">{svg}</g>'
# ---------- トトの部品 ----------
def eyes_sparkle(x1,x2,y,r=11):
    e=''
    for x in (x1,x2):
        e+=f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.12}" fill="{O}"/><circle cx="{x+r*0.35}" cy="{y-r*0.4}" r="{r*0.38}" fill="#fff"/><circle cx="{x-r*0.38}" cy="{y+r*0.35}" r="{r*0.18}" fill="#fff"/>'
    return e
def toto_face(kind):
    base=gen.CREST+gen.HEAD+gen.BEAK
    if kind=='spark': return base+gen.BEAKLINE+eyes_sparkle(74,126,96)+gen.cheek(54,118,13,8,'.9')+gen.cheek(146,118,13,8,'.9')
    if kind=='notice': return base+gen.BEAKLINE+gen.eye(74,98,6.5)+gen.eye(126,98,6.5)+gen.CHEEKS
    return gen.face(kind)
def toto_front(kind='n',feet=True,wing='rest'):
    wings=gen.wingsA if wing=='rest' else (f'<path d="M40 104 Q10 84 6 58 Q30 70 46 96Z" fill="#94aba3" {S}/><path d="M160 104 Q190 84 194 58 Q170 70 154 96Z" fill="#94aba3" {S}/>')
    return (gen.feetA if feet else '')+wings+toto_face(kind)
def toto_dive():   # 左に飛びつく(斜め前の体を前のめり、足は後ろへ)
    body=re.sub(r'<g stroke="#b7862f".*?</g>','',turn.three(),count=1)
    legs=f'<g stroke="#b7862f" stroke-width="5" stroke-linecap="round" fill="none"><path d="M120 160 L150 178 M150 178 L166 172 M150 178 L164 188"/><path d="M134 150 L168 160 M168 160 L182 152 M168 160 L182 170"/></g>'
    return legs+body
# ---------- マロ ----------
def maro(eyes='n',claw='down',berry=False,bite=False):
    flaps=gen_both(f'<ellipse cx="42" cy="96" rx="17" ry="10" fill="#f8d695" {S}/><ellipse cx="38" cy="120" rx="17" ry="10" fill="#f8d695" {S}/><ellipse cx="46" cy="144" rx="17" ry="10" fill="#f8d695" {S}/>')
    if eyes=='smug': e1=f'<circle cx="48" cy="50" r="12" fill="#fff" {S}/><circle cx="50" cy="55" r="4.5" fill="{O}"/><path d="M36.5 50 A12 12 0 0 1 59.5 50Z" fill="#f0b65a" stroke="{O}" stroke-width="4" stroke-linejoin="round"/>'
    else: e1=f'<circle cx="48" cy="50" r="12" fill="#fff" {S}/><circle cx="50" cy="51" r="5" fill="{O}"/>'
    stalks=gen_both(f'<path d="M68 78 L50 54" {L}/>'+e1)
    body=f'<ellipse cx="100" cy="116" rx="52" ry="54" fill="#f0b65a" {S}/>'
    cl=lambda d: f'<path d="{d}" fill="none" stroke="{O}" stroke-width="16" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#e7963a" stroke-width="7" stroke-linecap="round"/>'
    left=cl('M84 130 Q74 152 88 162 Q98 164 97 152')
    if claw=='up': right=cl('M118 120 Q150 96 150 52 Q150 36 138 38')
    elif claw=='eat': right=cl('M116 130 Q130 128 124 112 Q118 104 110 110')
    else: right=cl('M116 130 Q126 152 112 162 Q102 164 103 152')
    mouth=f'<path d="M90 112 Q100 120 110 112" {L}/>' if claw!='eat' else f'<ellipse cx="100" cy="116" rx="7" ry="6" fill="#c0564a" stroke="{O}" stroke-width="3"/>'
    s=flaps+stalks+body+left+right+mouth+gen.cheek(70,106)+gen.cheek(130,106)
    if berry=='up': s+=BERRY(140,30,15)
    elif berry=='hand': s+=BERRY(118,166,15)
    elif berry=='eat': s+=BERRY(112,104,13,True)+''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#e2564e"/>' for x,y in [(84,136),(124,140),(96,146)])
    return s
def gen_both(d): return d+f'<g transform="translate(200 0) scale(-1 1)">{d}</g>'
def BERRY(x,y,r=16,bite=False):
    s=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e2564e" {S.replace("5","4",1)}/><circle cx="{x-r*.35}" cy="{y-r*.35}" r="{r*.22}" fill="#fff" opacity=".75"/><path d="M{x} {y-r} q5 -11 15 -9 q-5 9 -15 9Z" fill="#7fb069" stroke="{O}" stroke-width="3" stroke-linejoin="round"/>'
    if bite: s+=f'<path d="M{x+r*.3} {y-r*.9} A{r*.5} {r*.5} 0 0 0 {x+r*.95} {y+r*.2}" fill="#f6efe2" stroke="{O}" stroke-width="3"/>'
    return s
# ---------- 漫画の記号 ----------
def heart(x,y,s=1,rot=0): return f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0 6 C-10 -6 -22 4 0 20 C22 4 10 -6 0 6Z" fill="#f2879a" stroke="{O}" stroke-width="2.5"/>'
def twinkle(x,y,s=1): return f'<path transform="translate({x} {y}) scale({s})" d="M0 -16 Q2 -2 16 0 Q2 2 0 16 Q-2 2 -16 0 Q-2 -2 0 -16Z" fill="#fff6c8" stroke="{O}" stroke-width="2.5" stroke-linejoin="round"/>'
def bang(x,y,s=1,rot=-8): return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M-6 -40 L8 -40 L4 6 L-3 6Z" fill="{O}"/><circle cx="1" cy="18" r="6" fill="{O}"/></g>'
def flaplines(x,y,side=1): return ''.join(f'<path d="M{x+side*i*10} {y+i*14} q{side*16} -6 {side*26} 2" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>' for i in range(3))
def dust(x,y,s=1): return ''.join(f'<circle cx="{x+dx*s}" cy="{y+dy*s}" r="{r*s}" fill="#efe4cf" stroke="{O}" stroke-width="3"/>' for dx,dy,r in [(-40,0,14),(-20,-14,18),(4,-6,16),(28,-12,13),(44,2,11)])
def speed(y0,y1,n=14):
    return ''.join(f'<path d="M{random.randint(560,1000)} {y} L{random.randint(80,380)} {y}" stroke="{O}" stroke-width="{random.choice([2,3,4])}" stroke-linecap="round" opacity=".35"/>' for y in [y0+(y1-y0)*i/n+random.randint(-6,6) for i in range(n)])
def burst(cx,cy,n=40,r0=230,r1=600):
    s=''
    for i in range(n):
        a=i*2*math.pi/n+random.uniform(-.04,.04); w=random.uniform(.008,.022)
        s+=f'<path d="M{cx+r0*math.cos(a-w):.0f} {cy+r0*math.sin(a-w):.0f} L{cx+r1*math.cos(a):.0f} {cy+r1*math.sin(a):.0f} L{cx+r0*math.cos(a+w):.0f} {cy+r0*math.sin(a+w):.0f}Z" fill="{O}" opacity=".18"/>'
    return s
# ---------- 背景 ----------
def tree(x,y,h,w,c1,c2): return f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" rx="{w/3}" fill="{c1}"/>'+''.join(f'<circle cx="{x+dx}" cy="{y-h+dy}" r="{r}" fill="{c2}"/>' for dx,dy,r in [(-w*1.6,10,w*1.5),(w*1.4,0,w*1.6),(0,-w*.8,w*1.9)])
def bush(x,y,s=1,c='#9cc07f'): return ''.join(f'<circle cx="{x+dx*s}" cy="{y+dy*s}" r="{r*s}" fill="{c}" stroke="{O}" stroke-width="3.5"/>' for dx,dy,r in [(-34,0,26),(0,-14,32),(34,0,26)])
def bg_forest(hz=430):
    s=f'<rect width="{W}" height="{H}" fill="#eef5e4"/>'
    s+=tree(80,hz-10,300,26,'#d9ccb0','#d2e4c0')+tree(930,hz-20,320,30,'#d9ccb0','#d2e4c0')+tree(720,hz-40,220,18,'#e3d8c0','#dbead0')+tree(280,hz-50,200,16,'#e3d8c0','#dbead0')
    s+=f'<path d="M0 {hz} Q300 {hz-24} 600 {hz-8} T1000 {hz} L1000 {H} L0 {H}Z" fill="#cfe3b6" stroke="{O}" stroke-width="3.5"/>'
    s+=''.join(f'<path d="M{x} {hz+30+(x%5)*6} l5 -12 l5 12" fill="none" stroke="#86ad69" stroke-width="3" stroke-linecap="round"/>' for x in range(40,1000,73))
    return s
FILT='<filter id="hand" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="1" seed="11"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>'
def panel(inner,idx):
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"><defs>{FILT}<clipPath id="c{idx}"><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="6"/></clipPath></defs><g clip-path="url(#c{idx})"><g filter="url(#hand)">{inner}</g></g><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="6" fill="none" stroke="{O}" stroke-width="6" filter="url(#hand)"/></svg>'
P=[]
# 1 引き: 葉の陰から実をちらつかせるマロ / 遠くで気づくトト
p=bg_forest(440)
p+=g(maro('smug','up','up'),250,300,1.05)+bush(250,420,1.6,'#a9cc8c')
p+=g(toto_front('notice'),760,330,0.72)+twinkle(706,268,0.9)+twinkle(796,262,0.6)+bang(830,220,0.8,12)
P.append(panel(p,1))
# 2 アップ: キラキラ目のトト、羽ぱたぱた
p=f'<rect width="{W}" height="{H}" fill="#fff3d6"/>'+burst(500,300,48,260,700)
p+=''.join(heart(x,y,s,r) for x,y,s,r in [(170,120,1.6,-14),(830,140,1.3,12),(120,400,1.1,-20),(880,420,1.5,16)])
p+=g(toto_front('spark',False,'up'),500,330,2.6)+flaplines(170,250,-1)+flaplines(830,250,1)
P.append(panel(p,2))
# 3 動き: 飛びつくトト、実をひょいと上げるマロ、空振り
p=f'<rect width="{W}" height="{H}" fill="#f4f8ec"/>'+speed(140,460,16)
p+=f'<path d="M0 470 L1000 470 L1000 560 L0 560Z" fill="#cfe3b6" stroke="{O}" stroke-width="3.5"/>'
p+=g(maro('smug','up','up'),260,310,1.25)
p+=f'<path d="M420 300 Q400 160 330 110" fill="none" stroke="{O}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>'
p+=g(toto_dive(),520,320,1.3,-22)
p+=f'<path d="M392 318 q-26 -6 -40 10" fill="none" stroke="{O}" stroke-width="4" stroke-linecap="round"/><path d="M398 340 q-30 2 -44 22" fill="none" stroke="{O}" stroke-width="4" stroke-linecap="round"/>'
p+=bang(640,150,0.9,10)
P.append(panel(p,3))
# 4 オチ: めり込んだトト、となりに同じへこみが2つ。マロは実をかじる
hz=380
p=f'<rect width="{W}" height="{H}" fill="#eef5e4"/>'+tree(900,hz,260,26,'#d9ccb0','#d2e4c0')
p+=f'<path d="M0 {hz} Q500 {hz-16} 1000 {hz} L1000 {H} L0 {H}Z" fill="#cfe3b6" stroke="{O}" stroke-width="3.5"/>'
for cx in (150,330):
    p+=f'<ellipse cx="{cx}" cy="{hz+60}" rx="62" ry="22" fill="#8fae74" stroke="{O}" stroke-width="3.5"/><path d="M{cx-14} {hz+44} q6 -14 12 -2 q6 -12 12 2" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round"/>'
# トト(さかさま): 体を描いてから、手前の地面で頭をかくす
toto_up=g(toto_front('n'),560,hz+40,1.05,180)
p+=toto_up+f'<path d="M400 {hz+40} Q560 {hz+14} 720 {hz+40} L720 {H} L400 {H}Z" fill="#cfe3b6"/><path d="M410 {hz+40} Q560 {hz+16} 710 {hz+40}" fill="none" stroke="{O}" stroke-width="4" stroke-linecap="round"/>'
p+=dust(470,hz+40,1.0)+dust(660,hz+44,0.9)
p+=f'<g stroke="{O}" stroke-width="3.5" stroke-linecap="round" fill="none"><path d="M520 {hz-120} l-12 -10"/><path d="M600 {hz-120} l12 -10"/><path d="M512 {hz-96} l-16 -2"/><path d="M608 {hz-96} l16 -2"/></g>'+heart(560,hz-150,1.2,10)
p+=g(maro('smug','eat','eat'),840,hz-10,1.1)
P.append(panel(p,4))
open('ep1b_panels.txt','w').write('\n'.join(P))
