#!usr/bin/env python3
# Producer/Consumer experiment - extended
# by Hawk Weisman

import csv
from timeit import timeit
from datetime import datetime

filename = "lrgexperiment " + str(datetime.now()).replace('/', '-') + ".csv" 

consumerNumbers = [2,4,6,8,10,12]
dataNumbers = [10,100,1000,3000,5000,7000,10000]

with open(filename, 'w') as csvfile:

	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["consumers", "data", "replicate", "time"])

	for data in dataNumbers:
		for consumers in consumerNumbers:
			args = "\\\"-Dargs=\\\"-c {c!s} -i {d!s} \\\"\\\"".format(c = consumers, d = data)
			call = "subprocess.call([\"ant\", \"run\", \"{args}\"])".format(args=args)
			for i in range(1, 5):
				print ("Running experiment with {c} consumers and {d} data items, replicate {r}".format(c = consumers, d = data, r = i))
				csvwriter.writerow([consumers,data,i,timeit(stmt=call, setup="import subprocess", number=1)])

csvfile.close()