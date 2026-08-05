#!/usr/bin/env bash
set -euo pipefail

# Convert all .osm.pbf files under an input directory tree into .osm files,
# preserving the relative directory layout under the output directory.
#
# Usage:
#   ./step2_convert.sh <input_pbf_dir> <output_osm_dir> [workers]
#
# Examples:
#   ./step2_convert.sh /data/PBF_files_202603 /data/OSM_files_202603
#   ./step2_convert.sh /data/PBF_files_202603 /data/OSM_files_202603 8

DEFAULT_WORKERS=16

usage() {
    echo "Usage: $0 <input_pbf_dir> <output_osm_dir> [workers]"
    echo "  input_pbf_dir   Root directory containing .osm.pbf files (required, must exist)"
    echo "  output_osm_dir  Root directory for converted .osm files (created if missing)"
    echo "  workers         Number of parallel osmium processes (default: ${DEFAULT_WORKERS})"
    exit 1
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
    usage
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
WORKERS="${3:-$DEFAULT_WORKERS}"

if ! [[ "${WORKERS}" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: workers must be a positive integer, got: ${WORKERS}"
    exit 1
fi

if [[ ! -d "${INPUT_DIR}" ]]; then
    echo "Error: input directory does not exist: ${INPUT_DIR}"
    exit 1
fi

mkdir -p "${OUTPUT_DIR}" || {
    echo "Error: failed to create output directory: ${OUTPUT_DIR}"
    exit 1
}

INPUT_DIR="$(realpath "${INPUT_DIR}")"
OUTPUT_DIR="$(realpath "${OUTPUT_DIR}")"

ensure_osmium() {
    if command -v osmium >/dev/null 2>&1; then
        echo "osmium is already installed: $(command -v osmium)"
        osmium --version 2>/dev/null | head -n 1 || true
        return 0
    fi

    echo "osmium not found. Attempting to install osmium-tool..."

    if command -v apt-get >/dev/null 2>&1; then
        if [[ "$(id -u)" -eq 0 ]]; then
            apt-get update
            apt-get install -y osmium-tool
        elif command -v sudo >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y osmium-tool
        else
            echo "Error: apt-get found, but root/sudo privileges are required to install osmium-tool."
            echo "Please run: sudo apt-get update && sudo apt-get install -y osmium-tool"
            exit 1
        fi
    elif command -v yum >/dev/null 2>&1; then
        if [[ "$(id -u)" -eq 0 ]]; then
            yum install -y osmium-tool
        elif command -v sudo >/dev/null 2>&1; then
            sudo yum install -y osmium-tool
        else
            echo "Error: yum found, but root/sudo privileges are required to install osmium-tool."
            echo "Please run: sudo yum install -y osmium-tool"
            exit 1
        fi
    elif command -v brew >/dev/null 2>&1; then
        brew install osmium-tool
    else
        echo "Error: could not auto-install osmium. No supported package manager found (apt-get/yum/brew)."
        echo "Please install osmium-tool manually, then re-run this script."
        exit 1
    fi

    if ! command -v osmium >/dev/null 2>&1; then
        echo "Error: osmium installation finished, but 'osmium' is still not on PATH."
        exit 1
    fi

    echo "osmium installed successfully: $(command -v osmium)"
}

ensure_osmium

echo "Input directory : ${INPUT_DIR}"
echo "Output directory: ${OUTPUT_DIR}"
echo "Workers         : ${WORKERS}"

STATUS_DIR="$(mktemp -d)"
JOB_LIST="$(mktemp)"
trap 'rm -rf "${STATUS_DIR}" "${JOB_LIST}"' EXIT

# Convert one "input_pbf|output_osm" pair.
# STATUS_DIR is read from the environment (exported below).
convert_one() {
    local pair="$1"
    local pbf_file="${pair%%|*}"
    local out_file="${pair#*|}"
    local out_dir
    local stamp

    out_dir="$(dirname "${out_file}")"
    mkdir -p "${out_dir}"
    stamp="$(printf '%s' "${out_file}" | md5sum | awk '{print $1}')"

    if [[ -f "${out_file}" ]]; then
        echo "[SKIP] already exists: ${out_file}"
        : > "${STATUS_DIR}/skip.${stamp}"
        return 0
    fi

    echo "[CONVERT] ${pbf_file} -> ${out_file}"
    if osmium cat "${pbf_file}" -o "${out_file}"; then
        echo "[DONE] ${out_file}"
        : > "${STATUS_DIR}/done.${stamp}"
        return 0
    fi

    echo "[FAIL] ${pbf_file}"
    rm -f "${out_file}"
    : > "${STATUS_DIR}/fail.${stamp}"
    return 1
}
export -f convert_one
export STATUS_DIR

total=0
while IFS= read -r -d '' pbf_file; do
    rel_path="${pbf_file#${INPUT_DIR}/}"
    out_file="${OUTPUT_DIR}/${rel_path%.osm.pbf}.osm"
    printf '%s|%s\0' "${pbf_file}" "${out_file}"
    total=$((total + 1))
done < <(find "${INPUT_DIR}" -type f -name "*.osm.pbf" -print0 | sort -z) > "${JOB_LIST}"

if [[ "${total}" -eq 0 ]]; then
    echo "Error: no .osm.pbf files found under ${INPUT_DIR}"
    exit 1
fi

echo "Discovered ${total} .osm.pbf file(s). Starting parallel conversion..."

set +e
xargs -0 -P "${WORKERS}" -n 1 -a "${JOB_LIST}" bash -c 'convert_one "$1"' _
xargs_status=$?
set -e

skipped="$(find "${STATUS_DIR}" -maxdepth 1 -type f -name 'skip.*' | wc -l | tr -d ' ')"
converted="$(find "${STATUS_DIR}" -maxdepth 1 -type f -name 'done.*' | wc -l | tr -d ' ')"
failed="$(find "${STATUS_DIR}" -maxdepth 1 -type f -name 'fail.*' | wc -l | tr -d ' ')"

echo "----------------------------------------"
echo "Finished"
echo "Total files : ${total}"
echo "Converted   : ${converted}"
echo "Skipped     : ${skipped}"
echo "Failed      : ${failed}"
echo "Output dir  : ${OUTPUT_DIR}"

if [[ "${failed}" -ne 0 || "${xargs_status}" -ne 0 ]]; then
    exit 1
fi
