```xhost +local:docker```
```sudo docker build -t --progress=plain figinii/swe-rp-2.1 .```
```sudo docker build -t figinii/swe-rp-2.1 .```
```sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix paologinefra/se2rp