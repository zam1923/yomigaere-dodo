import math
O='#5b4636'
S=f'stroke="{O}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
L='fill="none" '+S
def mirror(d): return f'<g transform="translate(200 0) scale(-1 1)">{d}</g>'
def both(d): return d+mirror(d)
def spiral(cx,cy):
    pts=[]; t=0
    while t<=15.5:
        r=5+t*3.1; pts.append(f'{cx+math.cos(t)*r:.1f} {cy+math.sin(t)*r:.1f}'); t+=0.25
    return f'<path d="M{" L".join(pts)}" {L}/>'
def legs(x1=80,x2=120,y=164,col='#b7862f'):  # 鳥の足
    f=lambda x,s: f'<path d="M{x} {y} L{x-4} {y+26} M{x} {y} L{x+4} {y+26} M{x} {y} L{x+12*s} {y+22}"/>'
    return f'<g stroke="{col}" stroke-width="5" stroke-linecap="round" fill="none">{f(x1,-1)}{f(x2,1)}</g>'
def paws(x1=78,x2=122,y=150,col='#8f6642'):  # けものの足
    return ''.join(f'<ellipse cx="{x}" cy="{y+12}" rx="15" ry="11" fill="{col}" {S}/>' for x in (x1,x2))
# 各キャラ: back=体のうしろの部品(左右ある), body=体, face=顔の部品(目・ほっぺ以外), eyes=(x1,x2,y), cheeks=(x1,x2,y), top=体の上に重なる部品, bc=後ろ姿の色, feet=足, eyesFn=特殊な目
C=[]
def add(**k): C.append(k)
# 0 トト
add(n='トト',sp='ドードー',feet=legs(),
 back=f'<path d="M40 112 Q16 118 18 146 Q32 146 44 136Z" fill="#94aba3" {S}/>'+f'<path d="M160 112 Q184 118 182 146 Q168 146 156 136Z" fill="#94aba3" {S}/>'+f'<path d="M86 54 Q80 28 96 38 Q100 20 108 38 Q124 28 116 56Z" fill="#d5dfd6" {S}/>',
 body=f'<ellipse cx="100" cy="108" rx="64" ry="60" fill="#a9bdb6" {S}/>',
 face='<ellipse cx="100" cy="120" rx="44" ry="38" fill="#e3ebe2"/>'+f'<path d="M74 112 Q100 98 126 112 Q126 146 104 160 Q94 152 98 138 Q78 134 74 112Z" fill="#f2d98d" {S}/><path d="M98 138 Q112 140 122 128" {L}/>',
 eyes=(74,126,98),cheeks=(56,144,116),bc='#9fb4ad')
# 1 ステラ
add(n='ステラ',sp='ステラーカイギュウ',feet=both(f'<path d="M44 132 Q22 146 30 164 Q44 160 54 146Z" fill="#7f9fb8" {S}/>'),
 back='',body=f'<path d="M36 112 Q36 52 100 52 Q164 52 164 112 Q164 160 100 160 Q36 160 36 112Z" fill="#8fb0c8" {S}/>',
 face=f'<ellipse cx="100" cy="126" rx="42" ry="27" fill="#d3e2eb" {S}/>'+f'<circle cx="91" cy="116" r="2.6" fill="{O}"/><circle cx="109" cy="116" r="2.6" fill="{O}"/><path d="M88 133 Q100 141 112 133" {L}/>'+both(f'<circle cx="72" cy="128" r="2" fill="{O}"/><circle cx="78" cy="138" r="2" fill="{O}"/>'),
 eyes=(64,136,94),cheeks=(50,150,110),bc='#86a6be',tail=f'<path d="M100 156 Q70 176 74 192 Q100 182 126 192 Q130 176 100 156Z" fill="#7f9fb8" {S}/>')
# 2 ハルル
sp=''.join(f'<path d="M{x-9} 98 L{x} 54 L{x+9} 98Z" fill="#f6e6f7" {S}/>' for x in [62,84,106,128,150])
lg=''.join(f'<path d="M{x} 128 Q{x-4} 148 {x+3} 166" {L}/>' for x in [62,84,106,128,150])
add(n='ハルル',sp='ハルキゲニア',feet=lg,back=sp,body=f'<rect x="42" y="90" width="126" height="44" rx="22" fill="#cba6da" {S}/><circle cx="42" cy="106" r="27" fill="#cba6da" {S}/>',
 face=f'<path d="M36 114 Q42 119 48 114" {L}/>',eyes=(32,52,102),cheeks=(24,60,112),bc='#c19bd1',long=1)
