import sys,random,math,json
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','kit'))
from epkit import *
import turn
from ep1b import maro as MARO
TT=lambda k='n': ch('トト',k)
def trilo(x,y,s=1,col='#8a7a66'):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -22 Q24 -20 26 0 Q24 24 0 28 Q-24 24 -26 0 Q-24 -20 0 -22Z" fill="{col}" stroke="{O}" stroke-width="3"/><path d="M-20 -4 L20 -4 M-22 6 L22 6 M-18 16 L18 16 M0 -22 L0 28" stroke="{O}" stroke-width="2" opacity=".6"/><circle cx="-8" cy="-12" r="3" fill="{O}"/><circle cx="8" cy="-12" r="3" fill="{O}"/></g>'
def uw(u): return underwater(u,'#5f9c9a','#2f5f66',470,'#8c8a6a',71)
def puff(): return '<ellipse cx="48" cy="116" rx="22" ry="20" fill="#f6a39a" stroke="#5b4636" stroke-width="4"/><ellipse cx="152" cy="116" rx="22" ry="20" fill="#f6a39a" stroke="#5b4636" stroke-width="4"/>'
def shore(u):
    o=sky(u,'#cfd3c6','#e8e6da')+sea(u,230,560,'#8fa6a2',72)
    o+=wash(u,'M0 330 Q200 300 460 330 L520 560 L0 560Z','#9b9183')+pen(u,'M0 330 Q200 300 460 330 L520 560',2.6)
    return o
P=[]
# 1 水の中。ほっぺをふくらませて息を止めるトト。暗がりから目が近づく
u='q1'; fg=g(TT('shut')+puff(),330,300,1.4,10)+bubbles(u,10,280,420,40,200,3)+f'<g opacity=".85">{g(sil(ch("マロ")),820,330,1.6)}</g>'
fg+=''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="#f6efd0"/><circle cx="{x-3}" cy="{y+2}" r="5" fill="#16303a"/>' for x,y in [(753,250),(887,250)])+sweat(450,190,1.3)
P.append(panel(uw(u),fg,1,u))
# 2 マロ、目の前に。トトはキラキラ目(息は止めたまま)
u='q2'; fg=g(MARO('n','down',False),680,300,1.8)+g(TT('spark')+puff(),270,310,1.55,-8)+twinkle(140,180,.9)+bubbles(u,8,150,300,40,200,5)
P.append(panel(uw(u),fg,2,u))
# 3 マロがトトをつかんで、ぽいっと水の外へ
u='q3'; bg=sky(u,'#cfd3c6','#e8e6da')+sea(u,330,560,'#8fa6a2',73)
fg=g(TT('dizzy'),520,170,1.1,160)+f'<path d="M380 360 Q420 220 500 200" fill="none" stroke="{O}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>'
fg+=''.join(f'<path d="M{x} 336 q{d*10} -40 {d*30} -50" fill="none" stroke="#e8f2f4" stroke-width="6" stroke-linecap="round"/>' for x,d in [(360,-1),(390,-1),(420,1),(440,1)])+bang(640,120,.9,8)
fg+=f'<g transform="translate(400 350)" fill="{SIL}"><path d="M-40 0 Q-70 -60 -40 -110 Q-20 -130 -6 -112 Q-30 -70 -14 0Z"/><path d="M40 0 Q70 -60 40 -110 Q20 -130 6 -112 Q30 -70 14 0Z"/>'+''.join(f'<path d="M{a*k} {-30*k2} l{a*14} -6" stroke="{SIL}" stroke-width="5"/>' for a in (-1,1) for k,k2 in [(52,1),(56,2)])+'</g>'+f'<path d="M0 340 L1000 340 L1000 560 L0 560Z" fill="#8fa6a2" opacity=".6"/>'
P.append(panel(bg,fg,3,u))
# 4 岩の上でぐったり。水ぎわからマロがのぞく
u='q4'; fg=g(TT('dizzy'),260,330,1.2,-80)+''.join(star(x,y,s) for x,y,s in [(220,190,1),(300,170,1.2)])
fg+=f'<path d="M560 420 Q760 400 1000 420 L1000 560 L560 560Z" fill="#8fa6a2"/>'+f'<g>{g(sil(ch("マロ")),760,470,.9)}</g>'+''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#f6efd0"/><circle cx="{x-2}" cy="{y+1}" r="3.5" fill="#16303a"/>' for x,y in [(719,422),(801,422)])
fg+=''.join(f'<path d="M{x} 470 q10 -6 20 0" fill="none" stroke="#e8f2f4" stroke-width="3"/>' for x in (640,700,860))
P.append(panel(shore(u),fg,4,u))
# 5 トト、こわがらずにキラキラ目で水ぎわへ
u='q5'; fg=g(TT('spark'),300,320,1.3,10)+f'<path d="M560 420 Q760 400 1000 420 L1000 560 L560 560Z" fill="#8fa6a2"/>'+g(MARO('n','down',False),780,430,1.1)
fg+=twinkle(180,180,1)+twinkle(420,170,.8)+f'<path d="M430 300 q30 -8 50 4 M432 330 q30 0 50 10" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>'
P.append(panel(shore(u),fg,5,u))
# 6 マロが三葉虫をはさみで見せる。したり顔
u='q6'; fg=f'<rect width="{W}" height="{H}" fill="#fff3d6"/>'+burst(560,300,44,240,700)+g(MARO('smug','up',False),560,320,1.9)+trilo(560,120,1.4)+twinkle(470,90,.8)+twinkle(660,80,.8)
P.append(panel('',fg,6,u))
# 7 トトが口を開けて待つ → マロが自分でひと飲み
u='q7'; fg=g(TT('happy'),270,320,1.25)+f'<path d="M560 420 Q760 400 1000 420 L1000 560 L560 560Z" fill="#8fa6a2"/>'+g(MARO('smug','eat',False),770,400,1.3)
fg+=trilo(770,440,.85)+''.join(f'<path d="M{x} {y} q8 -10 16 0" fill="none" stroke="{O}" stroke-width="3.5" stroke-linecap="round"/>' for x,y in [(880,330),(900,370)])+''.join(f'<text x="{x}" y="{y}" font-family="{F}" font-weight="900" font-size="34" fill="{O}">…</text>' for x,y in [(380,200)])
P.append(panel(shore(u),fg,7,u))
# 8 夜。岩の上で眠るトト。水の中から、2つの目がじっと見ている
u='q8'; bg=shore(u)+night(u)+stars_(80,9,220)
fg=g(TT('sleep'),260,360,1.0,-6)+zzz(330,250,.8)+f'<path d="M560 420 Q760 400 1000 420 L1000 560 L560 560Z" fill="#2c3f48"/>'
fg+=''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#f6efd0"/><circle cx="{x-2}" cy="{y+1}" r="3.5" fill="#16303a"/>' for x,y in [(760,446),(810,446)])
P.append(panel(bg,fg,8,u))
json.dump(P,open('ep02_panels.json','w'),ensure_ascii=False)

if __name__=='__main__':
    import asyncio, sheets, os
    os.makedirs('out',exist_ok=True)
    print(asyncio.run(sheets.render('第2話_うみのなかの目',P,'第2話\u3000うみのなかの目','約5億年前、カンブリア紀。陸にはまだ草も木もなく、生き物のほとんどは海の中にいた。',True)))
