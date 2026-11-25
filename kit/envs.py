from epkit import *
def bering(u,m='day'):
    o=sky(u,'#cfdbe0','#eef2ee')+mountains(u,250,'#b5c0c2',True,4)+sea(u,250,560,'#93aeb7',2)
    o+=floe(u,820,270,60)+floe(u,140,290,40)
    return o
def bering_front(u): return rock(u,80,560,120,70,'#8f8a80')+rock(u,930,560,110,90,'#8f8a80')+kelp(u,200,560,90)+kelp(u,780,560,70)
def cambrian(u,m='day'):
    o=underwater(u,'#5f9c9a','#2f5f66',430,'#8c8a6a',3)
    o+=sponge(u,120,440,90)+sponge(u,170,440,60,'#b98a62')+sponge(u,860,440,110,'#c9a06f')+kelp(u,780,440,140,'#6f8f5c')+kelp(u,260,440,100,'#7a9a62')
    return o
def creta_sea(u,m='day'):
    o=underwater(u,'#6aa7c2','#2c5a78',440,'#a99a76',5)+kelp(u,140,440,150)+kelp(u,880,440,120)+rock(u,720,450,80,50,'#8d8573')
    return o
def yangtze(u,m='day'):
    o=sky(u,'#e8dcc4','#efe6d2')+mountains(u,230,'#c9c3b2',False,7)
    o+=wash(u,'M0 230 L1000 230 L1000 270 L0 270Z','#a9b48e')+reeds(u,120,262,10,40)+reeds(u,760,262,10,40)
    o+=sea(u,268,560,'#b39f78',3)
    return o
def madagascar(u,m='day'):
    o=sky(u,'#f2dcb4','#f8ecd2')+mountains(u,300,'#cdb79a',False,9)+ground(u,300,'#d8b27e',4)+baobab(u,170,330,1.1)+baobab(u,840,320,0.9)
    for x in range(10,1000,60): o+=grass(u,x,306,5,16,x,'#a08a4c')
    return o
def tasmania(u,m='day'):
    o=sky(u,'#dfe6d8','#eef1e6')+mountains(u,300,'#a8b6a4',False,11)+ground(u,310,'#b8b68a',5)
    for x,h in [(80,260),(220,220),(820,250),(940,280)]: o+=euc(u,x,330,h)
    for x in range(10,1000,50): o+=grass(u,x,316,5,18,x)
    return o
def shikoku(u,m='day'):
    o=sky(u,'#e4eee6','#f2f4ea')+mountains(u,250,'#8fae8a',False,13)+mountains(u,270,'#a7c29c',False,14)
    o+=ground(u,270,'#b8cf98',6)+wash(u,'M0 330 Q500 300 1000 330 L1000 560 L0 560Z','#a9cfd0')+pen(u,'M0 330 Q500 300 1000 330',2.2)
    for x,y,w in [(150,400,50),(720,460,70),(880,380,40)]: o+=rock(u,x,y,w,w*0.6,'#b0a898')
    return o
def na_forest(u,m='day'):
    o=sky(u,'#e9ddc6','#f4ecda')+mountains(u,290,'#bfb5a0',False,15)+ground(u,310,'#c8b98a',7)
    for x,h,c in [(70,240,'#d79a5a'),(200,200,'#c4743f'),(820,230,'#d8a85a'),(950,260,'#b8653a')]: o+=tree_round(u,x,330,h,c)
    for x in range(10,1000,50): o+=grass(u,x,316,5,16,x,'#9a8a4c')
    return o
def creta_land(u,m='day'):
    o=sky(u,'#efd9b8','#f7ebd2')+volcano(u,720,300,150)+mountains(u,300,'#c2b39a',False,17)+ground(u,300,'#c6b78c',8)
    o+=cycad(u,100,330,1.3)+fern(u,220,330,1.2)+cycad(u,900,340,1.1)+fern(u,820,340,1)
    return o
def pleist(u,m='day'):
    o=sky(u,'#e6e6dc','#f1efe4')+mountains(u,290,'#b9c2c6',True,19)+ground(u,300,'#c9bf8a',9)
    for x in range(10,1000,40): o+=grass(u,x,306,7,24,x,'#a8984f')
    o+=conifer(u,90,320,160,'#6f876a')+conifer(u,930,320,180,'#6f876a')
    return o
def wrangel(u,m='day'):
    o=sky(u,'#d6dde2','#eef0f0')+mountains(u,280,'#c3ccd2',True,21)+ground(u,290,'#f2f3f0',10)
    for x in range(10,1000,70): o+=grass(u,x,296,4,14,x,'#a7a48a')
    r=random.Random(2); o+=''.join(f'<circle cx="{r.uniform(0,1000):.0f}" cy="{r.uniform(0,560):.0f}" r="{r.uniform(2,4):.1f}" fill="#fff" opacity=".9"/>' for _ in range(60))
    return o
def lagoon(u,m='day'):
    o=sky(u,'#f1dfb8','#f8efd8')+sea(u,260,560,'#9cc3b8',23)
    o+=wash(u,'M560 262 Q660 200 780 262Z','#b9ae7c')+cycad(u,660,250,.7)+wash(u,'M0 300 Q120 250 300 300 L300 560 L0 560Z','#d9c999')+pen(u,'M0 300 Q120 250 300 300',2.2)
    o+=cycad(u,90,300,1.2)+fern(u,220,300,1)
    return o
def natl(u,m='day'):
    o=sky(u,'#d5dbdc','#ecefec')+sea(u,250,560,'#8ea4a8',25)
    o+=rock(u,780,280,90,170,'#8d867c')+rock(u,900,270,50,90,'#8d867c')+wash(u,'M0 380 Q200 330 460 360 L520 560 L0 560Z','#9a9286')+pen(u,'M0 380 Q200 330 460 360 L520 560',2.4)
    return o
def island(u,m='day'):
    o=sky(u,'#efe2c2','#f7eed8')+sea(u,250,320,'#b9cfc8',1)+ground(u,312,'#eadbb6',2)+palm(u,40,560,330,50,3,1.2)+palm(u,960,560,300,-40,4,1.1)
    return o
