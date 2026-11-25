import sys,random,math,re,io,contextlib
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import ep1b
    from ep1b import heart, twinkle, bang, flaplines, burst, O, W, H, FILT, eyes_sparkle
    import logos2 as Lg
    from logoB3 import palm, ship
    import views, chars
from logos2 import wash, pen, wavy, band, grass, INK
F="'Zen Maru Gothic',sans-serif"
C={c['n']:c for c in chars.C}
SIL='#3a2f29'
def g(svg,x,y,s=1,rot=0,flip=False):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({-s if flip else s} {s}) translate(-100 -110)">{svg}</g>'
def sil(svg):
    svg=re.sub(r'fill="#[0-9a-fA-F]{3,6}"',f'fill="{SIL}"',svg); svg=re.sub(r'stroke="#[0-9a-fA-F]{3,6}"',f'stroke="{SIL}"',svg)
    return re.sub(r'opacity="[^"]*"','',svg)
# ---------- 表情 ----------
def eyes_k(c,k):
    if not c['eyes']: return ''
    x1,x2,y=c['eyes']
    if k=='spark': return eyes_sparkle(x1,x2,y,10)
    if k=='blank': return ''.join(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{O}"/>' for x in (x1,x2))
    if k=='happy': return ''.join(f'<path d="M{x-8} {y+3} Q{x} {y-8} {x+8} {y+3}" fill="none" stroke="{O}" stroke-width="4.5" stroke-linecap="round"/>' for x in (x1,x2))
    if k=='sleep': return ''.join(f'<path d="M{x-8} {y} Q{x} {y+6} {x+8} {y}" fill="none" stroke="{O}" stroke-width="4.5" stroke-linecap="round"/>' for x in (x1,x2))
    if k=='tear': return eyes_sparkle(x1,x2,y,10)+''.join(f'<path d="M{x+2} {y+12} Q{x+9} {y+24} {x+2} {y+30} Q{x-5} {y+24} {x+2} {y+12}Z" fill="#9fd0ec" stroke="{O}" stroke-width="2"/>' for x in (x1,x2))
    if k=='dizzy': return ''.join(swirl(x,y,7) for x in (x1,x2))
    if k=='shut': return ''.join(f'<path d="M{x-8} {y-4} L{x+8} {y+2} M{x-8} {y+6} L{x+8} {y+2}" fill="none" stroke="{O}" stroke-width="4" stroke-linecap="round"/>' for x in (x1,x2))
    return views.eye(x1,y)+views.eye(x2,y)
def ch(name,k='n',view='front'):
    c=C[name]
    if view=='side': return views.side(c)
    if view=='three': return views.three(c)
    if view=='back': return views.back(c)
    x1,x2,y=c['cheeks']
    return c.get('feet','')+c['back']+c['body']+c['face']+eyes_k(c,k)+views.cheek(x1,y)+views.cheek(x2,y)+c.get('prop','')
# ---------- 記号 ----------
def swirl(cx,cy,r=9):
    pts=[];t=0
    while t<=12: rr=1+t*r/12; pts.append(f'{cx+math.cos(t)*rr:.1f} {cy+math.sin(t)*rr:.1f}'); t+=0.4
    return f'<path d="M{" L".join(pts)}" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>'
def star(x,y,s=1): return f'<path transform="translate({x} {y}) scale({s})" d="M0 -12 L3.5 -4 L12 -3.5 L5.5 2 L7.5 11 L0 6 L-7.5 11 L-5.5 2 L-12 -3.5 L-3.5 -4Z" fill="#f6d36b" stroke="{O}" stroke-width="2.5" stroke-linejoin="round"/>'
def sweat(x,y,s=1): return f'<path transform="translate({x} {y}) scale({s})" d="M0 -14 Q10 2 0 10 Q-10 2 0 -14Z" fill="#9fd0ec" stroke="{O}" stroke-width="2.5"/>'
def qmark(x,y,s=1): return f'<text x="{x}" y="{y}" font-family="{F}" font-weight="900" font-size="{70*s}" fill="{O}" transform="rotate(10 {x} {y})">?</text>'
def zzz(x,y,s=1): return ''.join(f'<text x="{x+i*22*s}" y="{y-i*26*s}" font-family="{F}" font-weight="900" font-size="{(26+i*8)*s}" fill="{O}">Z</text>' for i in range(3))
def bubbles(u,n,x0,x1,y0,y1,seed=1):
    r=random.Random(seed); return ''.join(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(3,10):.1f}" fill="#e8f6f8" fill-opacity=".35" stroke="#f4fbfc" stroke-width="2"/>' for _ in range(n))
def motion(x,y,side=1,n=3,L=26):
    return ''.join(f'<path d="M{x+side*i*8} {y+i*16} q{side*L*0.6} -6 {side*L} 2" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>' for i in range(n))
def cap(x,y,txt):
    w=len(txt)*25+40
    return f'<g><rect x="{x}" y="{y}" width="{w}" height="50" rx="6" fill="#fff8ee" stroke="{O}" stroke-width="3.5"/><text x="{x+20}" y="{y+34}" font-family="{F}" font-weight="900" font-size="25" fill="{O}">{txt}</text></g>'
def panel(bg,fg,idx,u,over=''):
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"><defs>{FILT}{Lg.defs(u)}<clipPath id="c{idx}"><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="6"/></clipPath></defs><g clip-path="url(#c{idx})">{bg}<g filter="url(#hand)">{fg}</g><rect width="{W}" height="{H}" filter="url(#gr{u})" opacity=".5"/>{over}</g><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="6" fill="none" stroke="{O}" stroke-width="6" filter="url(#hand)"/></svg>'
# ---------- 背景の小物 ----------
def tree_round(u,x,y,h,col,trunk='#8b6a4c',s=1):
    r=random.Random(int(x*7+h)); o=pen(u,f'M{x} {y} Q{x+4} {y-h*0.5} {x} {y-h*0.7}',8*s,trunk)
    for k in range(5):
        cx=x+r.uniform(-40,40)*s; cy=y-h*0.75+r.uniform(-30,20)*s; rr=r.uniform(30,46)*s
        o+=wash(u,f'M{cx-rr} {cy} a{rr} {rr*0.85} 0 1 0 {2*rr} 0 a{rr} {rr*0.85} 0 1 0 {-2*rr} 0Z',col,.9)
    o+=pen(u,f'M{x-60*s} {y-h*0.7} Q{x-56*s} {y-h*1.05} {x} {y-h*1.05} Q{x+60*s} {y-h*1.02} {x+60*s} {y-h*0.68}',1.8,op=.6)
    return o
def baobab(u,x,y,s=1):
    t=f'M{x-26*s} {y} Q{x-30*s} {y-120*s} {x-18*s} {y-170*s} L{x+18*s} {y-170*s} Q{x+30*s} {y-120*s} {x+26*s} {y}Z'
    o=wash(u,t,'#b49572')+pen(u,t,2.2)
    for k in range(-3,4):
        o+=pen(u,f'M{x+k*5*s} {y-168*s} q{k*10*s} -20 {k*18*s} -22',3*s,'#7a5e44')
        o+=wash(u,f'M{x+k*18*s-18*s} {y-192*s} a{18*s} {11*s} 0 1 0 {36*s} 0 a{18*s} {11*s} 0 1 0 {-36*s} 0Z','#8fa86e',.9)
    return o
def conifer(u,x,y,h,col='#5f7f62',snow=False):
    o=pen(u,f'M{x} {y} L{x} {y-h*0.2}',6,'#6b5444')
    for k in range(4):
        yy=y-h*0.15-k*h*0.22; w=h*0.32*(1-k*0.2)
        d=f'M{x-w} {yy} L{x} {yy-h*0.35} L{x+w} {yy}Z'; o+=wash(u,d,col)+pen(u,d,1.6,op=.7)
        if snow: o+=pen(u,f'M{x-w*0.7} {yy-4} Q{x} {yy-h*0.2} {x+w*0.7} {yy-4}',4,'#fbfbf7',op=.9)
    return o
def euc(u,x,y,h):
    o=pen(u,f'M{x} {y} Q{x-8} {y-h*0.5} {x+6} {y-h}',7,'#d8cfc0')+pen(u,f'M{x} {y} Q{x-8} {y-h*0.5} {x+6} {y-h}',2,'#8a7a66',op=.7)
    r=random.Random(x)
    for k in range(6):
        cx=x+r.uniform(-50,50); cy=y-h+r.uniform(-20,50); w=r.uniform(30,50)
        o+=wash(u,f'M{cx-w} {cy} Q{cx} {cy-w*0.7} {cx+w} {cy} Q{cx} {cy+w*0.4} {cx-w} {cy}Z','#9fb39a',.85)
    return o
def fern(u,x,y,s=1,col='#6f9a5c'):
    o=''
    for k in range(7):
        a=-math.pi/2+(k-3)*0.38; L=60*s
        ex=x+math.cos(a)*L; ey=y+math.sin(a)*L*0.9
        o+=pen(u,f'M{x} {y} Q{x+math.cos(a)*L*0.5} {y+math.sin(a)*L*0.6-12} {ex:.0f} {ey:.0f}',2.4,col)
        for j in range(1,6):
            t=j/6; px=x+(ex-x)*t; py=y+(ey-y)*t-8*math.sin(t*3.14)
            o+=pen(u,f'M{px:.0f} {py:.0f} l{-7*s:.0f} {-6*s:.0f} M{px:.0f} {py:.0f} l{7*s:.0f} {-6*s:.0f}',1.4,col)
    return o
def cycad(u,x,y,s=1):
    t=f'M{x-12*s} {y} L{x-10*s} {y-50*s} L{x+10*s} {y-50*s} L{x+12*s} {y}Z'
    o=wash(u,t,'#a3825e')+pen(u,t,1.8)
    for k in range(9):
        a=-math.pi/2+(k-4)*0.35; L=70*s
        d=f'M{x} {y-50*s} Q{x+math.cos(a)*L*0.5:.0f} {y-50*s+math.sin(a)*L*0.5-14:.0f} {x+math.cos(a)*L:.0f} {y-50*s+math.sin(a)*L*0.7:.0f}'
        o+=pen(u,d,5*s,'#6f8f4c')+pen(u,d,1.2,op=.6)
    return o
def reeds(u,x,y,n=8,h=70,col='#8a9a5e'):
    r=random.Random(x); o=''
    for i in range(n):
        xx=x+r.uniform(-30,30); hh=h*r.uniform(.6,1.1); l=r.uniform(-12,12)
        o+=pen(u,f'M{xx:.0f} {y} q{l/2:.0f} {-hh/2:.0f} {l:.0f} {-hh:.0f}',2.2,col)
        if r.random()<.5: o+=f'<ellipse cx="{xx+l:.0f}" cy="{y-hh+8:.0f}" rx="3.5" ry="10" fill="#8b6a4c"/>'
    return o
def rock(u,x,y,w,h,col='#a39a8c'):
    d=f'M{x-w} {y} Q{x-w} {y-h} {x-w*0.2} {y-h} Q{x+w*0.6} {y-h*1.05} {x+w} {y-h*0.3} L{x+w} {y}Z'
    return wash(u,d,col)+pen(u,d,2)+pen(u,f'M{x-w*0.4} {y-h*0.75} q{w*0.3} -6 {w*0.6} 0',1.4,op=.5)
def kelp(u,x,y,h,col='#6f8f5c'):
    r=random.Random(x); d=f'M{x} {y}'; yy=y; xx=x
    while yy>y-h: yy-=30; xx+=r.uniform(-14,14); d+=f' Q{xx+r.uniform(-16,16):.0f} {yy+15:.0f} {xx:.0f} {yy:.0f}'
    o=pen(u,d,7,col,op=.85)
    for k in range(int(h/40)):
        o+=wash(u,f'M{x+r.uniform(-10,10):.0f} {y-30-k*40} q16 -10 30 4 q-14 8 -30 -4Z',col,.8)
    return o
def sponge(u,x,y,h,col='#c99b6f'):
    d=f'M{x-12} {y} Q{x-18} {y-h*0.6} {x-14} {y-h} L{x+14} {y-h} Q{x+18} {y-h*0.6} {x+12} {y}Z'
    return wash(u,d,col)+pen(u,d,2)+f'<ellipse cx="{x}" cy="{y-h}" rx="14" ry="4" fill="#7a5e44" opacity=".6"/>'
def floe(u,x,y,w):
    d=f'M{x-w} {y} L{x-w*0.8} {y-14} L{x+w*0.7} {y-16} L{x+w} {y}Z'
    return wash(u,d,'#f4f8fa')+pen(u,d,1.8)+f'<path d="M{x-w} {y} L{x+w} {y} L{x+w*0.9} {y+8} L{x-w*0.9} {y+8}Z" fill="#9fc0cc" opacity=".6"/>'
def volcano(u,x,y,h,col='#8f8378',smoke=True):
    d=f'M{x-h*1.6} {y} L{x-h*0.25} {y-h} L{x+h*0.25} {y-h} L{x+h*1.6} {y}Z'
    o=wash(u,d,col)+pen(u,d.replace('Z',''),1.8,op=.7)
    if smoke:
        for k in range(4): o+=wash(u,f'M{x-30+k*14} {y-h-20-k*30} a{26+k*6} {18+k*4} 0 1 0 {52+k*12} 0 a{26+k*6} {18+k*4} 0 1 0 {-52-k*12} 0Z','#cfc6bd',.7)
    return o
def mountains(u,hz,col,snow=False,seed=1):
    r=random.Random(seed); pts=[(0,hz)]; x=0
    while x<1000: x+=r.uniform(80,160); pts.append((x,hz-r.uniform(60,160)))
    pts.append((1000,hz))
    d='M'+' L'.join(f'{a:.0f} {b:.0f}' for a,b in pts)+'Z'
    o=wash(u,d,col,.9)+pen(u,d.replace('Z',''),1.6,'#5f5a50',op=.6)
    if snow:
        for a,b in pts[1:-1]: o+=f'<path d="M{a-22:.0f} {b+26:.0f} L{a:.0f} {b:.0f} L{a+22:.0f} {b+26:.0f} L{a+8:.0f} {b+18:.0f} L{a-6:.0f} {b+28:.0f}Z" fill="#fbfbf7" opacity=".95"/>'
    return o
def sky(u,c1,c2): return f'<defs><linearGradient id="sk{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#sk{u})"/>'
def ground(u,y,col,seed=1,line=True):
    o=wash(u,band(-20,W,y,H,6,seed),col)
    if line: o+=pen(u,wavy(-20,W+20,y,6,seed),2.4)
    return o
def sea(u,y,y2,col,seed=1):
    r=random.Random(seed); o=wash(u,f'M0 {y} L{W} {y} L{W} {y2} L0 {y2}Z',col,.95)+pen(u,f'M0 {y} L{W} {y}',1.8,'#5f5a50',op=.8)
    for _ in range(26):
        x=r.uniform(0,980); yy=r.uniform(y+6,y2-6); w=r.uniform(12,30)
        o+=pen(u,f'M{x:.0f} {yy:.0f} q{w/4:.0f} -3 {w/2:.0f} 0 q{w/4:.0f} 3 {w/2:.0f} 0',1.1,'#5f7a75',op=.55)
    return o
def underwater(u,top,bot,floor_y,floor_col,seed=1,rays=True):
    o=sky(u,top,bot)
    if rays:
        for i in range(6): x=120+i*160; o+=f'<path d="M{x} 0 L{x+60} 0 L{x+200} {floor_y} L{x+120} {floor_y}Z" fill="#ffffff" opacity=".08"/>'
    o+=ground(u,floor_y,floor_col,seed)
    r=random.Random(seed)
    for _ in range(18): x=r.uniform(0,1000); y=r.uniform(floor_y+20,H); o+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,8):.1f}" ry="{r.uniform(2,4):.1f}" fill="#000" opacity=".12"/>'
    return o
