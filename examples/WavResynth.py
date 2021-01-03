import sys
import numpy  as np
import pylab  as pl
import pandas as pd
import sys
from scipy.io import wavfile as wf
from pypevoc import PVAnalysis as pv

sr, sig =  wf.read(sys.argv[1])

# scale to floating point (range -1 to 1)
sig = sig/ float(np.iinfo(sig.dtype).max)
    
# Build the phase vocoder object
mypv=pv.PV(sig,sr,nfft=2048, npks=128, hop=256)

# Run the PV calculation
mypv.run_pv()

# convert to sinusoidal lines
ss=mypv.toSinSum()

# resynthesise based on PV analysis
# (reduce hop to slow down, increase to accelerate)
w=ss.synth(sr,mypv.hop)

# plot original and resynthesis
# pl.figure()
# pl.plot(sig,label='orig')
# pl.hold(True)
# pl.plot(w,label='resynth')
# pl.legend()
# pl.show()

# fig,ax=pl.subplots(2,1,sharex=True)
# ax[0].plot(np.arange(len(sig))/float(sr),sig,label='orig')
# # ax[0].hold(True)
# ax[0].plot(np.arange(len(w))/float(sr),w,label='resynth')
# ax[0].legend()
# mypv.plot_time_freq(ax=ax[1])

ww=np.int16(w*32767)
wf.write("out.wav", sr, ww)