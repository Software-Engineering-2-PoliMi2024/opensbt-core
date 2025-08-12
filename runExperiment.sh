#!/bin/bash

# Add argument parsing for --headless and -h/--help
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --headless)
      HEADLESS=true
      shift # Remove --headless from processing
      ;;
    -h|--help)
      echo "Usage: $0 [--headless] [-h|--help]"
      echo "  --headless   Run the script with xvfb-run"
      echo "  -h, --help   Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use -h or --help for usage information."
      exit 1
      ;;
  esac
done

# Run the script with or without xvfb-run based on --headless
if [ "$HEADLESS" = true ]; then
  xvfb-run python runExperiment.py
else
  python runExperiment.py
fi