def night(u): return f'<rect width="{W}" height="{H}" fill="#1e2340" opacity=".62"/>'
def dusk(u): return f'<rect width="{W}" height="{H}" fill="#c0603a" opacity=".22"/><rect width="{W}" height="{H}" fill="#3b2a4a" opacity=".16"/>'
def stars_(n=70,seed=3,ymax=330):
    r=random.Random(seed); return ''.join(f'<circle cx="{r.uniform(0,1000):.0f}" cy="{r.uniform(0,ymax):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#f6efd0" opacity="{r.uniform(.5,1):.2f}"/>' for _ in range(n))
# ---------- よみがえりの器(たまご・石・氷) ----------
EGG='M0 -125 C70 -125 104 -20 100 30 C96 95 50 125 0 125 C-50 125 -96 95 -100 30 C-104 -20 -70 -125 0 -125Z'
STONE='M-120 -70 Q-110 -112 -40 -116 Q40 -124 104 -96 Q132 -60 124 20 Q128 92 60 112 Q-20 128 -96 104 Q-136 70 -126 0Z'
ICE='M-110 -110 L96 -118 Q118 -116 116 -92 L120 92 Q118 116 94 116 L-100 120 Q-120 118 -118 94 L-122 -88 Q-124 -110 -110 -110Z'
OBJ={'egg':(EGG,'#fffdf6','#f4ead4','#dccaa4'),'stone':(STONE,'#e6ded0','#cdbfa8','#a99a82'),'ice':(ICE,'#f4fbff','#cfe6f0','#9cc4d6')}
def gdef(u,kind):
    _,a,b,c=OBJ[kind]; return f'<radialGradient id="ob{u}{kind}" cx=".38" cy=".35" r=".8"><stop offset="0" stop-color="{a}"/><stop offset=".7" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></radialGradient>'