# 3 ミオ
add(n='ミオ',sp='ヨウスコウカワイルカ',feet='',back=f'<path d="M116 62 Q130 30 148 62Z" fill="#cfe3ea" {S}/><path d="M122 148 Q126 174 146 166 Q144 152 136 144Z" fill="#cfe3ea" {S}/>',
 body=f'<path d="M66 104 Q30 108 16 124 Q12 134 24 136 Q50 138 74 128Z" fill="#e9f3f5" {S}/>'+f'<ellipse cx="114" cy="104" rx="58" ry="50" fill="#e9f3f5" {S}/>',
 face=f'<path d="M20 129 Q48 128 70 118" {L}/>',eyes=(92,138,96),cheeks=(104,150,114),bc='#dde9ec',long=1)
# 4 モナ
add(n='モナ',sp='アンモナイト',feet=f'<path d="M44 166 q-4 12 2 20 M62 172 q0 12 4 18 M80 166 q6 10 2 20" {L}/>',back='',
 body=f'<circle cx="114" cy="92" r="58" fill="#b9a8e0" {S}/>'+spiral(114,92)+f'<ellipse cx="62" cy="146" rx="36" ry="27" fill="#f3ddcb" {S}/>',
 face=f'<path d="M56 152 Q62 157 68 152" {L}/>',eyes=(50,74,142),cheeks=(36,88,152),bc='#ad9bd6',long=1)
# 5 エピ
add(n='エピ',sp='エピオルニス',feet='',back=f'<path d="M82 196 L88 110 Q100 92 112 110 L118 196Z" fill="#b89f78" {S}/>'+f'<path d="M92 46 Q96 30 102 44 Q110 32 110 48" fill="#b89f78" {S}/>',
 body=f'<ellipse cx="100" cy="78" rx="42" ry="35" fill="#c6ae86" {S}/>',
 face=f'<path d="M84 84 Q100 76 116 84 Q110 106 100 108 Q90 106 84 84Z" fill="#f0c97a" {S}/>',eyes=(78,122,72),cheeks=(66,134,86),bc='#bba27b',
 prop=f'<ellipse cx="154" cy="158" rx="26" ry="33" fill="#fbf3dc" {S}/><circle cx="146" cy="150" r="2.5" fill="#d9c9a3"/><circle cx="160" cy="166" r="2.5" fill="#d9c9a3"/><circle cx="158" cy="142" r="2" fill="#d9c9a3"/>')
# 6 シマ
add(n='シマ',sp='フクロオオカミ',feet=paws(col='#cfa96e'),back=both(f'<path d="M52 72 L48 26 L86 52Z" fill="#dcb980" {S}/><path d="M58 54 L56 40 L68 50Z" fill="#f2c9b0"/>'),
 body=f'<ellipse cx="100" cy="104" rx="62" ry="56" fill="#dcb980" {S}/>'+f'<path d="M84 51 L88 70 M100 48 L100 72 M116 51 L112 70" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round"/>',
 face=f'<ellipse cx="100" cy="128" rx="30" ry="24" fill="#f7ead0" {S}/><ellipse cx="100" cy="116" rx="9" ry="6" fill="{O}"/><path d="M100 122 L100 131 M90 135 Q100 142 110 135" {L}/>',
 eyes=(72,128,98),cheeks=(54,146,116),bc='#d2ae74',backmark=f'<path d="M70 96 L76 116 M86 92 L90 118 M100 90 L100 118 M114 92 L110 118 M130 96 L124 116" fill="none" stroke="{O}" stroke-width="6" stroke-linecap="round"/>',tail=f'<path d="M150 130 Q182 132 190 150 Q176 152 152 146Z" fill="#dcb980" {S}/>')
# 7 オパ
st=''
for x,y in zip([64,82,100,118,136],[66,54,48,54,66]): st+=f'<path d="M{x} 86 L{x} {y}" {L}/><circle cx="{x}" cy="{y}" r="9" fill="#fff" {S}/><circle cx="{x}" cy="{y+1}" r="3.6" fill="{O}"/>'
add(n='オパ',sp='オパビニア',feet='',back=both(f'<circle cx="42" cy="104" r="13" fill="#b5e3d6" {S}/><circle cx="38" cy="126" r="13" fill="#b5e3d6" {S}/><circle cx="46" cy="146" r="13" fill="#b5e3d6" {S}/>')+st,
 body=f'<ellipse cx="100" cy="122" rx="60" ry="44" fill="#84cdb8" {S}/>',
 face=f'<path d="M100 134 Q100 164 124 170 Q140 172 142 158" fill="none" stroke="{O}" stroke-width="17" stroke-linecap="round"/><path d="M100 134 Q100 164 124 170 Q140 172 142 158" fill="none" stroke="#9adbc8" stroke-width="8" stroke-linecap="round"/><path d="M88 116 Q100 124 112 116" {L}/>',
 eyes=None,cheeks=(66,134,120),bc='#7ac4af',stalks=1)
