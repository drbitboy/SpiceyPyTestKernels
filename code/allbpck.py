"""
Usage:

    rm -f earth_031228_231229_predict.xpc allbpck.bpc
    toxfr ../earth_031228_231229_predict.bpc earth_031228_231229_predict.xpc
    python allbpck.py
    tobin allbpck.xpc

Notes:

    XPC_KERNEL:  character string; binary PCK in transfer format

    PAIR_TIMES:  double; (left, right) ET confinement window pairs to
                 extract a limited set of Type 2 PCK records from
                 segments in XPC_KERNEL

    DEBUG:       Set non-blank to turn on additional debugging

\begindata
  XPC_KERNEL = 'earth_031228_231229_predict.xpc'
  PAIR_TIMES = ( @2003-OCT-13-00:00   @2003-OCT-13-12:00
                 @2006-NOV-08-00:00   @2006-NOV-10-00:00
                 @2007-MAY-03-00:00   @2007-MAY-04-00:00
               )
\begintext

Move DEBUG assignment below to just before \begintext line to log more output
information:

  DEBUG  = 'True'

"""
import os
import sys
import spiceypy as spice
from spiceypy.utils import support_types as stypes

# Convenience lambdas
l2d = lambda L: spice.hx2dp(eval(L))
d2s = lambda d: '{}'.format(spice.dp2hx(d))
l2i = lambda L: int(l2d(L))

# String constants
tick = "'"
crlf = "\r\n"

doDebug = False

########################################################################
class TotalArraysFound(Exception):
    def __init__(self, totalArraysLine, totalArrays):
        super(TotalArraysFound, self).__init__('Found [{}]'.format(totalArraysLine.rstrip(crlf)))
        self.totalArrays = totalArrays


########################################################################
class XpcRecord(object):
    """
    Binary PCK Type 2 Record in segment, from ARRAY in XPC file
    """
    def __init__(self, Ls, idx):
        self.recordLines = Ls
        self.index = idx
        midpoint, radius = map(l2d, self.recordLines[:2])
        self.window = stypes.SPICEDOUBLE_CELL(2)
        spice.scard(0, self.window)
        spice.wninsd(midpoint-radius, midpoint+radius, self.window)


    def inWindow(self, confinementWindow):
        """
        Return True if record window intersects the confinement window
        argument, else return False
        """
        return 0 < spice.wncard(spice.wnintd(self.window, confinementWindow))


