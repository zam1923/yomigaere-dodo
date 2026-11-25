import json, datetime
O='#5b4636'
S=f'stroke="{O}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
L='fill="none" '+S
def eye(x,y,r=5.5): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{O}"/><circle cx="{x+1.8}" cy="{y-1.8}" r="1.7" fill="#fff"/>'
def cheek(x,y,rx=9,ry=6,op='.7'): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f6a39a" opacity="{op}"/>'
CREST=f'<path d="M86 54 Q80 28 96 38 Q100 20 108 38 Q124 28 116 56Z" fill="#d5dfd6" {S}/>'
HEAD=f'<ellipse cx="100" cy="108" rx="64" ry="60" fill="#a9bdb6" {S}/><ellipse cx="100" cy="120" rx="44" ry="38" fill="#e3ebe2"/>'
BEAK=f'<path d="M74 112 Q100 98 126 112 Q126 146 104 160 Q94 152 98 138 Q78 134 74 112Z" fill="#f2d98d" {S}/>'
BEAKLINE=f'<path d="M98 138 Q112 140 122 128" {L}/>'
CHEEKS=cheek(56,116)+cheek(144,116)
def face(kind='n'):
    e=eye(74,98)+eye(126,98); ex=''; ch=CHEEKS; bl=BEAKLINE
    if kind=='smile': e=f'<path d="M64 100 Q74 88 84 100" {L}/><path d="M116 100 Q126 88 136 100" {L}/>'
    if kind=='sleep': e=f'<path d="M64 98 Q74 106 84 98" {L}/><path d="M116 98 Q126 106 136 98" {L}/>'; ex=f'<text x="150" y="58" font-family="Zen Maru Gothic, sans-serif" font-weight="900" font-size="26" fill="{O}">z</text><text x="168" y="38" font-family="Zen Maru Gothic, sans-serif" font-weight="900" font-size="18" fill="{O}">z</text>'
    if kind=='angry': ex=f'<path d="M62 84 L84 92" {L}/><path d="M138 84 L116 92" {L}/>'; ch=cheek(56,116,11,7,'.95')+cheek(144,116,11,7,'.95')
    if kind=='sad': ex=f'<path d="M64 90 L82 84" {L}/><path d="M136 90 L118 84" {L}/><path d="M70 108 Q64 122 70 126 Q78 122 70 108Z" fill="#9fd0ec" stroke="{O}" stroke-width="3"/>'; bl=f'<path d="M100 142 Q110 134 120 140" {L}/>'
    if kind=='wow': e=f'<circle cx="74" cy="98" r="10" fill="#fff" {S}/><circle cx="74" cy="98" r="4.5" fill="{O}"/><circle cx="126" cy="98" r="10" fill="#fff" {S}/><circle cx="126" cy="98" r="4.5" fill="{O}"/>'; bl=f'<ellipse cx="106" cy="140" rx="7" ry="9" fill="#c0564a" {S}/>'
    if kind=='shy': e=f'<path d="M64 100 Q74 92 84 100" {L}/><path d="M116 100 Q126 92 136 100" {L}/>'; ch=cheek(54,114,14,9,'.95')+cheek(146,114,14,9,'.95')+f'<path d="M46 108 L52 104 M50 116 L56 112" stroke="#e0786c" stroke-width="3" stroke-linecap="round"/>'
    if kind=='trouble': ex=f'<path d="M64 88 L82 82" {L}/><path d="M136 88 L118 82" {L}/><path d="M158 70 Q150 84 158 88 Q166 84 158 70Z" fill="#9fd0ec" stroke="{O}" stroke-width="3"/>'; bl=f'<path d="M98 140 Q106 134 114 140 Q120 144 124 138" {L}/>'
    return CREST+HEAD+BEAK+bl+e+ch+ex
WING=lambda x,flip: f'<path d="M{x} 118 Q{x-26*flip} 120 {x-30*flip} 146 Q{x-12*flip} 150 {x} 140Z" fill="#94aba3" {S}/>'
FEET=f'<path d="M78 176 L74 194 M78 176 L82 194 M78 176 L66 190" {L}/><path d="M122 176 L118 194 M122 176 L126 194 M122 176 L134 190" {L}/>'.replace(O,'#d9a441')
def svg(inner, vb='0 0 200 200', w=200, h=200, label='トト'):
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
# A: まるごと一体型(顔がそのまま体)
feetA=f'<g stroke="#b7862f" stroke-width="5" stroke-linecap="round" fill="none"><path d="M80 164 L76 190 M80 164 L84 190 M80 164 L68 186"/><path d="M120 164 L116 190 M120 164 L124 190 M120 164 L132 186"/></g>'
wingsA=f'<path d="M40 112 Q16 118 18 146 Q32 146 44 136Z" fill="#94aba3" {S}/><path d="M160 112 Q184 118 182 146 Q168 146 156 136Z" fill="#94aba3" {S}/>'
A_body=lambda k='n': feetA+wingsA+face(k)
# B: 2頭身(頭+小さな体)
bodyB=f'<ellipse cx="100" cy="182" rx="50" ry="42" fill="#a9bdb6" {S}/><ellipse cx="100" cy="192" rx="32" ry="26" fill="#e3ebe2"/><path d="M52 170 Q30 178 34 202 Q46 202 56 190Z" fill="#94aba3" {S}/><path d="M148 170 Q170 178 166 202 Q154 202 144 190Z" fill="#94aba3" {S}/><path d="M146 196 Q170 192 172 210 Q158 214 148 206Z" fill="#d5dfd6" {S}/>'
feetB=f'<g stroke="#b7862f" stroke-width="5" stroke-linecap="round" fill="none"><path d="M84 220 L80 240 M84 220 L88 240 M84 220 L72 236"/><path d="M116 220 L112 240 M116 220 L120 240 M116 220 L128 236"/></g>'
B_body=lambda k='n': feetB+bodyB+f'<g transform="translate(18 -6) scale(.82)">{face(k)}</g>'
ART={'orig':svg(face('n')),'A':svg(A_body(),'0 10 200 200',260,260,'トト まるごと一体型'),'B':svg(B_body(),'0 10 200 240',236,283,'トト 2頭身')}
EX=[('n','ふつう'),('smile','にっこり'),('sleep','ねむい'),('angry','おこる'),('sad','かなしい'),('wow','びっくり'),('shy','てれる'),('trouble','こまる')]
json.dump({'ART':ART,'EX':[(k,n,svg(A_body(k),'0 10 200 200',170,170,'トト '+n)) for k,n in EX],'STAMP':[(k,svg(A_body(k),'0 10 200 200',230,230,'トト')) for k in ['sleep','smile','trouble','shy']],'ICON':svg(face('n'),'0 0 200 200',40,40,'トト')},open('art.json','w'),ensure_ascii=False)
