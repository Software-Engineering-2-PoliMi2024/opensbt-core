# Check if gum is installed and functional, otherwise install it
if ! command -v gum &> /dev/null || ! gum --version &> /dev/null; then
    echo "gum is not installed or not functional. Installing gum..."
    echo "Detected OS type: $OSTYPE"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Adding Charm repository and installing gum..."
        echo "deb [trusted=yes] https://repo.charm.sh/apt/ /" | sudo tee /etc/apt/sources.list.d/charm.list
        if sudo apt update && sudo apt install gum; then
            echo "gum installed successfully."
        else
            echo "Failed to install gum. Please check your network or permissions."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Using Homebrew to install gum..."
        if brew install gum; then
            echo "gum installed successfully."
        else
            echo "Failed to install gum. Please check your Homebrew setup."
            exit 1
        fi
    else
        echo "Unsupported OS type: $OSTYPE. Please install gum manually from https://github.com/charmbracelet/gum"
        exit 1
    fi
fi