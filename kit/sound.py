"""リール用の音を一から合成する(著作権のある素材は使わない)。
make(path, panel_sec, end_sec, moods, sfx): moods はコマごとに 'light' / 'dark'、sfx は {コマ番号: 種類}
"""
import numpy as np, wave
SR=44100
def env(n,a=0.005,d=1.2):
    t=np.arange(n)/SR; e=np.exp(-t/d); k=int(a*SR); e[:k]*=np.linspace(0,1,k); return e
def bell(f,dur=1.4,amp=.25):
    n=int(dur*SR); t=np.arange(n)/SR
    w=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*2.01*t)+.15*np.sin(2*np.pi*f*3.02*t)
    return amp*w*env(n,.003,.45)
def musicbox(total):
    out=np.zeros(int(total*SR)+SR*2)
    scale=[523.25,587.33,659.25,783.99,880.0,1046.5]
    pat=[0,2,4,2,3,1,2,0, 0,2,5,4,3,2,1,2]
    beat=0.42; i=0; t=0.0
    while t<total:
        f=scale[pat[i%len(pat)]]; s=int(t*SR); b=bell(f)
        out[s:s+len(b)]+=b
        if i%4==0:
            lb=bell(f/2,1.8,.16); out[s:s+len(lb)]+=lb
        i+=1; t+=beat
    return out[:int(total*SR)]
def drone(total):
    n=int(total*SR); t=np.arange(n)/SR
    w=sum(np.sin(2*np.pi*f*t+ph) for f,ph in [(65.4,0),(98.0,1),(77.8,2)])
    trem=0.6+0.4*np.sin(2*np.pi*0.25*t)
    return 0.09*w*trem
def noise(n): return np.random.default_rng(1).uniform(-1,1,n)
def sfx(kind):
    if kind=='sparkle':
        out=np.zeros(int(1.6*SR))
        for i,f in enumerate([1318.5,1568,1975.5,2637]):
            b=bell(f,1.2,.18); s=int(i*0.07*SR); out[s:s+len(b)]+=b
        return out
    if kind=='stamp':
        n=int(.35*SR); t=np.arange(n)/SR; return .9*np.sin(2*np.pi*(90-60*t)*t)*env(n,.001,.08)+.25*noise(n)*env(n,.001,.02)
    if kind=='crack':
        n=int(.5*SR); x=noise(n)*env(n,.001,.03)
        for k in (0.0,0.08,0.17): s=int(k*SR); m=int(.06*SR); x[s:s+m]+=noise(m)*env(m,.001,.015)
        return .6*np.diff(x,prepend=0)*3
    if kind=='pop':
        n=int(.25*SR); t=np.arange(n)/SR; return .5*np.sin(2*np.pi*(300+1400*t)*t)*env(n,.002,.08)
    if kind=='splash':
        n=int(.9*SR); x=noise(n)*env(n,.01,.25); x=np.convolve(x,np.ones(6)/6,'same'); return .5*x
    if kind=='gulp':
        n=int(.3*SR); t=np.arange(n)/SR; return .5*np.sin(2*np.pi*(500-350*t)*t)*env(n,.002,.1)
    return np.zeros(1)
def make(path,panel_sec,end_sec,moods,fx):
    total=panel_sec*len(moods)+end_sec; n=int(total*SR)
    mb=musicbox(total); dr=drone(total)
    gl=np.zeros(n); gd=np.zeros(n)
    for i,m in enumerate(moods+[moods[-1] if moods else 'light']):
        s=int(i*panel_sec*SR); e=min(n,int((i+1)*panel_sec*SR)) if i<len(moods) else n
        (gd if m=='dark' else gl)[s:e]=1
    k=int(.4*SR); kern=np.ones(k)/k; gl=np.convolve(gl,kern,'same'); gd=np.convolve(gd,kern,'same')
    bed=mb*gl+dr*gd*2.2
    bed=bed/max(1e-6,np.percentile(np.abs(bed),99.5))*0.45
    mix=bed.copy()
    for i,kind in fx.items():
        s=int((i*panel_sec+0.35)*SR); x=sfx(kind); x=x/max(1e-6,np.abs(x).max())*0.6; e=min(n,s+len(x)); mix[s:e]+=x[:e-s]
    mix=np.tanh(mix*1.2)/np.tanh(1.2)
    fade=int(1.5*SR); mix[-fade:]*=np.linspace(1,0,fade); mix[:int(.3*SR)]*=np.linspace(0,1,int(.3*SR))
    mix*=0.9
    pcm=(mix*32767).astype(np.int16); st=np.stack([pcm,pcm],1)
    with wave.open(path,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
