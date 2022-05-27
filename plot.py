import matplotlib.pyplot as plt
import sys

# get memoryWeights data from stdin:
memoryWeights = eval(''.join(sys.stdin.readlines()).strip("\n"))

# setup bucket labels, so we know which buckets means which memory size
# start, end and growth values taken from https://github.com/kubernetes/autoscaler/blob/2542e8c884a8e25634d3b8f43243fa8706007f30/vertical-pod-autoscaler/pkg/recommender/model/aggregations_config.go#L93-L102
startBucket=1e7
endBucket=1e12
growFactor=0.05
i = 1
b = startBucket
outBuckets = {}
while b < endBucket:
    outBuckets[i]=b
    b = b*(1+growFactor)
    i += 1

xLabels = []
for bucket in outBuckets:
    xLabels.append(f'{outBuckets[bucket]/1e6:.2f} MiB')

# create an array 'w' where w[bucketIndex] = heightOfBar
w = [0] * outBuckets.__len__()
lowestBucketFilled = int(list(memoryWeights.keys())[0])
highestBucketFilled = 0
for key in memoryWeights:
  w[int(key)] = memoryWeights[key]
  highestBucketFilled = int(key)-1

# plot:
fig, ax = plt.subplots()

# only draw the interesting range between 'lowestBucketFilled' and 'highestBucketFilled'
ax.bar(xLabels[lowestBucketFilled:highestBucketFilled], w[lowestBucketFilled:highestBucketFilled])
plt.xticks(rotation = 45)
plt.show()