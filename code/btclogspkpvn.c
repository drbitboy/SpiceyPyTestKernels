#include <stdio.h>
#include <stdlib.h>
#include "SpiceUsr.h"
#include "SpiceZfc.h"
#include "SpiceZst.h"
#include "SpiceZmc.h"
 
 
void btclogspkpvn_ ( integer     * handle
                   , doublereal  * descr
                   , doublereal  * et
                   )
{
const SpiceInt lenFN = 1025;
SpiceChar spkFilename[1025];
const SpiceInt ND = 2;
const SpiceInt NI = 6;
SpiceDouble dc[ND];
SpiceInt ic[NI];
#define lTarget ((long)ic[0])
#define lCenter ((long)ic[1])
char* outFilename = getenv("BTC_LOG_SPKPVN");
FILE* outFile;

   if (!outFilename) return;

   chkin_c ( "btclogspkpvn_");

   /* Get SPK filename from DAF handle */
   dafhfn_((integer*)handle, (char*)spkFilename, (ftnlen) (lenFN-1));
   F2C_ConvertStr ( lenFN, spkFilename );

   /* Unpack summary descriptor to get target and center bodies */
   dafus_c(descr, ND, NI, dc, ic);

   /* Open file for append, log SPKPVN call, close file */
   outFile = fopen(outFilename, "a");
   fprintf(outFile, "%s %ld %.0lf %ld\n", spkFilename, lTarget, *et, lCenter);
   fclose(outFile);

   chkout_c ( "btclogspkpvn_");
}
