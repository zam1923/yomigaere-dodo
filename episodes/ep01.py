import sys,random,math,json,re
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','kit'))
from epkit import *
import envs, turn, logoIntact
from ep1b import eyes_sparkle
TT=lambda k='n': ch('トト',k)
def sailor(x,y,s=1):
    c=SIL
    o=f'<g transform="translate({x} {y}) scale({s})" fill="{c}">'
    o+='<path d="M-66 -560 L66 -560 L74 -330 Q96 -260 118 -196 L-118 -196 Q-96 -260 -74 -330Z"/>'   # 長いコート
    o+='<rect x="-62" y="-210" width="44" height="180"/><rect x="18" y="-210" width="44" height="180"/>'  # 脚
    o+='<path d="M-80 -40 L-10 -40 L-6 0 L-92 0Z"/><path d="M10 -40 L80 -40 L94 0 L6 0Z"/>'  # ブーツ
    o+='<rect x="-74" y="-352" width="148" height="16" fill="#1c1512"/>'  # ベルト
    o+='<path d="M58 -520 Q118 -440 104 -330" fill="none" stroke="'+c+'" stroke-width="34" stroke-linecap="round"/>'  # 腕
    o+='<circle cx="104" cy="-326" r="22"/>'  # こぶし
    o+='<path d="M96 -340 L118 -326 L-188 -12 L-206 -26Z"/>'  # 棒
    return o+'</g>'
def footprint(x,y,s=1,rot=0): return f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0 0 L-9 -14 M0 0 L0 -17 M0 0 L9 -14 M0 0 L0 7" stroke="#8a7357" stroke-width="3.4" stroke-linecap="round" fill="none" opacity=".75"/>'
def feather(u,x,y,s=1,rot=-20):
    d='M0 0 Q30 -60 110 -80 Q70 -20 0 0Z'
    o=f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'+wash(u,d,'#b8c6c0')+pen(u,d,2.2)+pen(u,'M-8 6 Q50 -40 108 -78',2)
    o+=''.join(pen(u,f'M{14+i*12} {-10-i*8} l{6+i} {-14+i}',1.2,op=.6) for i in range(8))
    return o+'</g>'
def barren(u,m='day'):
    o=sky(u,'#cfd3c6','#e8e6da')+sea(u,250,330,'#8fa6a2',61)
    o+=wash(u,band(-20,W,316,H,10,62),'#9b9183')+pen(u,wavy(-20,W+20,316,10,62),2.4)
    r=random.Random(5)
    for _ in range(9):
        x=r.uniform(0,1000); w=r.uniform(40,110); h=w*r.uniform(.4,.8); y=r.uniform(380,560)
        o+=rock(u,x,y,w,h,r.choice(['#8d8478','#a39a8c','#7f776c']))
    for _ in range(25): x=r.uniform(0,1000); y=r.uniform(330,560); o+=pen(u,f'M{x:.0f} {y:.0f} l{r.uniform(10,30):.0f} {r.uniform(-4,4):.0f}',1.3,op=.4)
    return o
def wind(x,y,n=3,L=120):
    return ''.join(f'<path d="M{x} {y+i*26} q{L*0.4} -14 {L*0.8} 0 q{L*0.15} 6 {L*0.2} -8" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round" opacity=".55"/>' for i in range(n))
