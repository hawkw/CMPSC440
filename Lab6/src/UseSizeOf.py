#!usr/bin/env python3.3
# UseSizeOf.py
# by Hawk Weisman
# for CMPSC440 Lab 6
# at Allegheny College
#
# Determines the size of various Python data types.

import sys

class Int2D:
	"""Represents a point on a 2D plane with integer precision"""
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

class Int3D:
	"""Represents a point on a 3D plane with integer precision"""
	def __init__(self, x, y, z):
		self.x = int(x)
		self.y = int(y)
		self.z = int(z)

class Float2D:
	"""Represents a point on a 2D plane with floating-point precision"""
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

class Float3D:
	"""Represents a point on a 3D plane with floating-point precision"""
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)	

bits = lambda bytes: bytes * 8

def main():

	if (len(sys.argv) > 1) and (sys.argv[1] is "--tex" or "-t"):
		tex_mode = True
	else:
		tex_mode = False

	print("{:<12s}{:>8s}{:>8s}\n{:<12s}{:>8s}{:>8s}".format("data type",
	      											 "bytes",
				      								 "bits",
				      								 "---- ----",
				      								 "-----",
				      								 "----" )
		)

	makeLine(int(), tex_mode)
	makeLine(float(), tex_mode)
	makeLine(complex(), tex_mode)
	makeLine(object(), tex_mode)
	makeLine(Int2D(0,0), tex_mode)
	makeLine(Int3D(0,0,0), tex_mode)
	makeLine(Float2D(0,0), tex_mode)
	makeLine(Float3D(0,0,0), tex_mode)

def makeLine(target, tex_mode):
	if tex_mode is True:
		print("{:<12s} & {:6d} & {:6d} \\\\".format(type(target).__name__,
      											  sys.getsizeof(target),
      											  bits(sys.getsizeof(target)))
			)
	else:
		print("{:<12s}{:8d}{:8d}".format(type(target).__name__,
		      							 sys.getsizeof(target),
		      							 bits(sys.getsizeof(target)))
			)

if __name__ == "__main__":
	main()
