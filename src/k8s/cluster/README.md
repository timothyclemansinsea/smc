# Creation and deletion of Kubernetes cluster

## Prerequisite:

Make sure that kubernetes is installed in `~/kubernetes`, downloaded from https://github.com/kubernetes/kubernetes/releases/.  Also gcloud must be setup so you can create/delete instances, etc., from here.

## Creating a k8s cluster

Type `./control.py create -h` for help on creating a cluster.  You can see how much
your cluster will cost per month before creating it:

    ./control.py create test --min-nodes=2 --max-nodes=5 --cost

Now create it, which takes 5-10 minutes:

    ./control.py create test --min-nodes=2 --max-nodes=5

## Switching clusters

You can easily switch between multiple clusters, say `test` and `test2`:

    ./control.py select test2
    # kubectl commands are for test2
    ./control.py select test
    # kubectl commands are for test


## Adjusting autoscaling

You can do this in the GCE web interface easily, or do this

    ./control.py autoscale test --min-nodes=2 --max-nodes=5

You can also force the cluster to have a given size:

    ./control.py resize test --size=2

## Deleting the cluster

    ./control.py delete test

## TODO: Troubleshooting

If you get errors like this when trying to use/connect to pods, it's the firewall:

    Error from server: dial tcp 10.240.0.39:10250: i/o timeout

This happens when the master can't connect to the minion.  The fix is to make a firewal
rule that allows anything with tag k8s-[name]-master to connect to anything with tag k8s-[name]-minion on any port.