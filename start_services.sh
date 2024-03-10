#!/bin/bash

# Define an array with the names of the directories containing Dockerfiles
declare -a dirs=("root" "api" "inference" "storage")

# Loop over the directories
for dir in "${dirs[@]}"
do
  # Build the Docker image
  docker build -t "${dir}_image" "/src/${dir}"

  # Run the Docker container
  docker run -d --name "${dir}_container" "${dir}_image"
done