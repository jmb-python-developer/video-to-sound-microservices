## Notification Service

This microservice is fundamentally a RabbitMQ consumer and has, as its core, the following functionalities

- Listens to and when messages are present reads from the 'mp3' queue the messages for video converted by the 'Converted Microservice'
- With the _fid_ (file id) of the mp3 file and an app's username (email used for authenticating with the app), both present in the message read, sends an email to the user notifying said user that the file is ready for download.

### Local Run Requirements

To be able to run this service, a SMTP server needs to be used. This can either be one's personal SMTP server, or, a email provider like in this service example: Outlook.com.
<br/>

To test locally the following has to be done:

- Change the Kubernetes K8s secrets file (`manifests/secret.yaml`), add a dummy email credentials serving as the SMTP server, and push to a docker repository owned. 
- Then deploy the service and all manifest files in a Kubernetes supported cluster (i.e. minikube)

