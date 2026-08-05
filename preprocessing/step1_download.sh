#!/bin/bash

# 1. Require input and output directories
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <input_directory> <output_directory>"
    echo "Example: $0 ./download_link /path/to/output_pbf_dir"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# 2. Input must already exist
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist!"
    exit 1
fi

# 3. Create output directory if missing
mkdir -p "$OUTPUT_DIR" || {
    echo "Error: Failed to create output directory '$OUTPUT_DIR'!"
    exit 1
}

# Convert to absolute paths to avoid issues during 'cd'
INPUT_DIR=$(realpath "$INPUT_DIR")
OUTPUT_DIR=$(realpath "$OUTPUT_DIR")

echo "Input directory (download lists): $INPUT_DIR"
echo "Output directory (saved .osm.pbf): $OUTPUT_DIR"
echo "Starting to scan directory and its subdirectories..."

# 4. Recursively locate all .txt files (handle spaces safely)
find "$INPUT_DIR" -type f -name "*.txt" -print0 | while IFS= read -r -d '' txt_file; do
    echo "=================================================="
    echo "Found download list: $txt_file"

    # Relative path of the txt's parent under INPUT_DIR, e.g. Europe/France
    rel_dir=$(dirname "${txt_file#$INPUT_DIR/}")
    if [ "$rel_dir" = "." ]; then
        out_dir="$OUTPUT_DIR"
    else
        out_dir="$OUTPUT_DIR/$rel_dir"
    fi

    mkdir -p "$out_dir" || {
        echo "Warning: Cannot create output directory $out_dir, skipping..."
        continue
    }

    # 5. cd into the mirrored output directory; curl -O writes files here
    cd "$out_dir" || {
        echo "Warning: Cannot enter directory $out_dir, skipping..."
        continue
    }

    echo "Saving downloads to: $out_dir"
    echo "Starting 4-process download..."

    # 6. Same download command; read URLs from the txt under INPUT_DIR
    # Note: 'tr -d '\r'' removes Windows carriage returns to prevent curl URL errors
    cat "$txt_file" | tr -d '\r' | xargs -n 1 -P 4 curl -L -O -C -

    echo ">> Downloads from $(basename "$txt_file") completed!"
done

echo "=================================================="
echo "All download tasks across all directories have been successfully completed!"