P=[]
# 1 ロゴ(割れる前のたまご)
logo=logoIntact.B3i('t1').replace('rx="28"','rx="0"',1)
logo=re.sub(r'<rect x="12" y="12"[^>]*/><rect x="20" y="20"[^>]*/>','',logo)
logo=logo.replace('<svg viewBox="0 0 900 440" width="900" height="440"','<svg viewBox="0 0 900 440" x="0" y="0" width="1000" height="560" preserveAspectRatio="xMidYMid slice"',1)
P.append(f'<svg viewBox="0 0 1000 560" width="1000" height="560" xmlns="http://www.w3.org/2000/svg"><defs>{FILT}<clipPath id="cT"><rect x="4" y="4" width="992" height="552" rx="6"/></clipPath></defs><g clip-path="url(#cT)">{logo}</g><rect x="4" y="4" width="992" height="552" rx="6" fill="none" stroke="{O}" stroke-width="6" filter="url(#hand)"/></svg>')
# 2 1662年、夕暮れの浜にトトが1羽
u='p2'; bg=envs.island(u)+dusk(u)+f'<circle cx="160" cy="250" r="40" fill="#f6d38a" opacity=".85"/>'+ship(u,760,256,1.0)
fg=g(turn.three(),470,410,0.75,0,True)+''.join(footprint(x,y,.8,90) for x,y in [(300,470),(350,478),(400,470)])+cap(24,24,'1662年　モーリシャス島')
P.append(panel(bg,fg,2,u))
# 3 棒を持った人間の影。トトはキラキラ目で近づく
u='p3'; bg=envs.island(u)+dusk(u)+f'<rect width="{W}" height="{H}" fill="#3b2a3a" opacity=".18"/>'
fg=sailor(800,520,1.0)+g(TT('spark'),330,360,1.35)+twinkle(200,230,1)+twinkle(470,200,.8)+''.join(footprint(x,500,.8,90) for x in (120,170,220))
fg+=f'<path d="M460 330 q30 -8 50 4 M462 360 q30 0 50 10" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>'
P.append(panel(bg,fg,3,u))
# 4 だれもいない浜。足あとが途切れ、羽根が1枚
u='p4'; bg=envs.island(u)+dusk(u)+f'<rect width="{W}" height="{H}" fill="#2e2440" opacity=".25"/>'+ship(u,560,252,1.2)
fg=''.join(footprint(x,y,.9,90) for x,y in [(120,460),(180,470),(240,460),(300,470),(360,460),(420,470)])+''.join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="11" transform="rotate(-8 {x} {y})" fill="#6f5a46" opacity=".45"/>' for x,y in [(960,500),(880,470),(800,505),(720,476),(640,500),(560,474),(500,500)])+feather(u,620,420,.9,-10)
P.append(panel(bg,fg,4,u))
# 5 暗いコマ。人間の手の影が、ページに「絶滅」のハンコを押す
u='p5'; bg=f'<rect width="{W}" height="{H}" fill="#241e1b"/><radialGradient id="lp{u}" cx=".45" cy=".6" r=".55"><stop offset="0" stop-color="#e9d9b0" stop-opacity=".55"/><stop offset="1" stop-color="#241e1b" stop-opacity="0"/></radialGradient><rect width="{W}" height="{H}" fill="url(#lp{u})"/>'
page='M180 300 L700 270 L760 520 L200 560Z'
fg=wash(u,page,'#efe2c3')+pen(u,page,2)
fg+=''.join(pen(u,f'M{230+i*4} {330+i*24} L{520+i*4} {316+i*24}',1.4,INK,op=.5) for i in range(6))
fg+=f'<g transform="translate(330 440) rotate(-6) scale(.62)" opacity=".55">{sil(turn.side())}</g>'
fg+=f'<g filter="url(#ink{u})" opacity=".92"><g transform="rotate(-10 600 440)"><circle cx="600" cy="440" r="52" fill="none" stroke="#c4473a" stroke-width="7"/><circle cx="600" cy="440" r="41" fill="none" stroke="#c4473a" stroke-width="2.6"/><text x="600" y="457" text-anchor="middle" font-family="{F}" font-weight="900" font-size="40" fill="#c4473a">絶滅</text></g></g>'
fg+='<path d="M560 0 L760 0 L730 150 L600 170Z" fill="#0e0b0a"/>'  # 袖
fg+='<path d="M590 160 Q600 120 650 118 Q720 116 742 150 Q760 196 730 226 Q690 250 640 240 Q596 228 590 190Z" fill="#0e0b0a"/>'  # こぶし
fg+=''.join(f'<path d="M{x} 150 q10 30 0 64" fill="none" stroke="#2a221d" stroke-width="3"/>' for x in (630,660,690,715))
fg+='<rect x="638" y="228" width="44" height="66" rx="8" fill="#3a2e27"/><rect x="600" y="290" width="120" height="26" rx="6" fill="#3a2e27"/><rect x="606" y="314" width="108" height="8" fill="#c4473a"/>'  # ハンコ
fg+=''.join(f'<path d="M{x} 340 l{d} 14" stroke="#e9d9b0" stroke-width="3" stroke-linecap="round" opacity=".7"/>' for x,d in [(616,-6),(660,0),(704,6)])
P.append(panel(bg,fg,5,u))
# 6 真っ黒。光がひとつ落ちてくる
u='p6'; bg=f'<rect width="{W}" height="{H}" fill="#0c0b10"/>'
fg=f'<path d="M500 -10 L500 380" stroke="#fff3c4" stroke-width="12" stroke-linecap="round" opacity=".35"/><path d="M500 -10 L500 380" stroke="#fffbe8" stroke-width="3.5" stroke-linecap="round"/><circle cx="500" cy="390" r="26" fill="#fff6cf" opacity=".5"/>'+twinkle(500,390,2.2)
P.append(panel(bg,fg,6,u))
# 7 約5億年前。草も木もない岩の浜に、ハンコつきのたまご
u='p7'; bg=barren(u)
fg=obj(u,'egg',560,380,0.85,6)+f'<ellipse cx="560" cy="486" rx="90" ry="12" fill="#4a3f36" opacity=".35"/>'+cap(24,24,'約5億年前')+wind(120,140,3,140)
P.append(panel(bg,fg,7,u))
# 8 アップ。ヒビが「絶滅」をまっぷたつに
u='p8'; P.append(panel(cream(),burst(500,280,52,250,700)+obj_crack(u,'egg'),8,u))
# 9 殻をのせたトトが、ぽかんと顔を出す
u='p9'; bg=barren(u)
fg=g(TT('blank'),500,300,1.45)+obj_open(u,'egg',500,400,1.05)+obj_cap(u,'egg',500,300-110*1.45+30,0.5,-12)
fg+=f'<g stroke="{O}" stroke-width="3" stroke-linecap="round" fill="none"><path d="M450 120 l-8 -18"/><path d="M500 106 l0 -20"/><path d="M550 120 l8 -18"/></g>'
P.append(panel(bg,fg,9,u))
# 10 大きく引いた絵。どこまでも岩と風だけ、トトは豆粒
u='p10'; bg=barren(u)
fg=f'<ellipse cx="520" cy="468" rx="26" ry="6" fill="#4a3f36" opacity=".35"/>'+g(turn.front(),520,430,0.34)+wind(140,120,3,180)+wind(640,200,2,160)+f'<path d="M505 395 q-4 -10 6 -14" fill="none" stroke="{O}" stroke-width="2"/>'
P.append(panel(bg,fg,10,u))
# 11 潮だまりをのぞく。見たことのない形の影たち。キラキラ目
u='p11'; bg=barren(u)
pool='M380 380 Q600 330 900 370 Q960 450 860 520 Q620 560 420 520 Q330 460 380 380Z'
fg=wash(u,pool,'#7fa6a6')+pen(u,pool,3)
fg+=f'<clipPath id="pl{u}"><path d="{pool}"/></clipPath><g clip-path="url(#pl{u})" opacity=".85">'+g(sil(ch('ハルル')),520,470,.6)+g(sil(ch('オパ')),760,440,.55,0,True)+''.join(f'<path transform="translate({x} {y}) scale(.8)" d="M0 -20 Q22 -18 24 0 Q22 22 0 26 Q-22 22 -24 0 Q-22 -18 0 -20Z" fill="{SIL}"/>' for x,y in [(640,500),(800,480),(460,420)])+'</g>'
fg+=g(TT('spark'),230,320,1.5,14)+twinkle(400,180,1)+twinkle(120,160,.8)
P.append(panel(bg,fg,11,u))
# 12 そのまま水に飛びこんで、しずむ。泡の向こうに大きな2つの目
u='p12'; bg=sky(u,'#3f6f74','#16303a')
maro=sil(ch('マロ'))
fg=f'<g opacity=".9">{g(maro,720,250,2.3)}</g>'
for ex,ey in [(624,135),(816,135)]: fg+=f'<circle cx="{ex}" cy="{ey}" r="15" fill="#f6efd0"/><circle cx="{ex-3}" cy="{ey+2}" r="7" fill="#16303a"/>'
fg+=g(TT('blank'),280,380,1.1,25)+bubbles(u,22,180,420,40,330,21)+sweat(370,290,1.2)
P.append(panel(bg,fg,12,u))
json.dump(P,open('ep01_panels.json','w'),ensure_ascii=False)

if __name__=='__main__':
    import asyncio, sheets, os
    os.makedirs('out',exist_ok=True)
    print(asyncio.run(sheets.render('第1話_よみがえれドードー',P,'第1話\u3000よみがえれ、ドードー','ドードーは、インド洋のモーリシャス島にだけすんでいた飛べない鳥。近づいてくるものを、ほとんどこわがらなかったと言われている。',False)))
