## MongoDB Database (Kubernetes )

This folder contains the necessary files, and instructions, to create a MongoDB database in Kubernetes.
Even if the K8s architecture is the target, the configurations and files could be spin up in a Minikube cluster locally as well.

Kubernetes stores the content of all secrets in a base 64 encoded format. If you want to see how your string will appear in a base64 format, execute the following.

`echo "secret" | base64` 

//after encoding it, this becomes c2VjcmV0Cg==

If you want to decode a base64 string. Run

`echo "c2VjcmV0Cg==" | base64 --decode`

//after decoding it, this will give "secret".

### StatefulSet or Deployment?

Here, in this example we are deploying a standalone MongoDB instance, therefore – we can use a deployment object. This is because only one pod will be spun up.

### Mongo Shell (through mongodb-client) can be used with cmds such as:

To avoid exposing the service by forwarding the port in K8s, the following command can be executed to log into
the pod's shell environment:

`kubectl exec deployment/mongo-db -it -- /bin/bash`


_Then once inside the pod's shell environment, use the mongodb shell by typing_ and authenticating at the same time: 

`mongosh -u adminuser -p password123`

`show dbs`

`use [db_name]`

`show collections`

Then to insert raw data from shell, i.e.:

`db.[collection].insert({name: "devopscube" })`

And, to find data:

`db.[collection].find()`

To remove all data from a collection:

`db.fs.files.remove({})`

In this case, it's removing files from GridFS mongo component, `{}` indicated no criteria for removal query, which defaults to deleting all.

