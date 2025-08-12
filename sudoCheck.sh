#!/bin/bash

RED="\033[31m"
NC="\033[0m"

if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}-sudo required${NC}"
  exit 1
fi