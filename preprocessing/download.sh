#!/bin/bash

# 1. Check if the target directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target_directory_path>"
    echo "Example: $0 /path/to/your/directory"
    exit 1
fi

TARGET_DIR="$1"

# 2. Check if the provided path is a valid directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist!"
    exit 1
fi

# Convert relative path to absolute path to avoid issues during 'cd'
TARGET_DIR=$(realpath "$TARGET_DIR")

echo "Starting to scan directory and its subdirectories: $TARGET_DIR"

# 3. Use 'find' to recursively locate all .txt files safely (handling spaces in paths)
find "$TARGET_DIR" -type f -name "*.txt" -print0 | while IFS= read -r -d '' txt_file; do
    echo "=================================================="
    echo "Found download list: $txt_file"

    # Get the directory path and the base name of the txt file
    dir_path=$(dirname "$txt_file")
    file_name=$(basename "$txt_file")

    # 4. Change to the directory where the txt file is located
    # If 'cd' fails, print a warning and skip to the next file
    cd "$dir_path" || { echo "Warning: Cannot enter directory $dir_path, skipping..."; continue; }

    echo "Current working directory changed to: $dir_path"
    echo "Starting 4-process download..."

    # 5. Execute the download command
    # Note: 'tr -d '\r'' removes Windows carriage returns to prevent curl URL errors
    cat "$file_name" | tr -d '\r' | xargs -n 1 -P 4 curl -L -O -C -

    echo ">> Downloads from $file_name completed!"
done

echo "=================================================="
echo "All download tasks across all directories have been successfully completed!"