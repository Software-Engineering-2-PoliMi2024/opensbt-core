# -it = interactive terminal
# --rm = remove container after exit
# -e DISPLAY=$DISPLAY = pass the display environment variable
# -v /tmp/.X11-unix:/tmp/.X11-unix = mount the X11 socket for GUI applications
# -v $(pwd):/se2rp = mount the current directory to /se2rp in the container
# paologinefra/se2rp = the Docker image to use
# bash = command to run in the container

docker run \
    --rm \
    -it -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/open-bst/se2rpCODEBASE \
    paologinefra/se2rp \
    bash