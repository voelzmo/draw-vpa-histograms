# What is this?
Ever wondered what the values in a VerticalPodAutoscalerCheckpoint even mean?

As a human it is hard to understand this

```json
{
  "apiVersion": "autoscaling.k8s.io/v1",
  "kind": "VerticalPodAutoscalerCheckpoint",
  "metadata": {
    "creationTimestamp": "2020-07-24T02:08:41Z",
    "name": "my-vpa-checkpoint",
    "namespace": "default"
  },
  "spec": {
    "containerName": "my-container",
    "vpaObjectName": "my-container-vpa"
  },
  "status": {
    "firstSampleStart": "2020-07-22T04:46:22Z",
    "lastSampleStart": "2022-05-27T15:11:24Z",
    "lastUpdateTime": "2022-05-27T15:11:47Z",
    "memoryHistogram": {
      "bucketWeights": {
        "2": 38,
        "35": 1,
        "36": 1,
        "37": 2,
        "38": 55,
        "39": 704,
        "40": 3788,
        "41": 10000,
        "42": 5422,
        "43": 2923,
        "44": 402,
        "45": 32,
        "46": 5212,
        "47": 1,
        "48": 7
      },
      "referenceTimestamp": "2022-05-28T00:00:00Z",
      "totalWeight": 6.673685189638553
    },
    "totalSamplesCount": 650223,
    "version": "v3"
  }
}
```
but much easier to grasp what's going on by looking at a picture!

# Usage
This script expects the `bucketWeights` section of a VerticalPodAutoscalerCheckpoint object as input on `stdin`.
```
$ kubectl get verticalpodautoscalercheckpoints.autoscaling.k8s.io my-vpa-checkpoint -o jsonpath={.status.memoryHistogram.bucketWeights} | python ./plot.py --resource=memory
```

And prints you a nice bar chart like this

<img width="2118" alt="Screenshot 2022-11-04 at 09 54 45" src="https://user-images.githubusercontent.com/2256887/199932881-5322653a-1258-4d40-beae-f07d7899bb2c.png">

CPU histograms now supported as well:
```
$ kubectl get verticalpodautoscalercheckpoints.autoscaling.k8s.io my-vpa-checkpoint -o jsonpath={.status.cpuHistogram.bucketWeights} | python ./plot.py --resource=cpu
```

Note: the y-axis is still normalized, this means the values are not actual occurrences, but the highest bucket will always be listed as `10000`.

# Requirements

This script requires python 3 and `matplotlib` installed.