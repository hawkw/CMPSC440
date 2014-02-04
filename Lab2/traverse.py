#! usr/bin/env python3.3

"""
traverse.py
by Hawk Weisman
for CMPSC440 at Allegheny College

Tool to recursively traverse a filesystem and collect data on 
characteristics such as size, age, et cetera.

Usage: 
	traverse.py (DIRECTORY) [--size] [--links] [--histogram] [--verbose]

Arguments:
	DIRECTORY 			Root directory from which to begin traversal.

Options:
	--histogram, -h		Make a histogram
	--verbose			Verbose mode execution
	--size, -s 			Analyze file size
	--age, -a 			Analyze file age
	--links, -l 		Analyze file link count

"""
from hurry.filesize import size as filesize
import os, numpy, math
from scipy import stats
from matplotlib import pyplot, mlab
from docopt import docopt
from stat import *

def mean(l):
    """Returns the arithmetic mean of list l, as a float"""
    return sum(l) / len(l)

def traverse(path):
	"""Traverses the filesystem starting at path"""
	filesystem = {}
	_traverse(path,filesystem)
	return filesystem


def _traverse(path, files):
	"""Helper traversal function"""

	for item in os.listdir(path):

		# get the path to the current item
		itempath = os.path.join(path, item)	

		if arguments['--verbose']:
			print(itempath)
		
		# os.lstat() does not follow symlinks; we are not 
		try:
			files[itempath] = os.lstat(itempath)											
		except IOError:								
			print("failed to get information about ", itempath)
		else:
			# check if the stat-ed item is a directory, and if it is, recurse
			if S_ISDIR(files[itempath].st_mode):			
				_traverse(itempath,files)			

def size(filesystem):
	"""Perform analyses related to file size"""
	bytesizes = [value.st_size for value in filesystem.values() if value.st_size > 0]

	if arguments['--verbose']:
		for value in sorted(bytesizes):
			print("Found a %s file" % filesize(value))

	print("Average file size:\t%s" % filesize(mean(bytesizes)))
	print("Maximum file size:\t%s" % filesize(max(bytesizes)))
	print("Minimum file size:\t%s\n" % filesize(min(bytesizes)))



	if arguments['--histogram']:

		density = stats.gaussian_kde(bytesizes)
		density.covariance_factor = lambda : .25
		density._compute_covariance()

		n, bins, patches = pyplot.hist(bytesizes, bins=50, log=True, normed=True, histtype='step')
		#pyplot.plot(xgrid, density(xgrid), 'r-')

		pyplot.xlabel('File size (bytes)\nLogarithmic')
		pyplot.ylabel('Frequency')
		pyplot.title('Histogram of file sizes')
		pyplot.show()

def links(filesystem):
	"""Perform analyses related to file link count"""
	linkcount = []

	for key, value in filesystem.items():
		linkcount.append(value.st_nlink)

	print("Average link count:\t%s" % mean(linkcount))
	print("Maximum link count:\t%s" % max(linkcount))
	print("Minimum link count:\t%s\n" % min(linkcount))

	if arguments['--histogram']:

		pyplot.hist(linkcount, bins=50, log=True)
		pyplot.xlabel('Number of links')
		pyplot.ylabel('Frequency')
		pyplot.title('Histogram of link counts')
		pyplot.show()		

if __name__ == '__main__':
    arguments = docopt(__doc__, version='traverse.py 0.2')

    filesystem = traverse(arguments["DIRECTORY"])

    if arguments['--size']:
    	size(filesystem)

    if arguments['--links']:
    	links(filesystem)
