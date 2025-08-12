./sudoCheck.sh
    
python3 docker_pyRequirements.py . > requirements.txt

DOCKER_BUILDKIT=1 docker build -t paologinefra/se2rp .