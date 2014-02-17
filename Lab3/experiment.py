#!usr/bin/env python3
# Producer/Consumer experiment
# by Hawk Weisman

import csv
from timeit import timeit
from datetime import datetime

filename = "experiment " + str(datetime.now()) + ".csv" 

consumerNumbers = [n for n in range(4,10)]
dataNumbers = [n for n in range(1000,10100) if n % 100 == 0]

with open(filename, 'w') as csvfile:

	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["consumers", "data", "time"])

	for consumers in consumerNumbers:
		for data in dataNumbers:
			args = "\\\"-Dargs=\\\"-c {c!s} -i {d!s}\\\"\\\"".format(c = consumers, d = data)
			call = "subprocess.call([\"ant\", \"run\", \"{args}\"])".format(args=args)
			for i in range(1, 10):
				csvwriter.writerow([consumers,data,timeit(stmt=call, setup="import subprocess")])
				#print call

csvfile.close()