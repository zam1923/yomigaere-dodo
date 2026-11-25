import re,sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from chars import C,O,S,L,mirror
def eye(x,y,r=5.5): return f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{O}"/><circle cx="{x+1.8*r/5.5:.1f}" cy="{y-1.8*r/5.5:.1f}" r="{1.7*r/5.5:.2f}" fill="#fff"/>'
def cheek(x,y,rx=9,ry=6): return f'<ellipse cx="{x:.1f}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f6a39a" opacity=".7"/>'
def tx(s,a,dx,cx=100): return f'<g transform="translate({cx+dx} 0) scale({a} 1) translate({-cx} 0)">{s}</g>'
def recolor(s,c): return re.sub(r'fill="#[0-9a-fA-F]{3,6}"',f'fill="{c}"',s)
def front(c):
    e=''
    if c['eyes']: x1,x2,y=c['eyes']; e=eye(x1,y)+eye(x2,y)
    x1,x2,y=c['cheeks']; ch=cheek(x1,y)+cheek(x2,y)
    return c.get('feet','')+c['back']+c['body']+c['face']+e+ch+c.get('prop','')
def three(c):
    if c.get('long'): return tx(front(c),0.88,-2)
    a,dx=0.86,-16
    T=lambda x:100+(x-100)*a+dx
    e=''
    if c['eyes']: x1,x2,y=c['eyes']; e=eye(T(x1),y)+eye(T(x2)-4,y,5)
    x1,x2,y=c['cheeks']; ch=cheek(T(x1),y,7,5)+cheek(T(x2)-4,y)
    return tx(c.get('feet',''),0.9,-4)+c.get('tail','')+tx(c['back'],0.92,8)+c['body']+tx(c['face'],a,dx)+e+ch+tx(c.get('prop',''),0.9,6)
def side(c):
    if c.get('long'): return front(c)
    a,dx=0.5,-40
    T=lambda x:100+(x-100)*a+dx
    e=''
    if c['eyes']: x1,x2,y=c['eyes']; e=eye(T(x1)+6,y)
    x1,x2,y=c['cheeks']; ch=cheek(T(x1)+12,y)
    return tx(c.get('feet',''),0.6,4)+c.get('tail','')+tx(c['back'],0.6,10)+tx(c['body'],0.94,0)+tx(c['face'],a,dx)+e+ch+tx(c.get('prop',''),0.8,10)
def back(c):
    if c.get('long'):
        b=recolor(c['body'],c['bc'])
        return mirror(c.get('feet','')+c['back']+b)
    b=recolor(c['body'],c['bc'])
    return c.get('feet','')+c.get('prop','')+b+c.get('backmark','')+c['back']
def svg(inner,w=200,label=''):
    return f'<svg viewBox="0 10 200 200" width="{w}" height="{w}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
VIEWS=[('正面',front),('斜め前',three),('横',side),('後ろ',back)]
