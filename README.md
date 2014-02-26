python-stlsplitter
==================

STL file splitter and binary/ascii read/write library for Python

# STL Splitter

This is a small tool that recognizes when an stl file contains separate objects (plate) and writes them out as separate files

Usage:

    ./stlSplitter.py <file.stl>
    
The output format is file-1.stl file-2.stl etc.

# stlRW

This is a library for input/output of ascii and binary STL files. it implements the following functions:

    header, points, normals, v1, v2, v3, isAscii = stlRead(stl_filename)

reads an STL file, automatically recognizing if it is binary or ascii. Returns the header (unimplemented), an array containing all the points, an array containing all the normals, three arrays containing the vertices of the triangles and a boolean variable identifying if the read file was ASCII. The library has two specialized forms of this function, with the same syntax: ```stlReadAscii``` and ```stlReadBinary```.

    stlWrite(fname, normals, v1, v2, v3, isAscii=False)

writes an STL file, accepting the same parameters as the output of the above functions. There are two specialized versions that can be called directly: ```stlWriteAscii``` and ```stlWriteBinary```.

The code of this library is partly based on https://github.com/cmpolis/convertSTL by Chris Polis and https://github.com/sukhbinder/python by Sukhbinder Singh
   
