docker run \
    --rm \
    -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -p 8000:8000 \
    paologinefra/se2rp-simulator