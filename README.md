# ObjectClassification
This branch is a detailed module breakdown

### Client Module
Libraries used:
- **_websockets_**

The client uses **_websocket-client_** to establish connection with the server (23.254.176.188) via 
`HTTP` protocol and listens for the `snap` message from other client. Once `snap` has been received, 
Client returns `True`



### Capture Module
Libraries used: 
- **_requests_**
- **_cv2_**
- **_time_** 

Capture uses **_OpenCV_** for taking a picture from a camera. `cam = cv2.VideoCapture(0)` 
initialises camera at input stream 0. **__Different devices have different camera input index__**

When the camera is being launched, it takes about 2 seconds to load the input picture therefore, 
**_Time_** is used to make a delay  

After the image has been taken, it is being saved to the local storage and has a name `opencv_frame_0.png`
The **_requests_** library is used to make a `PUT` request at `snippets/1/` to the API server.



###Server Module
Libraries used:
- **_websockets_**
- **_asyncio_**
- **_socket_**

Server Module uses **_socket_** only for displaying the IP address of the server. 

**_websockets_** is used for establishing connections with clients and receiving messages.  

**_asyncio_** is used for asynchronous connection with client-server network. A real life example 
is when clients send message simultaneously, the program will not crash.

The script is ran on the server (23.254.176.188) via `systemctl` framework so that the program will run 
forever. `server_echo.py` is ran via `socket.service`

The following commands to be executed via SSH:
- To run `socket.service` forever: `sudo systemctl start socket.service`
- To reload the service files to include the new service: `sudo systemctl daemon-reload`
- To check the status of the service: `sudo systemctl status example.service`
- To enable the service on every reboot: `sudo systemctl enable example.service`
- To disable your service on every reboot: `sudo systemctl disable example.service`

The location of the service on the server: `/etc/systemd/system` and called `socket.service`
