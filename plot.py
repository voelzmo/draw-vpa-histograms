import matplotlib.pyplot as plt
import sys, getopt

# start, end and growth values taken from https://github.com/kubernetes/autoscaler/blob/2542e8c884a8e25634d3b8f43243fa8706007f30/vertical-pod-autoscaler/pkg/recommender/model/aggregations_config.go#L81-L102
CPU_START_BUCKET=0.01
CPU_END_BUCKET=1000.0
MEMORY_START_BUCKET=1e7
MEMORY_END_BUCKET=1e12
BUCKET_GROW_FACTOR=0.05

def main(argv):
  resource = ''
  try:
    opts, args = getopt.getopt(argv,"hr:",["help","resource="])
  except getopt.GetoptError as e:
    print(f'Error: {e}')
    print('Usage: plot.py --resource <cpu|memory> <bucket weight data>')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
       print('Usage: plot.py --resource <cpu|memory> <bucket weight data>')
    elif opt in ("-r", "--resource"):
      if arg not in ("cpu", "memory"):
        print('Error: resource has to be one of \'cpu\' or \'memory\'')
        sys.exit(2)
      resource = arg
  
  startBucket = ''
  endBucket = ''
  resource_unit = ''
  unit_factor = ''
  # setup bucket labels, so we know which buckets means which value
  if resource == 'memory':
    startBucket = MEMORY_START_BUCKET
    endBucket = MEMORY_END_BUCKET
    resource_unit = "MiB"
    unit_factor = 1e6
  
  elif resource == "cpu":
    startBucket = CPU_START_BUCKET
    endBucket = CPU_END_BUCKET
    resource_unit = "mCores"
    unit_factor = 1e-3
  
  # calculate the bucket starting points according to https://github.com/kubernetes/autoscaler/blob/f3242d8485ab3d53a6ac3fbe430918408295a8cf/vertical-pod-autoscaler/pkg/recommender/util/histogram_options.go#L131-L134
  i = 1
  b = startBucket
  outBuckets = {}
  outBuckets[1]=startBucket
  ratio=1+BUCKET_GROW_FACTOR
  while b < endBucket:
      i += 1
      b = startBucket*((ratio**i)-1)/(ratio-1)
      outBuckets[i] = b

  xLabels = []
  for bucket in outBuckets:
      xLabels.append(f'{outBuckets[bucket]/unit_factor:.4f} {resource_unit}')
  
  # get bucketWeights data from stdin:
  bucketWeights = eval(''.join(sys.stdin.readlines()).strip("\n"))
  sortedBucketWeightKeys = sorted(bucketWeights, key=int)

  # create an array 'w' where w[bucketIndex] = heightOfBar
  w = [0] * outBuckets.__len__()
  lowestBucketFilled = int(sortedBucketWeightKeys[0])
  highestBucketFilled = 0
  for key in sortedBucketWeightKeys:
    w[int(key)] = bucketWeights[key]
    highestBucketFilled = int(key)
  
  # plot:
  fig, ax = plt.subplots()
  
  # only draw the interesting range between 'lowestBucketFilled' and 'highestBucketFilled'
  ax.bar(xLabels[lowestBucketFilled:highestBucketFilled+1], w[lowestBucketFilled:highestBucketFilled+1])
  plt.xticks(rotation = 45)
  plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])