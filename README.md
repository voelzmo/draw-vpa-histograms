# Usage
This script expects the `bucketWeights` section of a VPA object as input on `stdin`.
```
$ kubectl get verticalpodautoscalercheckpoints.autoscaling.k8s.io my-fancy-vpa-checkpoint -o json | jq -r '.status.memoryHistogram.bucketWeights' | python ./plot.py
```

And prints you a nice bar chart like this

<img width="1067" alt="Screenshot 2022-05-27 at 17 03 26" src="https://user-images.githubusercontent.com/2256887/170726322-97010770-81cb-4987-a215-d91937f39791.png">

Note: the y-axis is still normalized, this means the values are not actual occurrences, but the highest bucket will always be listed as `1000`.
