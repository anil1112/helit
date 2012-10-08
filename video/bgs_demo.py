#! /usr/bin/env python

# Copyright 2012 Tom SF Haines

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import sys
import video



lumScale = 0.7
noiseFloor = 0.15
quarter = True


man = video.Manager()


vid = video.ReadCamCV()
man.add(vid)

if quarter:
  vid_old = vid
  vid = video.Half()
  vid.source(0,vid_old)
  man.add(vid)
  


cb = video.ColourBias(lumScale, noiseFloor, man.getCL())
cb.source(0,vid)
man.add(cb)

cb_h = video.Half()
cb_h.source(0,cb)
man.add(cb_h)

lc = video.LightCorrectMS()
lc.source(0,cb_h)
man.add(lc)

bs = video.BackSubDP(man.getCL())
bs.source(0,cb)
bs.source(1,lc,0)
man.add(bs)

lc.source(1,bs,2)


bs.setDP(comp=6, conc=0.01, cap=128.0)
bs.setHackDP(min_weight = 0.0005)
bs.setBP(threshold = 0.4, half_life = 0.05, iters = 2)
bs.setExtraBP(cert_limit = 0.005, change_limit = 0.001, min_same_prob = 0.99, change_mult = 3.0)
bs.setOnlyCL(minSize = 64, maxLayers = 8, itersPerLevel = 2)


mr = video.RenderMask(bgColour=(0.0,0.0,1.0))
mr.source(0,bs)
mr.source(1,vid)
man.add(mr)

ref = video.Reflect()
ref.source(0,mr)
man.add(ref)

out = video.ViewPyGame(320,240)
out.source(0,ref)
man.add(out)


man.run(profile=True)
