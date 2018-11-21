
"""
Computes a histrogram for the 9th layer of pretrained AlexNet, that computes 256 convolutions resulting 
in a layer of size 256x13x13.
We have computed the first 12k eigenvalues "exactly" using ARPACK

Small spikes have been amplified in amplitude for visual clarity
"""
import numpy as np
import sys
import json
import re
print(sys.argv)
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
output = []
iteration = 0

name = [ int(c) for c in re.split('([0-9]+)', sys.argv[1]) if c.isdigit()][-1]

for f in sorted_nicely(sys.argv[1:]):
	data = np.genfromtxt(f,delimiter=",")
	specialFirstBar = False

	bins=data[:,0].flatten()
	weights=data[:,1].flatten()
	numBins = data.shape[0]
	step = bins[1]
	if specialFirstBar:
		step = bins[6]-bins[5]
	weightsA = numBins * [0]
	weightsB = numBins * [0]
	x=0
	for i in range(numBins-1,-1,-1):
		# print(i)
		if x+weights[i]<=1000:
			x+=weights[i]
			weightsB[i] = weights[i]
			weightsA[i] = 0
		elif x>=1000:
			weightsA[i] = weights[i]
		elif x+weights[i]>1000:
			weightsA[i] = weights[i]
			#weightsB[i] = 1000-x
			#weightsA[i] = weights[i]-weightsB[i]
			x=1000
	# for i in range(numBins):
	# 	if weightsB[i]>0:
	# 		print(100/(weightsB[i]**0.8))
	# 		weightsB[i]*=100/(weightsB[i]**0.8)


	secondLargest = max(weights[1:])
	sizeHeuristic = 1.25 if secondLargest/weights[0]>0.1 else 3.5
	ticks=[float("{0:.2f}".format(x)) for x in bins[::numBins//10]]+[float("{0:.2f}".format(x)) for x in [bins[-1]+step]]
	j = {
		"name":"Epoch "+str(iteration),
		"data": [{"bin": j, "count": weights[i]} for i,j in enumerate(bins)],
		"ticks" : ticks
		}
	output.append(j)
	iteration+=1
json.dump(output,open("data{}.json".format(name),"w"),indent=2)