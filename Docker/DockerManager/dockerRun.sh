# -it = interactive terminal
# --rm = remove container after exit
# -e DISPLAY=$DISPLAY = pass the display environment variable
# -v /tmp/.X11-unix:/tmp/.X11-unix = mount the X11 socket for GUI applications
# -v $(pwd):/se2rp = mount the current directory to /se2rp in the container
# paologinefra/se2rp = the Docker image to use
# bash = command to run in the container

# Check if gum is installed and functional
./Docker/DockerManager/CheckGum.sh

# clear

./Docker/DockerManager/sudoCheck.sh

gum style \
    --foreground 39 --border-foreground 39 --border double \
    --align center --width 50 --margin "1 2" --padding "2 4" \
    'Simulator Docker running'

# xhost +local:docker # grant docker permission to X server

docker run \
    --rm \
    -it -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/open-bst/se2rpCODEBASE \
    paologinefra/se2rp \
    bash