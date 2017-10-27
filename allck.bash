#!/bin/bash

[ -f allck.bc ] && exit 0

function getargs() {
cat << EoF
allck0.bc -start 2013-feb-24-23:58 -stop 2013-feb-25-00:02
allck1.bc -start 2013-feb-25-10:15 -stop 2013-feb-25-12:30
EoF
}

getargs \
| while read ckname tailArgs ; do
    [ ! -f "$ckname" ] || rm -fv "$ckname" 1>&2
    ckslicer -lsk naif0012.tls -sclk cas00167.tsc -inputck 13056_13057ra.bc -id -82000 -timetype UTC -outputck $ckname $tailArgs | grep '[^ ]' 1>&2
    echo ==ALLCK.SOURCE==:$ckname
  done \
| grep '^==ALLCK.SOURCE==:' \
| sed  's/^==ALLCK.SOURCE==://' \
| dafcat allck.bc

rm -f allck[01].bc
