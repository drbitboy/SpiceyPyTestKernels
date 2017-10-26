# Hack CSPICE to log calls to SPKPVN

### A few directories:

* This repo, .../SpiceyPyTestKernels/
* CSPICE N0066 source for cspice.a:  .../SpiceyPy/cspice/src/cspice/
* SpiceyPy wrapper repo, .../SpiceyPy/

This file resides in .../SpicePyTestKernels/code/

To use these files:

1. Copy patched source to CSPICE source:

    cd .../SpicePyTestKernels/code/
    cp btclogspkpvn.c spkpvn.c.n0066.patched .../SpiceyPy/cspice/src/spice/

2. Build patched source and log source in CSPICE and add to CSPICE library:

    cd .../SpiceyPy/cspice/src/cspice/
    gcc -c -ansi -m64 -O2 -fPIC -DNON_UNIX_STDIO btclogspkpvn.c spkpvn.c 
    ar rv ../../lib/cspice.a *.o
    ranlib ../../lib/cspice.a 

3. Rebuild spice.so:

    cd .../SpiceyPy/
    find . -name spice.so | xargs rm -v
    python setup.py build

4. Generate log of SPKPVN calls (BASH):

    cd .../SpiceyPy/
    BTC_LOG_SPKPVN=spkpvn_log.txt python setup.py test

5. Generate and use SPKMERGE setup file:

    cd .../SpiceyPyTestKernels/
    cp .../SpiceyPy/spkpvn_log.txt ./
    python code/sumpvn.py spkpvn
    BTC_LOG_SPKPVN=spkpvn_log.txt python setup.py test
    sort -u -k1,1 -k2,2n -k3,3n -u spkpvn_log.txt > sort-u_spkpvn_log.txt
    python sumpvn.py sort-u_spkpvn_log.txt > allspk.spkmerge
    rm -f allspk.bsp
    spkmerge allspk.spkmerge

### N.B. To re-create spkpvn.c.n0066.patched

    cd .../SpiceyPyTest/code/
    make clean all
    mv -f spkpvn.c spkpvn.c.n0066.patched
