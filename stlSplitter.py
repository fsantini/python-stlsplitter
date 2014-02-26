#!/usr/bin/env python
# STL splitter
# splits a STL file containing separate objects
#
# copyright 2014 Francesco Santini <francesco.santini@gmail.com>
#
# based on https://github.com/cmpolis/convertSTL by Chris Polis
# and BinarySTL https://github.com/sukhbinder/python by Sukhbinder Singh
#
# Released under the MIT/X license


import stlRW
import sys
from os import path

## functions

# maybe insert a tolerance for floating points?
def check_connection(tri1, tri2):
  for v1 in tri1[0:2]:
    for v2 in tri2[0:2]:
      if (v1[0] == v2[0] and v1[1] == v2[1] and v1[2] == v2[2]): return True
  return False
    

if len(sys.argv) < 2:
  print "Usage: " + sys.argv[0] + " <file.stl>"
  sys.exit(-1)

fname = sys.argv[1]

print "Reading..."

head,points,n,v1,v2,v3,isAscii = stlRW.stlRead(fname)

print "Analyzing..."

faceTree = []

for triangleIndex in range(0, len(v1)):
  triangle = [ v1[triangleIndex], v2[triangleIndex], v3[triangleIndex], n[triangleIndex] ]
  connectedTo = []
  for treeindex in range(0, len(faceTree)):
    for face in faceTree[treeindex]:
      if check_connection(face, triangle):
        connectedTo.append(treeindex) # the triangle is connected to at least one triangle of the current treeIndex
        break
      
  if len(connectedTo) == 0:
    # this is a triangle from a new set
    #print "new set"
    faceTree.append([])
    faceTree[len(faceTree)-1].append(triangle)
  elif len(connectedTo) == 1:
    #print "existing set"
    # the triangle is connected to one set
    faceTree[connectedTo[0]].append(triangle)
  else:
    #print "connecting triangle"
    #this triangle connects two branches of the tree: collapse the branches
    faceTree[connectedTo[0]].append(triangle)
    for i in range(len(connectedTo)-1, 0, -1):
      faceTree[connectedTo[0]].extend(faceTree.pop(connectedTo[i]))
      
print "Number of separate objects: ", len(faceTree)

print "Writing files"

origFile, origExt = path.splitext(fname)
for i in range(0, len(faceTree)):
  newFile = origFile + "-" + str(i+1) + origExt
  print "Writing ", newFile
  n = [field[2] for field in faceTree[i]]
  v1 = [field[0] for field in faceTree[i]] 
  v2 = [field[1] for field in faceTree[i]] 
  v3 = [field[2] for field in faceTree[i]]
  stlRW.stlWrite(newFile, n, v1, v2, v3)