########################################################################
class XpcSegment(object):
    """
    One DAF segment, represented by ARRAY in XPC file
    """
    def __init__(self, fIn=False):
        self.ok = False
        self.arrayWordCount = 0
        self.records = []
        self.segmentLines = []
        if fIn:
            fR = fIn.readline
            # First line of array ...
            firstLine = fR()
            # Get line terminator
            firstLineRStripped = firstLine.rstrip(crlf)
            self.lineTerm = firstLine[len(firstLineRStripped):]
            toks = firstLineRStripped.split()
            try:
                # ... must be [BEGIN_ARRAY n count], or ...
                assert 3 == len(toks)
                assert 'BEGIN_ARRAY' == toks[0]
            except:
                # ... must be [TOTAL_ARRAYS n]
                assert 2 == len(toks)
                assert 'TOTAL_ARRAYS' == toks[0]
                totalArrays = int(toks[1])
                raise TotalArraysFound(firstLine, totalArrays)
            # Get array number and length from [BEGIN_ARRAY n count]
            self.arrayNum, self.arrayWordCount = self.arrayInfo = map(int,toks[1:])
            def fNext(rem):
                rtn = fR()
                if not rem:
                    # Argument rem is 0:  stripped line must start and end with a tick
                    assert tick == rtn[0] and tick == rtn.rstrip(crlf)[-1]
                    # Return line only
                    return rtn
                if tick == rtn[0]:
                    # Line starts with a tick; stripped, it must end with a tick
                    assert tick == rtn.rstrip(crlf)[-1]
                    # Return decremented segment item count and line
                    return rem-1, rtn
                # Line does not start with a tick, it must be 1024 if there
                # there are more than 1024 segment items left, else it must
                # be the number of segment items left
                assert (1024 < iRem and '1024' == rtn.rstrip(crlf)) or int(rtn) == iRem
                # Return decremented segment item count and line
                return iRem-1, fNext(0)
            # Get the segment name and the descriptor
            self.sName          = fNext(0)
            # ND == 2
            self.sInitialEpoch  = fNext(0)
            self.sFinalEpoch    = fNext(0)
            # NI==5, NI-2==3; initial and final addresses are not in XFR file
            self.sBody          = fNext(0)
            self.sIrf           = fNext(0)
            self.sType          = fNext(0)
            # Only handle Type 2 PCK records
            assert "'2'" == self.sType.rstrip(crlf)
            # Read lines records, stop at directory
            iRem = self.arrayWordCount
            while iRem > 4:
                iRem, L = fNext(iRem)
                self.segmentLines.append(L)
            assert 4 == iRem
            # Read directory
            iRem, self.sFirstInitialEpoch = fNext(iRem)
            iRem, self.sIntervalLen = fNext(iRem)
            iRem, self.sRecordSize = fNext(iRem)
            iRem, self.sNRecords = fNext(iRem)
            assert iRem is 0
            assert self.sFirstInitialEpoch == self.sInitialEpoch
            # Parse directory items to doubles and ints
            self.firstInitialEpoch = l2d(self.sFirstInitialEpoch)
            self.intervalLen = l2d(self.sIntervalLen)
            self.recordSize = l2i(self.sRecordSize)
            self.nRecords = l2i(self.sNRecords)
            assert (self.arrayWordCount - 4) == (self.recordSize * self.nRecords)
            # Read END_ARRAY
            toks = fR().rstrip(crlf).split()
            assert 3 == len(toks)
            assert 'END_ARRAY' == toks[0]
            assert map(int,toks[1:]) == self.arrayInfo
            # Break lines into records
            for i in range(self.nRecords):
                iFirstWord = i * self.recordSize
                words = self.segmentLines[iFirstWord:iFirstWord+self.recordSize]
                assert len(words) == self.recordSize
                self.records.append(XpcRecord(words,i))
            # Finish
            self.ok = True
            return
        # End of [if fIn:]


    ####################################################################
    def slice(self,confinementWindow,arrayNum):
        currentSegment = False
        returnSegments = []
        # Append records to last segment ...
        for record in self.records:
            # ... but only if record overlaps confinement window
            if record.inWindow(confinementWindow):
                # Initialize a segment if none exists
                if not currentSegment:
                    firstInitialEpoch = record.window[0]
                    sFirstInitialEpoch = d2s(firstInitialEpoch) + self.lineTerm
                    currentSegment = XpcSegment()
                    currentSegment.arrayInfo = [arrayNum, 4]
                    currentSegment.arrayNum = arrayNum
                    currentSegment.arrayWordCount = 4
                    arrayNum += 1
                    currentSegment.firstInitialEpoch = firstInitialEpoch
                    currentSegment.intervalLen = self.intervalLen
                    currentSegment.lineTerm = self.lineTerm
                    currentSegment.nRecords = 0
                    currentSegment.recordSize = self.recordSize
                    currentSegment.sBody = self.sBody
                    currentSegment.sFirstInitialEpoch = sFirstInitialEpoch
                    currentSegment.sInitialEpoch = sFirstInitialEpoch
                    currentSegment.sIntervalLen = self.sIntervalLen
                    currentSegment.sIrf = self.sIrf
                    currentSegment.sName = self.sName
                    currentSegment.sRecordSize = self.sRecordSize
                    currentSegment.sType = self.sType
                    currentSegment.ok = True
                # Update segment with record
                currentSegment.records.append(record)
                currentSegment.sFinalEpoch = d2s(record.window[1]) + self.lineTerm
                currentSegment.arrayInfo[1] += self.recordSize
                currentSegment.arrayWordCount += self.recordSize
                currentSegment.nRecords += 1
                currentSegment.sNRecords = d2s(currentSegment.nRecords) + self.lineTerm
                currentSegment.segmentLines.extend(record.recordLines)
            # If record is not in confinement window, and
            # a current segment exists ...
            elif currentSegment:
                # Finish the segment and add it to the list of segments
                returnSegments.append(currentSegment)
                # Clear the current segment
                currentSegment = False
        return returnSegments, arrayNum


    ####################################################################
    def write(self,fOut):
        fW = fOut.write
        # Beginning of array and descriptor:  Name; ND=3; NI=2=(5-3).
        fW('BEGIN_ARRAY {} {}{}'.format(self.arrayNum, self.arrayWordCount, self.lineTerm))
        fW(self.sName)
        fW(self.sInitialEpoch)
        fW(self.sFinalEpoch)
        fW(self.sBody)
        fW(self.sIrf)
        fW(self.sType)
        # Segment lines:   groups of 1024 lines or less, delimited by
        #                  a line with the lesser of 1024 and remaining
        #                  line count
        iSofar = 0
        nLeft = len(self.segmentLines) + 4
        # Record lines plus directory
        for L in (self.segmentLines +
                  [self.sFirstInitialEpoch,
                   self.sIntervalLen,
                   self.sRecordSize,
                   self.sNRecords]):
            if not (iSofar%1024):
                fW('{}{}'.format(nLeft if nLeft < 1024 else 1024, self.lineTerm))
            fW(L)
            iSofar += 1
            nLeft -= 1
        # End of array
        fW('END_ARRAY {} {}{}'.format(self.arrayNum, self.arrayWordCount, self.lineTerm))


