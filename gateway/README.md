## Gateway Service


### Testing the Product
<br>

**Prerequisites**:


- Either the Gateway service is exposed through minikube tunneling (minikube tunnel) in conjunction with adding the address
to the /etc/hosts file (in unix like envs)

- Or, perhaps simpler though not providing the K8s service inherent load balancing capabilities for pods, the port in which the service listens can be "forwarded" in K8s, by running the following command:

`kubectl port-forward gateway-[pod unique K8s ID] 8080:8080`

#### Authentication

The Gateway service communicates with the Authentication service to retrieve a token for the duration of the user's session; which is limited by the token's expiry time (defaulted to 1 day currently in the solution).

The following curl command can be used to retrieve the token:

`curl --location --request POST 'localhost:8080/login' \
--header 'Authorization: Basic anVhbmJydW5vQGdtYWlsLmNvbTpqdWFubQ=='`

_Clarification:_ The Basic authentication links to the credentials used by the Authentication service that reside in the MySQL
database.

Once the command is run, a JWT token is produced, i.e.:

`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imp1YW5icnVub0BnbWFpbC5jb20iLCJleHAiOjE2NzcwODA5NzMsImlhdCI6MTY3Njk5NDU3MywiYWRtaW4iOnRydWV9.Ci84ZPGChfcAM8z78eApGaVm4TGmwEPzY4v204Frfdk`

<br>

#### Uploading a Video File for Conversion

The request to upload a video file for subsequent conversion to MP3 format can be done with the following _curl_ command; bear in mind the video file has to be in the same directory from where the command is executed:

`curl -X POST -F 'file=@./zuck.mp4' -H 'Authorization: Bearer [token]' localhost:8080/upload`

Example:

```
curl -X POST -F 'file=@./zuck.mp4' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpicnVuby5jb2RpbmdAZ21haWwuY29tIiwiZXhwIjoxNjc4NTUyMjc3LCJpYXQiOjE2Nzg0NjU4NzcsImFkbWluIjp0cnVlfQ.vbegStbTNjjJFRy3SkplkYpnzO82ogYi_oazg2oU0BQ' localhost:8080/upload
```

Where "zuck.mp4" is an example for a filename


#### Downloading an MP3 for a converted video file

A token with an active session, just as it's done in the upload operation, has to be used to get download authorization in the application.

Once this is done, the following request, which requires a request parameter with the 'file ID' to download, downloads the file"

```
curl --location --output zuck.mp3 --request GET 'localhost:8080/download?fid=640b5be572f6591b98242d31' --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpicnVuby5jb2RpbmdAZ21haWwuY29tIiwiZXhwIjoxNjc4NTUyMjc3LCJpYXQiOjE2Nzg0NjU4NzcsImFkbWluIjp0cnVlfQ.vbegStbTNjjJFRy3SkplkYpnzO82ogYi_oazg2oU0BQ'
```