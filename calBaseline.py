#!/usr/bin/env python

import ROOT
import math
import argparse
import os

def calculateBaseline( wf ):
  
  v = 0.
  v2 = 0.
  n = wf.GetNbinsX()
  # print 'n: %d' %n
  
  for i in xrange(1, n+1 ):
    vi = wf.GetBinContent(i)
    v += vi
    v2 += vi*vi
  v /= float(n)
  v2 /= float(n)
  rms = math.sqrt( max (v2-v*v, 0))
  # print 'baseline: %f' % v
  # print 'rms:      %f' % rms

  return v, rms

# def calculateBaseline()

# def makePlot():

# def makePlot()


if __name__ == "__main__":
  
  parser = argparse.ArgumentParser( description = 'Check the baseline and RMS' )
  parser.add_argument( '-i', dest = 'inFile', type = str, help = 'Input file name.' )
  parser.add_argument( '-o', dest = 'outDir', type = str, help = 'Output file directory.' )
  parser.add_argument( '-n', dest = 'nEvents', type = int, help = 'Number of events to process.' )
  
  args = parser.parse_args()
  
  if not os.path.exists( args.outDir ):
    os.makedirs( args.outDir )

  DACOffset1 = [ 0xFFFF, 0x0000, 0x9000, 0xC010, 0xA010, 0x9010, 0xC100, 0xA100, 0xA100 ]
  DACOffset2 = [ 0xF000, 0xD000, 0xC000, 0xF010, 0xD010, 0xC010, 0xF100, 0xD100, 0xC100 ]

  outFilename = '%s/Baseline.txt' % args.outDir
  nEvents = args.nEvents
  nBoards = 9
  nFragments = 1
  nChannels = 64
  
  baseline = {}
  rms = {}
  
  f = ROOT.TFile( args.inFile )
  
  for iEvent in xrange( 1, nEvents ):
    for iFragment in xrange ( 0, nFragments ):
      for iBoard in xrange( 0, nBoards ):
        h = f.Get( 'view/h_%d_%d_%d' % ( iEvent, iFragment, iBoard ) )
        
        for iChannel in xrange( 0, nChannels ):
          print 'Processing Event %d, Fragment %d, Board %d, Channel %d...' %( iEvent, iFragment, iBoard, iChannel )
          wf = h.ProjectionY( 'Channel%02d' % iChannel, iChannel+1, iChannel+1 )
          
          key = '%d_%d_%d_%d' % ( iEvent, iFragment, iBoard, iChannel )
          baseline[key], rms[key] = calculateBaseline( wf )
          
  outFile = open( outFilename, 'w' )
  outFile.write( '            ')
  for iBoard in xrange( 0, nBoards ):
    outFile.write( 'Board %d  ' % iBoard )
  outFile.write( '\n' )
  outFile.write( 'DACOffset1  ' )
  for iBoard in xrange( 0, nBoards ):
    value = DACOffset1[iBoard]*4096./65536.
    outFile.write( '%4.2f  ' % value )
  outFile.write( '\n\n' )

  for iChannel in xrange( 0, nChannels ):
    if iChannel == 32:
      outFile.write( '\nDACOffset2  ' )
      for iBoard in xrange( 0, nBoards ):
        value = DACOffset2[iBoard]*4096./65536.
        outFile.write( '%4.2f  ' % value )
      outFile.write( '\n\n' )
    outFile.write( 'Channel %02d  ' % iChannel )
    for iBoard in xrange( 0, nBoards ):
      key = '1_0_%d_%d' % ( iBoard, iChannel )
      outFile.write( '%4.2f  ' % baseline[key] )
    outFile.write( '\n' )