# 8 セセ
add(n='セセ',sp='ニホンカワウソ',feet=paws(col='#8f6642'),back=both(f'<circle cx="52" cy="64" r="15" fill="#8f6642" {S}/>'),
 body=f'<ellipse cx="100" cy="104" rx="64" ry="56" fill="#ad7d55" {S}/>',
 face=f'<ellipse cx="100" cy="126" rx="38" ry="27" fill="#f5e4c8" {S}/><path d="M88 110 Q100 104 112 110 Q108 122 100 122 Q92 122 88 110Z" fill="{O}"/><path d="M100 122 L100 130 M88 134 Q100 143 112 134" {L}/>'+both(f'<path d="M66 124 L42 119 M66 132 L44 137" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round"/>'),
 eyes=(72,128,94),cheeks=(54,146,108),bc='#a37550',tail=f'<path d="M152 132 Q186 128 196 150 Q180 156 150 150Z" fill="#8f6642" {S}/>')
# 9 ポポ
add(n='ポポ',sp='リョコウバト',feet=legs(84,116,158,'#d0705f'),back=both(f'<path d="M46 108 Q28 130 46 148Z" fill="#6b8ba6" {S}/>')+f'<path d="M94 46 Q100 32 106 46" {L}/>',
 body=f'<ellipse cx="100" cy="104" rx="58" ry="58" fill="#7fa0bb"/><path d="M50 124 Q100 100 150 124 Q142 162 100 162 Q58 162 50 124Z" fill="#eda88f"/><ellipse cx="100" cy="104" rx="58" ry="58" {L}/>',
 face=f'<path d="M89 104 L111 104 L100 122Z" fill="#f0c97a" {S}/>',eyes=(76,124,92),cheeks=(60,140,108),bc='#7798b3',tail=f'<path d="M150 120 L196 112 L188 128 L150 134Z" fill="#6b8ba6" {S}/>')
# 10 マロ
add(n='マロ',sp='アノマロカリス',feet='',back=both(f'<ellipse cx="42" cy="96" rx="17" ry="10" fill="#f8d695" {S}/><ellipse cx="38" cy="120" rx="17" ry="10" fill="#f8d695" {S}/><ellipse cx="46" cy="144" rx="17" ry="10" fill="#f8d695" {S}/>')+both(f'<path d="M68 78 L50 54" {L}/><circle cx="48" cy="50" r="12" fill="#fff" {S}/><circle cx="50" cy="51" r="5" fill="{O}"/>'),
 body=f'<ellipse cx="100" cy="116" rx="52" ry="54" fill="#f0b65a" {S}/>',
 face=both(f'<path d="M84 130 Q74 152 88 162 Q98 164 97 152" fill="none" stroke="{O}" stroke-width="16" stroke-linecap="round"/><path d="M84 130 Q74 152 88 162 Q98 164 97 152" fill="none" stroke="#e7963a" stroke-width="7" stroke-linecap="round"/>')+f'<path d="M90 112 Q100 120 110 112" {L}/>',
 eyes=None,cheeks=(70,130,106),bc='#e6ab50',stalks=1)
# 11 アトル
add(n='アトル',sp='ケツァルコアトルス',feet=legs(86,114,140),back=both(f'<path d="M62 118 Q20 98 8 142 Q30 136 40 152 Q52 140 66 146Z" fill="#c1cdf1" {S}/>')+f'<path d="M84 60 Q68 22 106 40 Q100 52 106 60Z" fill="#f2a56b" {S}/>',
 body=f'<ellipse cx="100" cy="100" rx="50" ry="46" fill="#9db0e8" {S}/>',
 face=f'<path d="M82 108 Q100 98 118 108 L103 180 Q100 186 97 180Z" fill="#f8e3a6" {S}/><path d="M100 112 L100 150" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round"/>',
 eyes=(76,124,94),cheeks=(62,138,110),bc='#94a8e2')
