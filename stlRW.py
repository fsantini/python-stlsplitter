# STL reader-writer
#
# copyright 2014 Francesco Santini <francesco.santini@gmail.com>
#
# based on https://github.com/cmpolis/convertSTL by Chris Polis
# and BinarySTL https://github.com/sukhbinder/python by Sukhbinder Singh
#
# Released under the MIT/X license

import numpy as np
from struct import unpack, pack

def stlReadBinary(fname):
  fp = open(fname, 'rb')
  Header = fp.read(80)
  nn = fp.read(4)
  Numtri = unpack('i', nn)[0]
  #print nn
  record_dtype = np.dtype([
                  ('normals', np.float32,(3,)),  
                  ('Vertex1', np.float32,(3,)),
                  ('Vertex2', np.float32,(3,)),
                  ('Vertex3', np.float32,(3,)) ,              
                  ('atttr', '<i2',(1,) )
  ])
  data = np.fromfile(fp , dtype = record_dtype , count =Numtri)
  fp.close()

  Normals = data['normals']
  Vertex1= data['Vertex1']
  Vertex2= data['Vertex2']
  Vertex3= data['Vertex3']

  p = np.append(Vertex1,Vertex2,axis=0)
  p = np.append(p,Vertex3,axis=0) #list(v1)
  Points =np.array(list(set(tuple(p1) for p1 in p)))
  
  return Header,Points,Normals,Vertex1,Vertex2,Vertex3,False

def stlReadAscii(fname):
  fp = open(fname, 'r')
  Normals = []
  Vertex1 = []
  Vertex2 = []
  Vertex3 = []
  Points = []
  while True:
    line = fp.readline()
    if not line: break
    if line.find("solid") > -1 or line.find("endfacet") > -1: continue
    if line.find("facet normal") > -1:
      normline = line[line.find("facet normal")+len("facet normal"):]
      normal = np.array([float(val.strip()) for val in normline.split()])
      Normals.append(normal)
      vertices = []
      fp.readline() # outer loop
      # read vertices after normal
      for vIndex in range(0,3):
        vLine = fp.readline()
        vLine = vLine[vLine.find("vertex")+len("vertex"):]
        vertices.append(np.array([float(val.strip()) for val in vLine.split()]))
      Vertex1.append(vertices[0])
      Vertex2.append(vertices[1])
      Vertex3.append(vertices[2])
      Points.extend(vertices)
      fp.readline() # endloop
  return "", Points, Normals, Vertex1, Vertex2, Vertex3,True
    
  
def stlRead(fname):
  fp = open(fname, "r")
  if fp.readline().find("solid") > -1:
    fp.close()
    return stlReadAscii(fname)
  else:
    fp.close()
    return stlReadBinary(fname)
    
def stlWriteBinary(fname, normals, v1, v2, v3):
  with open(fname, "wb") as fout:
    # write 80 bytes header
    for i in range(0, 80): fout.write(pack("<c", " "))
    fout.write(pack("<I", len(normals))) # number of triangles
    for i in range(0, len(normals)):
      fout.write(pack("<fff", *normals[i]))
      fout.write(pack("<fff", *v1[i]))
      fout.write(pack("<fff", *v2[i]))
      fout.write(pack("<fff", *v3[i]))
      fout.write(pack("<H", 0)) # attribute
      
def writeVector(fd, vec):
  for v in vec:
    fd.write("{:.7e}".format(v))
    fd.write(" ")
      
def stlWriteAscii(fname, normals, v1, v2, v3):
  with open(fname, "w") as fout:
    fout.write("solid \n")
    for i in range(0, len(normals)):
      fout.write("  facet normal ")
      writeVector(fout, normals[i])
      fout.write("\n")
      fout.write("    outer loop\n")
      fout.write("      vertex ")
      writeVector(fout, v1[i])
      fout.write("\n")
      fout.write("      vertex ")
      writeVector(fout, v2[i])
      fout.write("\n")
      fout.write("      vertex ")
      writeVector(fout, v3[i])
      fout.write("\n")
      fout.write("    endloop\n")
      fout.write("  endfacet\n")
      
      
def stlWrite(fname, normals, v1, v2, v3, isAscii=False):
  if isAscii:
    stlWriteAscii(fname, normals, v1, v2, v3)
  else:
    stlWriteBinary(fname, normals, v1, v2, v3)
# test
if __name__ == "__main__":
  import sys
  fname = sys.argv[1]
  h,p,n,v1,v2,v3,isAscii = stlRead(fname)
  print len(n)
  print v1[0]
  stlWriteBinary("binary.stl", n, v1, v2, v3);
  stlWriteAscii("ascii.stl", n, v1, v2, v3);