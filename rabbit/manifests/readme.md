## RabbitMQ Broker (Kubernetes)

###Connecting locally to RabbitMQ

<br>

Normally, the following should work:

1- Edit /etc/hosts and add

`127.0.0.1 rabbitmq-manager.com`

2- Start Minikube tunneling

`minkube tunnel`

*If that doesn't work, then try:*

`kubectl port-forward rabbitmq-0 15672:15672`

And head to the address:

`localhost:15672`