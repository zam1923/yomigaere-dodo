O='#5b4636'
S=f'stroke="{O}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
L='fill="none" '+S
def eye(x,y,r=5.5): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{O}"/><circle cx="{x+1.8*r/5.5}" cy="{y-1.8*r/5.5}" r="{1.7*r/5.5:.2f}" fill="#fff"/>'
def cheek(x,y,rx=9,ry=6): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f6a39a" opacity=".7"/>'
FEET='<g stroke="#b7862f" stroke-width="5" stroke-linecap="round" fill="none">{}</g>'
def foot(x,dir=0):
    if dir==0: return f'<path d="M{x} 164 L{x-4} 190 M{x} 164 L{x+4} 190 M{x} 164 L{x-12} 186"/>' if x<100 else f'<path d="M{x} 164 L{x-4} 190 M{x} 164 L{x+4} 190 M{x} 164 L{x+12} 186"/>'
    return f'<path d="M{x} 164 L{x-2} 190 M{x-2} 190 L{x-14} 190 M{x-2} 190 L{x-10} 184"/>'
BODY=f'<ellipse cx="100" cy="108" rx="64" ry="60" fill="#a9bdb6" {S}/>'
def crest(dx=0): return f'<path d="M{86+dx} 54 Q{80+dx} 28 {96+dx} 38 Q{100+dx} 20 {108+dx} 38 Q{124+dx} 28 {116+dx} 56Z" fill="#d5dfd6" {S}/>'
WL=f'<path d="M40 112 Q16 118 18 146 Q32 146 44 136Z" fill="#94aba3" {S}/>'
WR=f'<path d="M160 112 Q184 118 182 146 Q168 146 156 136Z" fill="#94aba3" {S}/>'
TAIL=lambda x,y: f'<path d="M{x} {y} Q{x+18} {y-14} {x+26} {y-2} Q{x+18} {y+2} {x+22} {y+12} Q{x+10} {y+6} {x} {y+10}Z" fill="#d5dfd6" {S}/>'
def front():
    return FEET.format(foot(80)+foot(120))+WL+WR+crest()+BODY+'<ellipse cx="100" cy="120" rx="44" ry="38" fill="#e3ebe2"/>'+f'<path d="M74 112 Q100 98 126 112 Q126 146 104 160 Q94 152 98 138 Q78 134 74 112Z" fill="#f2d98d" {S}/><path d="M98 138 Q112 140 122 128" {L}/>'+eye(74,98)+eye(126,98)+cheek(56,116)+cheek(144,116)
def three():   # 斜め前(左向き)
    return FEET.format(foot(74)+foot(116))+TAIL(160,118)+WR+f'<path d="M46 128 Q26 134 28 156 Q40 156 50 146Z" fill="#94aba3" {S}/>'+crest(-12)+BODY+'<ellipse cx="84" cy="120" rx="40" ry="37" fill="#e3ebe2"/>'+f'<path d="M50 112 Q72 98 98 110 Q98 144 74 160 Q64 150 70 136 Q52 132 50 112Z" fill="#f2d98d" {S}/><path d="M70 136 Q84 138 94 126" {L}/>'+eye(54,97,5)+eye(104,98)+cheek(40,116,7,5)+cheek(124,116)
def side():   # 横(左向き)
    return FEET.format(foot(96,1)+foot(116,1))+TAIL(160,104)+crest(-14)+BODY+'<ellipse cx="70" cy="118" rx="30" ry="34" fill="#e3ebe2"/>'+f'<path d="M58 100 Q34 100 18 112 Q10 122 14 136 Q20 130 28 128 Q46 128 62 122Z" fill="#f2d98d" {S}/><path d="M24 126 Q40 120 58 118" {L}/>'+eye(62,94)+cheek(76,114)+f'<path d="M104 104 Q144 100 148 128 Q142 152 112 146 Q100 128 104 104Z" fill="#94aba3" {S}/><path d="M118 124 L138 120 M116 134 L136 134" {L}/>'
def back():
    return FEET.format(foot(80)+foot(120))+WL+WR+crest()+f'<path d="M88 156 Q86 180 100 186 Q114 180 112 156Z" fill="#d5dfd6" {S}/>'+BODY+'<ellipse cx="100" cy="98" rx="44" ry="38" fill="#b3c6bf"/>'
def svg(inner,w=220): return f'<svg viewBox="0 10 200 200" width="{w}" height="{w}" role="img" aria-label="トト" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def flip(inner): return f'<g transform="translate(200 0) scale(-1 1)">{inner}</g>'
VIEWS=[('正面',front()),('斜め前',three()),('横',side()),('後ろ',back())]