def stamp(u,x=0,y=20,r=40,rot=-12):
    st=f'<g transform="rotate({rot} {x} {y})"><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#c4473a" stroke-width="{r/8:.1f}"/><circle cx="{x}" cy="{y}" r="{r*.79:.1f}" fill="none" stroke="#c4473a" stroke-width="{r/20:.1f}"/><text x="{x}" y="{y+r*.32:.1f}" text-anchor="middle" font-family="{F}" font-weight="900" font-size="{r*.74:.1f}" fill="#c4473a">絶滅</text></g>'
    return f'<g filter="url(#ink{u})" opacity=".9">{st}</g>'
def texture(u,kind,name=None):
    r=random.Random(5); o=''
    if kind=='egg':
        for _ in range(14):
            a=r.uniform(0,6.28); d=r.uniform(.2,.9); px=math.cos(a)*90*d; py=math.sin(a)*112*d
            if px*px+(py-20)**2<52**2: continue
            o+=f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{r.uniform(3,8):.1f}" ry="{r.uniform(2,5):.1f}" fill="#b89766" opacity=".75" filter="url(#wc{u})"/>'
    if kind=='stone':
        if name: o+=f'<g opacity=".28">{g(sil(ch(name,view="side")),-6,-40,0.55)}</g>'
        for _ in range(10): o+=f'<path d="M{r.uniform(-100,80):.0f} {r.uniform(-90,90):.0f} q{r.uniform(10,30):.0f} {r.uniform(-4,4):.0f} {r.uniform(20,50):.0f} 0" fill="none" stroke="#8d7f6a" stroke-width="1.6" opacity=".5"/>'
    if kind=='ice':
        if name: o+=f'<g opacity=".22">{g(sil(ch(name)),0,-30,0.62)}</g>'
        o+='<path d="M-90 -96 L-40 -98 M-96 -80 L-70 -82 M70 60 L100 58" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M-60 40 L-20 -10 L10 30" fill="none" stroke="#b6d6e3" stroke-width="2"/>'
    return o
