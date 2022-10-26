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
  # setup bucket labels, so we know which buckets means which value
  if resource == 'memory':
    startBucket = MEMORY_START_BUCKET
    endBucket = MEMORY_END_BUCKET
    resource_unit = "MiB"
  
  elif resource == "cpu":
    startBucket = CPU_START_BUCKET
    endBucket = CPU_END_BUCKET
    resource_unit = "mCores"
  
  i = 1
  b = startBucket
  outBuckets = {}
  while b < endBucket:
      outBuckets[i]=b
      b = b*(1+BUCKET_GROW_FACTOR)
      i += 1
  
  xLabels = []
  for bucket in outBuckets:
      xLabels.append(f'{outBuckets[bucket]/1e6:.2f} {resource_unit}')
  
  # get bucketWeights data from stdin:
  bucketWeights = eval(''.join(sys.stdin.readlines()).strip("\n"))
  
  # create an array 'w' where w[bucketIndex] = heightOfBar
  w = [0] * outBuckets.__len__()
  lowestBucketFilled = int(list(bucketWeights.keys())[0])
  highestBucketFilled = 0
  for key in bucketWeights:
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