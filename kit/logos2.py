import sys,random,math,io,contextlib,json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from ep1b import toto_face, O
F="'Zen Maru Gothic',sans-serif"
INK='#6b5444'
def defs(u):
    return f'''<filter id="wc{u}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="7" result="d"/><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="11" result="n2"/><feColorMatrix in="n2" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.1 0.25" result="m"/><feComposite in="d" in2="m" operator="in"/></filter>
<filter id="pn{u}" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"/></filter>
<filter id="tr{u}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.25" numOctaves="2" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
<filter id="gr{u}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.27  0 0 0 0 0.2  0.35 0 0 0 -0.12"/></filter>
<filter id="ink{u}"><feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="2" seed="9" result="n"/><feColorMatrix in="n" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.6 1.75" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feTurbulence type="fractalNoise" baseFrequency="0.05" seed="4" result="n3"/><feDisplacementMap in="c" in2="n3" scale="3"/></filter>
<filter id="bl{u}"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="hd{u}"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="1" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>'''
def wash(u,d,c,op=1): return f'<path d="{d}" fill="{c}" opacity="{op}" filter="url(#wc{u})"/>'
def pen(u,d,w=2.6,c=INK,fill='none',op=.9): return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}" filter="url(#pn{u})"/>'
def g(svg,x,y,s=1,rot=0): return f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate(-100 -110)">{svg}</g>'
def T(x,y,txt,size,fill,sw,ls=0,rot=0,anchor='middle'):
    return f'<text x="{x}" y="{y}" transform="rotate({rot} {x} {y})" text-anchor="{anchor}" font-family="{F}" font-weight="900" font-size="{size}" fill="{fill}" stroke="{O}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke" letter-spacing="{ls}">{txt}</text>'
def tw(x,y,s=1): return f'<path transform="translate({x} {y}) scale({s})" d="M0 -14 Q2 -2 14 0 Q2 2 0 14 Q-2 2 -14 0 Q-2 -2 0 -14Z" fill="#fff8ee" stroke="{O}" stroke-width="2.5" stroke-linejoin="round"/>'
def wavy(x0,x1,y,amp,seed,step=40):
    r=random.Random(seed); pts=[]
    x=x0
    while x<=x1+step: pts.append((x,y+r.uniform(-amp,amp))); x+=step
    d=f'M{pts[0][0]} {pts[0][1]:.1f}'
    for i in range(1,len(pts)):
        mx=(pts[i-1][0]+pts[i][0])/2; my=(pts[i-1][1]+pts[i][1])/2
        d+=f' Q{pts[i-1][0]} {pts[i-1][1]:.1f} {mx:.1f} {my:.1f}'
    return d
def band(x0,x1,ytop,ybot,amp,seed): return wavy(x0,x1,ytop,amp,seed)+f' L{x1+40} {ybot} L{x0} {ybot}Z'
def grass(u,x,y,n,h,seed,col='#7d9b5e'):
    r=random.Random(seed); s=''
    for i in range(n):
        xx=x+r.uniform(-14,14); hh=h*r.uniform(.6,1.1); lean=r.uniform(-10,10)
        s+=f'M{xx:.1f} {y} q{lean/2:.1f} {-hh/2:.1f} {lean:.1f} {-hh:.1f} '
    return f'<path d="{s}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" filter="url(#pn{u})"/>'
def wrap(u,inner,bg,top):
    return f'<svg viewBox="0 0 900 440" width="900" height="440" xmlns="http://www.w3.org/2000/svg"><defs>{defs(u)}<clipPath id="cl{u}"><rect width="900" height="440" rx="28"/></clipPath></defs><g clip-path="url(#cl{u})"><rect width="900" height="440" fill="{bg}"/>{inner}<rect width="900" height="440" filter="url(#gr{u})" opacity=".55"/>{top}</g></svg>'

# ================= A =================
def A(u):
    r=random.Random(5); s=''
    s+=f'<defs><linearGradient id="skA{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f0e6"/><stop offset="1" stop-color="#f7f1e1"/></linearGradient></defs><rect width="900" height="440" fill="url(#skA{u})"/>'
    # 遠景の木々(にじみ)
    for x,hh,c in [(70,150,'#cfe0c4'),(160,110,'#d9e7cf'),(640,130,'#d4e4ca'),(860,170,'#c9dcbd')]:
        s+=wash(u,f'M{x-50} 300 Q{x-60} {300-hh} {x} {300-hh-20} Q{x+60} {300-hh} {x+50} 300Z',c,.9)
        s+=pen(u,f'M{x} 300 L{x} {300-hh*0.45}',2,'#a8987c',op=.5)
    # 地層
    s+=wash(u,band(-20,900,296,440,8,1),'#dcc8a0')
    s+=wash(u,band(-20,900,350,440,7,2),'#cfb68b')
    s+=wash(u,band(-20,900,404,440,5,3),'#bfa274')
    s+=pen(u,wavy(-20,920,296,8,1),3)+pen(u,wavy(-20,920,350,7,2),1.8,op=.5)+pen(u,wavy(-20,920,404,5,3),1.8,op=.5)
    # 地層の細かい線と小石
    for _ in range(26):
        x=r.uniform(10,890); y=r.uniform(312,432); w=r.uniform(14,40)
        s+=pen(u,f'M{x:.0f} {y:.0f} q{w/2:.0f} {r.uniform(-3,3):.1f} {w:.0f} 0',1.4,op=.35)
    for _ in range(22):
        x=r.uniform(10,890); y=r.uniform(316,434); a=r.uniform(4,9); b=a*r.uniform(.5,.8)
        s+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{a:.1f}" ry="{b:.1f}" fill="#a98d63" opacity=".8" filter="url(#wc{u})"/><ellipse cx="{x-a*.3:.0f}" cy="{y-b*.3:.0f}" rx="{a*.35:.1f}" ry="{b*.3:.1f}" fill="#efe2c6" opacity=".7"/>'
    # 化石(ドードーの骨)
    bone='#f4ecd9'; sh='#d9c9a6'
    fs=''
    fs+=wash(u,'M152 352 Q124 344 108 356 Q96 368 100 386 Q106 396 112 386 Q116 378 128 380 Q140 388 154 388Z',bone)  # くちばし
    fs+=pen(u,'M152 352 Q124 344 108 356 Q96 368 100 386 Q106 396 112 386 Q116 378 128 380 Q140 388 154 388',2.4)
    fs+=f'<ellipse cx="172" cy="370" rx="26" ry="22" fill="{bone}" filter="url(#wc{u})"/>'+pen(u,'M150 360 Q160 346 178 348 Q200 352 198 372 Q194 392 168 392 Q154 390 152 384',2.4)
    fs+=f'<ellipse cx="176" cy="366" rx="8" ry="7" fill="#8f7754" opacity=".8" filter="url(#wc{u})"/>'+pen(u,'M118 372 L146 374',1.4,op=.6)
    # 首の骨
    for i in range(6):
        t=i/5; x=200+t*46; y=366-t*24
        fs+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7.5" ry="6" transform="rotate(-30 {x:.0f} {y:.0f})" fill="{bone}" filter="url(#wc{u})"/>'+pen(u,f'M{x-7:.0f} {y:.0f} a7 6 -30 1 0 14 0 a7 6 -30 1 0 -14 0',1.8)
    # 背骨と肋骨
    fs+=pen(u,'M248 340 Q300 326 352 334 Q380 338 398 350',3.2)
    for i in range(6):
        x=262+i*18; y=334-math.sin(i/5*math.pi)*4
        fs+=pen(u,f'M{x} {y:.0f} q{6+i} 26 {-4+i*1.5:.0f} {46-abs(i-2.5)*3:.0f}',2.6)
    fs+=f'<ellipse cx="380" cy="350" rx="24" ry="14" transform="rotate(14 380 350)" fill="{bone}" filter="url(#wc{u})"/>'+pen(u,'M356 346 Q372 332 398 342 Q410 352 400 362 Q380 368 360 358Z',2.2)
    # 脚
    fs+=pen(u,'M372 360 L356 392 L366 420',3)+pen(u,'M366 420 l-14 6 M366 420 l4 10 M366 420 l14 4',2.2)
    fs+=pen(u,'M392 362 L402 394 L392 422',3)+pen(u,'M392 422 l-12 8 M392 422 l6 10 M392 422 l14 2',2.2)
    # 尾羽の骨
    fs+=pen(u,'M400 348 l18 -12 M402 352 l22 -4 M400 356 l18 8',2)
    s+=f'<g transform="translate(-40 6)">{fs}</g>'
    # ラベル(小さな札)
    s+=f'<g transform="rotate(-4 470 410)"><rect x="420" y="396" width="104" height="30" rx="4" fill="#fbf5e6" filter="url(#wc{u})"/>'+pen(u,'M420 396 h104 v30 h-104Z',1.6)+f'<text x="472" y="417" text-anchor="middle" font-family="{F}" font-weight="700" font-size="14" fill="{INK}">DODO 17C.</text></g>'
    # 地表の草
    for x,sd in [(30,1),(240,2),(560,3),(620,4),(880,5)]: s+=grass(u,x,298,7,18,sd)
    # トトが地面から(土の盛り上がり)
    s+=g(toto_face('spark'),760,256,0.72,8)
    s+=wash(u,'M660 312 Q700 286 760 288 Q820 286 862 310 L870 330 L650 330Z','#cfb68b')
    s+=pen(u,'M652 314 Q700 284 760 286 Q820 284 868 312',3)
    for x,y,a in [(668,272,8),(860,262,7),(694,240,5),(846,228,6),(822,196,4),(704,206,3.5)]:
        s+=f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{a*.8:.1f}" fill="#b99d72" filter="url(#wc{u})"/>'+pen(u,f'M{x-a} {y} a{a} {a*.8:.1f} 0 1 0 {2*a} 0 a{a} {a*.8:.1f} 0 1 0 {-2*a} 0',1.6,op=.7)
    s+=pen(u,'M700 186 l-12 -14 M836 176 l12 -14 M770 160 l0 -16',3)
    top=T(60,116,'よみがえれ、',52,'#e6dfcf',10,6,0,'start')
    for c,x,y,rt in [('ド',110,272,0),('ー',230,262,-3),('ド',350,246,-6),('ー',474,222,-12)]: top+=T(x,y,c,118,'#a9bdb6',14,0,rt)
    top+=tw(420,60,.9)+tw(560,110,.7)+tw(880,110,.7)
    return wrap(u,s,'#eef3e6',top)

# ================= B =================
def B(u):
    r=random.Random(8); s=''
    s+=f'<defs><radialGradient id="lgB{u}" cx=".75" cy=".45" r=".7"><stop offset="0" stop-color="#fff8e4"/><stop offset="1" stop-color="#f6e6c2"/></radialGradient><radialGradient id="egB{u}" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#fffdf6"/><stop offset=".7" stop-color="#f4ead4"/><stop offset="1" stop-color="#dccaa4"/></radialGradient></defs><rect width="900" height="440" fill="url(#lgB{u})"/>'
    # 光
    for i in range(14):
        a=-math.pi/2+(i-6.5)*0.2
        s+=f'<path d="M700 230 L{700+math.cos(a-0.04)*600:.0f} {230+math.sin(a-0.04)*600:.0f} L{700+math.cos(a+0.04)*600:.0f} {230+math.sin(a+0.04)*600:.0f}Z" fill="#fff6d8" opacity=".55"/>'
    # 草地
    s+=wash(u,band(-20,900,372,440,6,4),'#c3d9a6')+pen(u,wavy(-20,920,372,6,4),2.6)
    for x in range(10,900,46): s+=grass(u,x,376,6,22,x)
    for x,y,c in [(80,400,'#f3c3c0'),(250,416,'#fbf0b8'),(860,404,'#f3c3c0'),(520,420,'#fbf0b8')]:
        s+=''.join(f'<circle cx="{x+math.cos(k*1.256)*5:.1f}" cy="{y+math.sin(k*1.256)*5:.1f}" r="4" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for k in range(5))+f'<circle cx="{x}" cy="{y}" r="2.6" fill="#e8b84f"/>'
    # 巣(小枝)
    nest=''
    for i in range(70):
        cx=700+r.uniform(-130,130); cy=372+r.uniform(-12,14); L=r.uniform(40,90); a=r.uniform(-0.35,0.35)
        x1=cx-math.cos(a)*L/2; y1=cy-math.sin(a)*L/2; x2=cx+math.cos(a)*L/2; y2=cy+math.sin(a)*L/2
        col=r.choice(['#9b7a52','#b08d62','#86684a','#c2a074'])
        nest+=f'<path d="M{x1:.0f} {y1:.0f} Q{cx:.0f} {cy+r.uniform(-8,8):.0f} {x2:.0f} {y2:.0f}" stroke="{col}" stroke-width="{r.uniform(2,4):.1f}" fill="none" stroke-linecap="round"/>'
    back_nest=wash(u,'M570 362 Q700 330 830 362 Q840 392 700 398 Q560 392 570 362Z','#a8865c')
    s+=f'<ellipse cx="700" cy="390" rx="150" ry="18" fill="#6b5444" opacity=".35" filter="url(#bl{u})"/>'+back_nest
    # トト + たまご
    zig='M604 232 L628 214 L646 236 L668 206 L690 234 L712 204 L734 232 L756 210 L782 236 L798 220'
    eggd=f'{zig} Q808 300 748 352 Q704 374 658 352 Q596 300 604 232Z'
    s+=g(toto_face('spark'),700,196,0.95)
    s+=f'<path d="{eggd}" fill="url(#egB{u})"/>'
    s+=f'<path d="M608 236 L628 220 L646 242 L668 212 L690 240 L712 210 L734 238 L756 216 L782 242 L796 228" fill="none" stroke="#fffdf6" stroke-width="5" stroke-linejoin="round"/>'
    for _ in range(16):
        x=r.uniform(620,790); y=r.uniform(250,345); a=r.uniform(2,7)
        s+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{a:.1f}" ry="{a*r.uniform(.5,.9):.1f}" fill="#b89766" opacity=".75" filter="url(#wc{u})"/>'
    s+=f'<path d="{eggd}" fill="none" stroke="{O}" stroke-width="4" stroke-linejoin="round" filter="url(#pn{u})"/>'
    s+=pen(u,'M760 300 Q770 324 752 344',2,'#fffdf6',op=.8)
    s+=f'<g>{nest}</g>'
    # 頭の殻
    cap='M640 112 Q648 54 694 50 Q742 54 748 112 L726 98 L706 116 L684 96 L662 116Z'
    s+=f'<g transform="rotate(-14 690 104)"><path d="{cap}" fill="url(#egB{u})"/><ellipse cx="676" cy="80" rx="6" ry="4" fill="#b89766" filter="url(#wc{u})"/><ellipse cx="714" cy="70" rx="4.5" ry="3.5" fill="#b89766" filter="url(#wc{u})"/><path d="{cap}" fill="none" stroke="{O}" stroke-width="4" stroke-linejoin="round" filter="url(#pn{u})"/></g>'
    for x,y,rt in [(560,170,20),(842,190,-30),(572,330,60),(852,300,10)]:
        s+=f'<path transform="translate({x} {y}) rotate({rt})" d="M0 0 L16 -6 L12 10Z" fill="#f8f0de" stroke="{O}" stroke-width="2.6" stroke-linejoin="round" filter="url(#pn{u})"/>'
    s+=pen(u,'M612 56 l-14 -12 M600 84 l-20 -2 M790 44 l12 -14',3.2)
    top=T(290,150,'よみがえれ、',58,'#fff8ee',11,6)+T(300,278,'ドードー',124,'#a9bdb6',14,4)+tw(70,100,.9)+tw(540,90,.8)
    return wrap(u,s,'#fff3d6',top)

# ================= C =================
def C(u):
    r=random.Random(12); s=''
    s+=f'''<defs><linearGradient id="pgL{u}" x1="0" x2="1"><stop offset="0" stop-color="#efe0bd"/><stop offset=".85" stop-color="#f3e7c9"/><stop offset="1" stop-color="#cdb88e"/></linearGradient>
<linearGradient id="pgR{u}" x1="0" x2="1"><stop offset="0" stop-color="#c9b388"/><stop offset=".15" stop-color="#f4e9cd"/><stop offset="1" stop-color="#ecdcb6"/></linearGradient>
<radialGradient id="hole{u}" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#7a634f"/><stop offset="1" stop-color="#3a2d24"/></radialGradient></defs>'''
    # 机(木目)
    s+=f'<rect width="900" height="440" fill="#c9a37a"/>'
    for i in range(16):
        y=8+i*28+r.uniform(-4,4)
        s+=pen(u,wavy(-20,920,y,5,100+i,60),1.6,'#a7825b',op=.6)
    s+=f'<rect width="900" height="440" fill="#e7d2b2" opacity=".25"/>'
    # 本(影・厚み)
    bx,by=110,128
    s+=f'<ellipse cx="450" cy="420" rx="370" ry="24" fill="#4a3628" opacity=".4" filter="url(#bl{u})"/>'
    s+=f'<path d="M100 150 Q275 126 450 152 Q625 126 800 150 L806 410 Q628 392 450 414 Q272 392 94 410Z" fill="#7d5a3e"/>'
    for k in range(4):
        s+=pen(u,f'M{100+k} {404-k*4} Q275 {386-k*4} 450 {408-k*4} Q625 {386-k*4} {800-k} {404-k*4}',1.2,'#d8c49c',op=.9)
    L='M110 142 Q280 118 450 146 L450 396 Q280 372 112 392Z'
    R='M450 146 Q620 118 790 142 L788 392 Q620 372 450 396Z'
    s+=f'<path d="{L}" fill="url(#pgL{u})"/><path d="{R}" fill="url(#pgR{u})"/>'
    # しみ(foxing)
    for _ in range(14):
        x=r.uniform(130,770); y=r.uniform(160,380); a=r.uniform(3,10)
        s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{a:.1f}" fill="#d8bf8c" opacity=".45" filter="url(#wc{u})"/>'
    s+=pen(u,L,2.6)+pen(u,R,2.6)
    # 左ページ: 見出し・手書き文・銅版画風ドードー
    s+=f'<text x="140" y="172" font-family="{F}" font-weight="900" font-size="18" fill="{INK}">No.001</text><text x="210" y="172" font-family="{F}" font-weight="700" font-size="16" fill="{INK}">ドードー</text>'
    s+=pen(u,'M140 180 L300 178',1.4,op=.6)
    def script(x,y,w,seed):
        rr=random.Random(seed); d=f'M{x} {y}'; xx=x
        while xx<x+w:
            st=rr.uniform(5,9); d+=f' q{st/2:.1f} {rr.uniform(-6,-2):.1f} {st:.1f} {rr.uniform(-1,1):.1f}'; xx+=st
            if rr.random()<.12: xx+=8; d+=f' m8 0'
        return pen(u,d,1.3,INK,op=.55)
    for i,(y,w) in enumerate([(300,250),(318,270),(336,230),(354,260),(372,150)]): s+=script(140,y,w,i)
    # 銅版画風のドードー(横向き、細線+ハッチング)
    dd='M168 270 Q150 250 168 226 Q186 210 214 214 Q224 196 240 196 Q258 196 262 210 Q286 206 292 222 Q290 232 272 228 Q266 246 270 262 Q262 282 230 286 Q190 288 168 270Z'
    s+=f'<clipPath id="dd{u}"><path d="{dd}"/></clipPath><path d="{dd}" fill="#eadbb5"/>'
    hat=''.join(f'<path d="M{150+i*7} 290 L{190+i*7} 190" stroke="{INK}" stroke-width=".9" opacity=".45"/>' for i in range(22))
    s+=f'<g clip-path="url(#dd{u})">{hat}</g>'+pen(u,dd,1.8)
    s+=pen(u,'M264 212 Q292 212 302 228',1.4)+f'<circle cx="250" cy="208" r="2.4" fill="{INK}"/>'
    s+=pen(u,'M206 284 L202 296 M232 286 L236 298 M168 232 q-12 -6 -18 2 M164 244 q-14 0 -16 8',1.4)
    s+=f'<text x="230" y="140" font-family="{F}" font-size="1" fill="none"> </text>'
    # 絶滅ハンコ(インクのかすれ)
    stamp=f'<g transform="rotate(-14 372 240)"><circle cx="372" cy="240" r="40" fill="none" stroke="#c4473a" stroke-width="5"/><circle cx="372" cy="240" r="32" fill="none" stroke="#c4473a" stroke-width="2"/><text x="372" y="253" text-anchor="middle" font-family="{F}" font-weight="900" font-size="30" fill="#c4473a">絶滅</text></g>'
    s+=f'<g filter="url(#ink{u})" opacity=".9">{stamp}</g>'
    # 右ページの破れ穴
    hole='M540 178 L566 160 L580 182 L610 156 L626 186 L664 164 L674 194 L712 180 L710 218 L744 238 L714 262 L734 298 L696 302 L702 340 L664 328 L644 364 L620 332 L580 348 L580 310 L540 310 L558 276 L522 254 L554 234 L526 208Z'
    s+=f'<path d="{hole}" fill="url(#hole{u})"/><clipPath id="hc{u}"><path d="{hole}"/></clipPath>'
    s+=f'<g clip-path="url(#hc{u})">{g(toto_face("spark"),628,266,1.05)}</g>'
    # 破れ縁の白い繊維
    s+=f'<path d="{hole}" fill="none" stroke="#fffaf0" stroke-width="7" stroke-linejoin="round" filter="url(#tr{u})"/>'+pen(u,hole,2.2)
    # めくれた紙片(裏側は陰)
    for d in ['M566 160 L580 182 L590 142Z','M664 164 L674 194 L700 150Z','M744 238 L714 262 L766 274Z','M644 364 L620 332 L612 382Z','M522 254 L554 234 L506 222Z','M702 340 L664 328 L690 370Z']:
        s+=f'<path d="{d}" fill="#e9d9b4" filter="url(#tr{u})"/>'+pen(u,d,1.8)
    for x,y,rt in [(780,120,20),(500,120,-30),(792,320,40),(480,340,10),(840,220,-10)]:
        s+=f'<path transform="translate({x} {y}) rotate({rt})" d="M0 0 L18 -4 L10 12Z" fill="#f4e9cd" filter="url(#tr{u})"/>'+f'<path transform="translate({x} {y}) rotate({rt})" d="M0 0 L18 -4 L10 12Z" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
    s+=pen(u,'M508 152 l-12 -16 M770 136 l12 -14 M800 260 l20 -4',3)
    top=T(46,86,'よみがえれ、',46,'#fff8ee',10,4,0,'start')+T(330,98,'ドードー',96,'#a9bdb6',13,2,0,'start')+tw(860,60,.9)+tw(300,34,.7)
    return wrap(u,s,'#e7efe0',top)
L={k:(f(k),f(k+'s')) for k,f in [('A',A),('B',B),('C',C)]}
json.dump(L,open('logos2.json','w'),ensure_ascii=False)
open('/tmp/logos2.html','w').write('<html><head><link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap" rel="stylesheet"></head><body style="margin:0;background:#ccc;display:flex;flex-direction:column;gap:10px;width:900px">'+''.join(v[0] for v in L.values())+'</body></html>')