def obj(u,kind,x,y,s=1,rot=0,name=None):
    d=OBJ[kind][0]
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><defs>{gdef(u,kind)}</defs><path d="{d}" fill="url(#ob{u}{kind})"/>{texture(u,kind,name)}{stamp(u)}<path d="{d}" fill="none" stroke="{O}" stroke-width="{5/s:.1f}" filter="url(#pn{u})"/></g>'
ZZ='M-130 10 L-84 -2 L-56 22 L-26 4 L0 28 L26 2 L54 26 L82 0 L130 14'
def obj_crack(u,kind,name=None):
    d=OBJ[kind][0]
    body=f'<path d="{d}" fill="url(#ob{u}{kind})"/>{texture(u,kind,name)}{stamp(u)}<path d="{d}" fill="none" stroke="{O}" stroke-width="3" filter="url(#pn{u})"/>'
    o=f'<g transform="translate(500 280) scale(1.9)"><defs>{gdef(u,kind)}<clipPath id="up{u}"><path d="{ZZ} L130 -200 L-130 -200Z"/></clipPath><clipPath id="dn{u}"><path d="{ZZ} L130 200 L-130 200Z"/></clipPath></defs>'
    o+=f'<g clip-path="url(#up{u})" transform="translate(-4 -7) rotate(-2)">{body}</g><g clip-path="url(#dn{u})" transform="translate(3 5) rotate(1.5)">{body}</g>'
    o+=f'<path d="{ZZ}" fill="none" stroke="{O}" stroke-width="3.5" stroke-linejoin="round" transform="translate(-4 -7) rotate(-2)"/><path d="{ZZ}" fill="none" stroke="{O}" stroke-width="3.5" stroke-linejoin="round" transform="translate(3 5) rotate(1.5)"/></g>'
    frag={'egg':'#f8f0de','stone':'#d8cdb9','ice':'#e6f4fa'}[kind]
    o+=''.join(f'<path transform="translate({x} {y}) rotate({r})" d="M0 0 L18 -6 L12 12Z" fill="{frag}" stroke="{O}" stroke-width="3" stroke-linejoin="round"/>' for x,y,r in [(250,180,20),(760,170,-30),(270,400,60),(740,420,10),(820,300,-12)])
    return o
