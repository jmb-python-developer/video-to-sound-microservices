## MySQL Database (Kubernetes)

This folder contains the necessary files, and instructions, to create a MySQL database in Kubernetes.
Even if the K8s architecture is the target, the configurations and files could be spin up in a Minikube cluster locally as well.

*To access the MySQL service running in the K8s pod, the following command can be executed, which will allow to
use the pod's shell environment:

`kubectl exec deployment/mysql -it -- /bin/bash`

Then log in with the MySQL dummy credentials, like so:

`mysql -u auth_user -p`

Dummy password: Auth123

**Important**

The 'auth_service' service (and related project) contains the `init.sql` script that has to be executed before using the dummy 
password of above, the script will do the following:

- Create the 'auth_user' user
- Create the service's tables
- Grant the necessary privileges to the 'auth_user' over the tables created.