# 12 キバ
add(n='キバ',sp='スミロドン',feet=paws(col='#d9944f'),back=both(f'<circle cx="54" cy="62" r="17" fill="#d9944f" {S}/><circle cx="56" cy="64" r="7" fill="#f2c9b0"/>'),
 body=f'<ellipse cx="100" cy="102" rx="64" ry="56" fill="#e3a763" {S}/><path d="M92 50 L94 64 M108 50 L106 64" fill="none" stroke="#b9743a" stroke-width="5" stroke-linecap="round"/>',
 face=both(f'<path d="M80 136 L85 174 Q88 180 91 174 L95 138Z" fill="#fff" {S}/>')+f'<ellipse cx="100" cy="124" rx="34" ry="23" fill="#f9ecd2" {S}/><path d="M90 112 L110 112 L100 123Z" fill="#c7705f" stroke="{O}" stroke-width="3" stroke-linejoin="round"/><path d="M100 123 L100 132" {L}/>',
 eyes=(72,128,94),cheeks=(52,148,110),bc='#d99d5a',tail=f'<path d="M154 128 Q180 130 184 144 Q170 146 152 142Z" fill="#d9944f" {S}/>')
# 13 ケナ
add(n='ケナ',sp='ケナガマンモス',feet=paws(76,124,152,'#946a4e'),back=both(f'<ellipse cx="38" cy="104" rx="17" ry="24" fill="#946a4e" {S}/>'),
 body=f'<ellipse cx="100" cy="100" rx="60" ry="58" fill="#a87a5c" {S}/><path d="M62 64 Q68 28 100 32 Q132 28 138 64 Q120 50 100 60 Q80 50 62 64Z" fill="#7e563d" {S}/>',
 face=both(f'<path d="M70 132 Q50 172 86 178 Q70 160 82 138Z" fill="#fbf3dc" {S}/>')+f'<path d="M86 112 Q100 104 114 112 L112 162 Q112 178 100 178 Q88 178 88 162Z" fill="#b98a6a" {S}/><path d="M92 134 L108 134 M92 150 L108 150" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round"/>',
 eyes=(72,128,96),cheeks=(56,144,114),bc='#9f7356',tail=f'<path d="M156 118 Q174 124 172 140" fill="none" stroke="#946a4e" stroke-width="6" stroke-linecap="round"/>')
# 14 アーケ
add(n='アーケ',sp='始祖鳥',feet=legs(84,116,152),back=f'<path d="M86 58 Q78 22 96 34 Q100 14 108 34 Q126 24 116 60Z" fill="#f2c14e" {S}/>'+both(f'<path d="M48 106 Q16 102 12 138 L30 128 L32 148 L50 134Z" fill="#4f9fc4" {S}/>'),
 body=f'<ellipse cx="100" cy="104" rx="54" ry="52" fill="#74b6d6" {S}/>',
 face='<ellipse cx="100" cy="130" rx="30" ry="20" fill="#d9eff7"/>'+f'<path d="M84 102 L116 102 L100 128Z" fill="#f0c97a" {S}/><path d="M90 111 L110 111" fill="none" stroke="{O}" stroke-width="3" stroke-linecap="round"/>',
 eyes=(76,124,90),cheeks=(62,138,106),bc='#6cadce',tail=f'<path d="M148 128 Q180 120 196 136 Q180 140 186 150 Q168 146 148 140Z" fill="#4f9fc4" {S}/>')
# 15 オーク
add(n='オーク',sp='オオウミガラス',feet=legs(84,116,160,'#2f3a4a'),back=both(f'<path d="M46 112 Q26 134 44 154Z" fill="#374558" {S}/>'),
 body=f'<ellipse cx="100" cy="104" rx="58" ry="60" fill="#44546a"/><path d="M58 128 Q100 104 142 128 Q138 164 100 164 Q62 164 58 128Z" fill="#fbf7ea"/><ellipse cx="100" cy="104" rx="58" ry="60" {L}/>',
 face=both('<ellipse cx="74" cy="90" rx="15" ry="11" fill="#fff"/>')+f'<path d="M84 104 Q100 96 116 104 Q112 134 100 138 Q88 134 84 104Z" fill="#2f3a4a" {S}/><path d="M90 115 Q100 111 110 115 M92 125 Q100 121 108 125" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>',
 eyes=(77,123,91),cheeks=(58,142,112),bc='#3d4c60')
