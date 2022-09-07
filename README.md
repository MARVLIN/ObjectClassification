## How to start
- Activate virtual environment: `$ source venv/bin/activate`
- Install requirements.txt: `pip install -r requirements.txt`
- Set the script path to run_detect.py


## detect.py Breakdown
Run the detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.
Usage - sources:

    $ `python detect.py --weights yolov5s.pt --source 0`

- img.jpg          
- vid.mp4              
- path/                       
- 'path/*.jpg' 
                                                     

Usage - formats:

    $ `python detect.py --weights ProjectionAreas.pt`

- `yolov5s.torchscript`:         TorchScript
- `yolov5s.onnx`:                ONNX Runtime or OpenCV DNN with --dnn
- `yolov5s.xml`:                 OpenVINO
- `yolov5s.engine`:              TensorRT
- `yolov5s.mlmodel`:             CoreML (macOS-only)
- `yolov5s_saved_model`:         TensorFlow SavedModel
- `yolov5s.pb`:                  TensorFlow GraphDef
- `yolov5s.tflite`:              TensorFlow Lite
- `yolov5s_edgetpu.tflite`:      TensorFlow Edge TPU

Libraries used:
- **_argparse_**
- **_json_**
- **_json.encoder_**
- **_os_**
- **_sys_**
- **_Path (pathlib)_**
- **_requests_**
- **_torch_**
- **_client_** 
- **_capture_**

The main loop that loads a module `listen` and then activates `capture` module. Documentation for these modules can be found [here](https://github.com/dcomradd/ObjectClassification/tree/Module_Breakdown#readme)

After `clinet.listen()` receives a value of True, module `capture` is activated

`if client.listen():
    capture()`

The following snippet collects coordinates by creating empty lists for x, y, w, h coordinates. Before it populates the
lists when running `for loop` the program counts coordinates of the diagonal sides of the rectangle in detected region(s).
In addition, the program counts the centre of the detected area(s) for further projection purposes. 

  
`x_coord = []
y_coord = []
w_coord = []
h_coord = []

for *xyxy, conf, cls in reversed(det):
    count += 1
    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))

    center_point = round((c1[0] + c2[0]) / 2), round((c1[1] + c2[1]) / 2)
    circle = cv2.circle(im0, center_point, 5, (0, 255, 0), 2)
    text_coord = cv2.putText(im0, str(center_point), center_point, cv2.FONT_HERSHEY_PLAIN, 2,
                                             (0, 0, 255))

    # print(x_coord, y_coord, w_coord, h_coord)
    # print(center_point)


    x_coord.append(c1[0])
    y_coord.append(c1[1])

    w = c2[0] - c1[0]

    w_coord.append(w)

    h = c2[1] - c1[1]

    h_coord.append(h)`
    
Current snippet allows to make the detection from images and write results to `/runs/exp*` after detection ran
```
#Print results
for c in det[:, -1].unique():
    n = (det[:, -1] == c).sum()  # detections per class
    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

    # Write results
    for *xyxy, conf, cls in reversed(det):
        if save_txt:  # Write to file
        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
        with open(f'{txt_path}.txt', 'a') as f:
        f.write(('%g ' * len(line)).rstrip() % line + '\n')

        if save_img or save_crop or view_img:  # Add bbox to image
            c = int(cls)  # integer class
            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
            annotator.box_label(xyxy, label, color=colors(c, True))
            if save_crop:
                save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                # Stream results
                im0 = annotator.result()
                if view_img:
                    import platform
                    if platform.system() == 'Linux' and p not in windows:
                        windows.append(p)
                        cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                        cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                        cv2.imshow(str(p), im0)
                        cv2.waitKey(1)  # 1 millisecond

                        # Save results (image with detections)
                        if save_img:
                            if dataset.mode == 'image':
                                cv2.imwrite(save_path, im0)
                            else:  # 'video' or 'stream'
                                if vid_path[i] != save_path:  # new video
                                    vid_path[i] = save_path
                                    if isinstance(vid_writer[i], cv2.VideoWriter):
                                        vid_writer[i].release()  # release previous video writer
                                        if vid_cap:  # video
                                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                        else:  # stream
                                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                                            save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                                            vid_writer[i].write(im0)
```

After the program processed detection, it creates one single list with coordinates and sends this list as a JSON to [API Server](https://github.com/dcomradd/Rest_API_Framework#readme)
Finally, `stop` is sent to the [Socket Server](https://github.com/dcomradd/ObjectClassification/tree/Module_Breakdown#readme)
        
```
Boxes = []

for i in range(len(x_coord)):
    Boxes.append({"X": x_coord[i], "Y": y_coord[i], "W": w_coord[i], "H": h_coord[i]})

    url = "http://art1x.pythonanywhere.com/snippets/1/"
    username = "artemii"
    password = "admin"
    data = {'Boxes': json.dumps(Boxes)}
    response = requests.put(url, auth=(username, password), data=data)
    print(response.status_code)
    print(response.json())


    # Print time (inference-only)
    LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')


    client.scan_complete()
```

## Conclusion
Current program can be run on Jetson Nano and on any computer with python>=3.7

After start, the program can run autonomously every time waiting for `snap`. When the program detected the object it sends
'Ready for capture' to the Socket Server. This program can be improved by using best.onnx model to make the RAM usage lower 