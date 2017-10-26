"""
Script sumpvn.py

Purpose:

  Convert ET lookups in SpiceyPy testing to SPKMERGE file

Usage:

  # CHDIR to top of SpiceyPy repo
  BTC_LOG_SPKPVN=spkpvn_log.txt python setup.py test

  # CHDIR to directory with all SPKs e.g.
  # - SpiceyPy/spiceypy/tests/
  #  OR
  # - SpiceyPyTestKernels/

  sort -u -k1,1 -k2,2n -k3,3n .../SpiceyPy/spkpvn_log.txt > sort-u_spkpvn_log.txt

  python sumpvn.py sort-u_spkpvn_log.txt | tee allspk.spkmerge

  rm -f allspk.bsp
  spkmerge allspk.spkmerge

"""
import os
import sys
import pprint
import spiceypy as sp

doDebug = "DEBUG" in os.environ

if "__main__" == __name__ and sys.argv[1:]:
  d = dict()
  ninetyDaysPlus = (90 * 86400) + 600
  with open(sys.argv[1],'rb') as fIn:
    for rawline in fIn:
      path,target,strET,ctr = rawline.strip().split()

      et = int(strET)
      bn = os.path.basename(path)

      if not (bn in d):
        d[bn] = dict(path=path)

      if not (target in d[bn]):
        d[bn][target] = [[et,et,0]]

      lastEt = d[bn][target][-1][1]
      if et == lastEt: continue

      assert et > lastEt

      delEt = et - lastEt

      if delEt > ninetyDaysPlus:
        d[bn][target].append([et,et,0])
        continue

      d[bn][target][-1][1] = et
      d[bn][target][-1][2] = (et - d[bn][target][-1][0]) / 864e3

  if doDebug: pprint.pprint(d,stream=sys.stderr)

  print('LEAPSECONDS_KERNEL = naif0012.tls')
  print('SPK_KERNEL = allspk.bsp')
  for bn in d:
    dbn = d[bn]
    path = dbn['path']
    for target in dbn:
      if target == 'path': continue
      for dbntn in dbn[target]:
        print('  SOURCE_SPK_KERNEL = {}'.format(bn))
        print('    BODIES = {}'.format(target))
        print('    BEGIN_TIME = {} TDB'.format(sp.etcal(dbntn[0] - 600)))
        print('    END_TIME = {} TDB'.format(sp.etcal(dbntn[1] + 600)))