def obj_open(u,kind,x,y,s=1):
    """割れたあと(下半分)。キャラの前に重ねる"""
    d=OBJ[kind][0]
    low=f'<clipPath id="lo{u}"><path d="{ZZ} L130 200 L-130 200Z"/></clipPath>'
    o=f'<g transform="translate({x} {y}) scale({s})"><defs>{gdef(u,kind)}{low}</defs><g clip-path="url(#lo{u})"><path d="{d}" fill="url(#ob{u}{kind})"/>{texture(u,kind)}<g transform="translate(0 30)">{stamp(u,0,20,34,-6)}</g><path d="{d}" fill="none" stroke="{O}" stroke-width="{5/s:.1f}"/></g><path d="{ZZ}" fill="none" stroke="{O}" stroke-width="{5/s:.1f}" stroke-linejoin="round"/></g>'
    return o
def obj_cap(u,kind,x,y,s=1,rot=-12):
    d=OBJ[kind][0]
    up=f'<clipPath id="ca{u}"><path d="{ZZ} L130 -200 L-130 -200Z"/></clipPath>'
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><defs>{gdef(u,kind)}{up}</defs><g clip-path="url(#ca{u})"><path d="{d}" fill="url(#ob{u}{kind})"/><path d="{d}" fill="none" stroke="{O}" stroke-width="{5/s:.1f}"/></g><path d="{ZZ}" fill="none" stroke="{O}" stroke-width="{5/s:.1f}" stroke-linejoin="round"/></g>'
# ---------- 光が落ちる ----------
def light_fall(x,y,x0=320,y0=40):
    o=burst(x,y,44,40,700).replace(f'fill="{O}" opacity=".18"','fill="#f6e3a0" opacity=".28"')
    o+=f'<path d="M{x0} {y0} Q{(x0+x)/2+60} {(y0+y)/2-20} {x} {y-10}" fill="none" stroke="#fff3c4" stroke-width="10" stroke-linecap="round" opacity=".5"/><path d="M{x0} {y0} Q{(x0+x)/2+60} {(y0+y)/2-20} {x} {y-10}" fill="none" stroke="#fffbe8" stroke-width="3" stroke-linecap="round"/>'
    o+=f'<circle cx="{x}" cy="{y}" r="30" fill="#fff6cf" opacity=".6"/>'+twinkle(x,y,2.4)+twinkle(x-90,y-130,.8)+twinkle(x+80,y-60,.7)
    return o
