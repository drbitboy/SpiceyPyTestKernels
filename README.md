# SpiceyPyTestKernels
SPICE Kernels to support SpiceyPy tests

# Purpose

Support unit testing in clones of the 
[Python wrapper for NAIF CSPICE Toolkit](https://github.com/AndrewAnnex/SpiceyPy).

## MD5 Checksums of current kernel set

    41210b787e06c1b8bce7ded3d0b930ab  130212AP_SK_13043_13058.bsp
    056c65b8a8064f2958aa097db40160b2  130220AP_SE_13043_13073.bsp
    d3acb29fd931b66e34120feb26f7efb7  13056_13057ra.bc
    a30faec21039ba589d3c88db6b5fb536  cas00167.tsc
    101419660e4fe5856d30eb624da61a3f  cas_iss_v10.ti
    99f1f5a1900afc536354306419dc119b  cas_v40.tf
    8c16afc3bd886326e852b54bd71cc751  cpck05Mar2004.tpc
    b010eb485bd01da5b651c58a6c8f8e67  de405s_bigendian.bsp
    b4bb31ce13a006a4b20c124ad58b933a  de405s_littleendian.bsp
    affa1da5adeee5ea4b0d7da54e4b69d7  earth_031228_231229_predict.bpc
    a37d8d5e3023f0df7ead0e6b40d6a5b6  earthstns_itrf93_050714.bsp
    fbde06c5abc5da969db984bb4ce5e6e0  earth_topo_050714.tf
    6445f12003d1effcb432ea2671a51f18  gm_de431.tpc
    d8d742db3f9502571fb5a5f8c55e8e62  mar022-1.bsp
    25a2fff30b0dedb4d76c06727b1895b1  naif0012.tls
    da153641f7346bd5b6a1226778e0d51b  pck00010.tpc
    68261460433bfc67b9e57bb57f79c5c9  phobos_lores.bds
    4bcaf22788efbd86707c4b3c4d63c0c3  vg200022.tsc

## Source kernels

The original sources for most of these kernels are from the generic_kernels section of the NAIF/JPL website:

    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/130212AP_SK_13043_13058.bsp
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/130220AP_SE_13043_13073.bsp
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ck/13056_13057ra.bc
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00167.tsc
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/cas_iss_v10.ti
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/cas_v40.tf
    https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de405s.bsp
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/a_old_versions/earth_031228_231229_predict.bpc
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/stations/earthstns_itrf93_050714.bsp
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/stations/earth_topo_050714.tf
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/a_old_versions/mar022-1.bsp
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc
    https://naif.jpl.nasa.gov/pub/naif/VOYAGER/kernels/sclk/vg200022.tsc

N.B. The DSK phobos_lores.bds comes from a 10deg x 10deg SPUD shape model of Phobos created by Peter C. Thomas at Cornell University, and is used by permission.

N.B. The SPK de405s_bigendian.bsp is a copy of the NAIF generic kernel de405s.bsp, and de405s_littleendian.bsp was gererated from de405s_bigendian.bsp by the BINGO SPICE utility; see https://naif.jpl.nasa.gov/pub/naif/utilities/PC_Windows_32bit/bingo.ug.
