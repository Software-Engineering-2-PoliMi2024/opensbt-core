# Basic Usage
# To use the Docker Manager, simply run this script and follow the prompts to either build a Docker image or run a Docker container.

usage() {
    echo "Usage: ./DockerManager.sh"
    echo "This script provides options to build a Docker image or run a Docker container."
    echo "Follow the on-screen prompts to make your selection."
}

# Call the usage function if needed
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
    exit 0
fi


# Ensures gum is installed and functional
./Docker/DockerManager/CheckGum.sh

gum style \
    --foreground 39 --border-foreground 39 --border double \
    --align center --width 50 --margin "1 2" --padding "2 4" \
    'the Docker Manager'

choices=$(gum choose \
        --header "What do you want to do?" \
        --no-limit \
        --selected "Run Docker Container" \
        "Build Docker Image" \
        "Run Docker Container")

# Handle multiple choices
if [[ "$choices" == *"Build Docker Image"* ]]; then
    ./Docker/DockerManager/dockerBuild.sh
fi
if [[ "$choices" == *"Run Docker Container"* ]]; then
    ./Docker/DockerManager/dockerRun.sh
fi