def cream(): return f'<rect width="{W}" height="{H}" fill="#fff3d6"/>'
def crab(x,y,s=1):
    c=f'<g transform="translate({x} {y}) scale({s})" fill="{SIL}" stroke="{SIL}" stroke-width="4" stroke-linecap="round"><ellipse cx="0" cy="0" rx="26" ry="16"/>'
    for k in (-1,1):
        c+=f'<path d="M{k*20} 8 l{k*14} 14 M{k*14} 12 l{k*10} 16 M{k*24} 2 l{k*16} 10" fill="none"/><path d="M{k*18} -8 q{k*10} -18 {k*24} -14" fill="none"/><ellipse cx="{k*34}" cy="-24" rx="9" ry="7"/>'
        c+=f'<path d="M{k*7} -14 l0 -14" fill="none"/><circle cx="{k*7}" cy="-30" r="5" fill="#f6efdc" stroke="{SIL}" stroke-width="2"/><circle cx="{k*7}" cy="-30" r="2" fill="{SIL}" stroke="none"/>'
    return c+'</g>'
def fish(x,y,s=1,flip=False):
    sx=-s if flip else s
    return f'<g transform="translate({x} {y}) scale({sx} {s})" fill="{SIL}"><path d="M-30 0 Q-10 -18 18 -4 L34 -16 L30 0 L34 16 L18 4 Q-10 18 -30 0Z"/><circle cx="-18" cy="-3" r="3.5" fill="#f6efdc"/><circle cx="-18" cy="-3" r="1.6" fill="{SIL}"/></g>'
def smallbird(x,y,s=1,flip=False):
    sx=-s if flip else s
    return f'<g transform="translate({x} {y}) scale({sx} {s})" fill="{SIL}"><ellipse cx="0" cy="0" rx="20" ry="15"/><circle cx="-16" cy="-12" r="10"/><path d="M-25 -12 L-36 -8 L-25 -6Z"/><path d="M14 -4 L32 -14 L28 4Z"/><path d="M-4 14 L-6 26 M6 14 L6 26" stroke="{SIL}" stroke-width="3"/><circle cx="-19" cy="-14" r="3" fill="#f6efdc"/><circle cx="-19" cy="-14" r="1.4" fill="{SIL}"/></g>'
def gull(x,y,s=1):
    return f'<path transform="translate({x} {y}) scale({s})" d="M-30 0 Q-15 -14 0 -2 Q15 -14 30 0 Q15 -8 0 4 Q-15 -8 -30 0Z" fill="{SIL}"/>'