########################################################################
class XpcFile(object):
    def __init__(self,fnIn=False):
        """
        Parse SPICE XFR format from Binary PCK file
        N.B. Type 2 segments only
        """
        self.filename = fnIn if fnIn else False
        self.segments = []
        if not fnIn: return
        with open(self.filename,'rb') as fIn:
            (self.dafetf, self.dafpck, self.nd, self.ni,
             self.iName) = self.first5 = ( fIn.readline(), fIn.readline(),
                                           fIn.readline(), fIn.readline(),
                                           fIn.readline())
            self.lineTerm = self.dafetf[len(self.dafetf.rstrip(crlf)):]
            assert "'2'" == self.nd.rstrip(crlf) and "'5'" == self.ni.rstrip()
            try:
                while True: self.segments.append(XpcSegment(fIn))
            except TotalArraysFound as e:
                assert len(self.segments) == e.totalArrays


    ####################################################################
    def slice(self, confinementWindow, filename='allbpck.xpc'):
        """
        Slice self into a new XpcFile based on a confinement window
        """
        # Create new empty XpcFile
        returnFile = XpcFile()
        returnFile.filename = filename
        # Update file parameters
        (returnFile.dafetf,
         returnFile.dafpck,
         returnFile.nd,
         returnFile.ni,
         returnFile.iName) = returnFile.first5 = self.first5
        # Line terminator
        returnFile.lineTerm = self.lineTerm
        # Initialize array number to one and loop over segments
        nextArrayNum = 1
        for segment in self.segments:
            newSegments, nextArrayNum = segment.slice(confinementWindow, nextArrayNum)
            returnFile.segments.extend(newSegments)
        # Return the XpcFile object
        return returnFile


    ####################################################################
    def write(self,fOut):
        fOut.write('{}{}{}{}{}'.format(*self.first5))
        for segment in self.segments:
            segment.write(fOut)
        fOut.write('TOTAL_ARRAYS {}{}'.format(len(self.segments),self.lineTerm))


########################################################################
if "__main__" == __name__:
    # FURNSH the docstring above as a text kernel,
    # plus any other files on the command line,
    # and put values into kernel pool
    for arg in sys.argv: spice.furnsh(arg)
    # Get pairs of ET endpoints from kernel pool
    pts = list(spice.gdpool('PAIR_TIMES', 0, 100))
    nPETs = len(pts)
    # Set or clear debug flag
    try:
        doDebug = True if spice.gcpool("DEBUG", 0, 1, 999)[0] else False
    except:
        doDebug = False
    # Allocate cell of SpiceDoubles
    pws = stypes.SPICEDOUBLE_CELL(nPETs)
    # Add ET endpoints to cell
    pts.reverse()
    while pts: spice.appndd(pts.pop(),pws)
    # Convert those pairs of ET endpoints into confinement window
    pws = spice.wnvald(nPETs,nPETs,pws)
    assert (spice.wncard(pws) << 1) == nPETs
    pts = list(spice.gdpool('PAIR_TIMES', 0, 100))
    # Get the filename of, and read, the input XFR file
    filename = spice.gcpool("XPC_KERNEL", 0, 1, 999)[0]
    assert filename
    # Read transfer file as XpcFile object
    xpcFileIn = XpcFile(fnIn=filename)
    if doDebug:
        import pprint
        pprint.pprint((vars(xpcFileIn),vars(xpcFileIn.segments[0])))
    # Slice read XpcFile object per confinement window
    xpcFileOut = xpcFileIn.slice(pws)
    if doDebug:
        pprint.pprint((vars(xpcFileOut),vars(xpcFileOut.segments[0])))
    # Write sliced object as SPICE transfer file
    with open(xpcFileOut.filename,'wb') as fOutOut:
        xpcFileOut.write(fOutOut)
