gum style \
    --foreground 39 --border-foreground 39 --border double \
    --align center --width 50 --margin "1 2" --padding "2 4" \
    'Building Docker image...'

./Docker/DockerManager/sudoCheck.sh
    
python3 ./Docker/RequirementsAggregator.py . > requirements.txt

DOCKER_BUILDKIT=1 docker build -f Docker/Dockerfile -t paologinefra/se2rp .