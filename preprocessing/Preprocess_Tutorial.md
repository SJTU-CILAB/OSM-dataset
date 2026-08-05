# Preprocessing Tutorial

This guide explains how to run the three scripts under `OSM-dataset/preprocessing/` to go from Geofabrik download lists to legacy-compatible CSV files.

## Pipeline Overview

```text
download_link/*.txt
        |
        |  Step 1: step1_download.sh
        v
   *.osm.pbf files
        |
        |  Step 2: step2_convert.sh   (requires osmium)
        v
   *.osm files
        |
        |  Step 3: step3_split.py     (requires Python 3 + lxml)
        v
   *_node.csv / *_split_edge.csv / *_fulltag_edge.csv
```

Directory layout is preserved across steps. For example:

```text
download_link/Europe/France/geofabrik_france_all_osm_pbf_links.txt
  -> PBF_files_YYYYMM/Europe/France/alsace-latest.osm.pbf
  -> OSM_files_YYYYMM/Europe/France/alsace-latest.osm
  -> CSV_files_YYYYMM/Europe/France/alsace-latest/alsace-latest_node.csv
                     /alsace-latest_split_edge.csv
                     /alsace-latest_fulltag_edge.csv
```

## Prerequisites

- `bash`, `curl`, `find`, `xargs`
- `osmium` (`osmium-tool`): Step 2 will try to install it automatically if missing
- Python 3 with `lxml` for Step 3:

```bash
pip install lxml
```

Recommended working directory:

```bash
cd OSM-dataset/preprocessing
chmod +x step1_download.sh step2_convert.sh
```

Replace the paths below with your own storage locations. The scripts do **not** hard-code `PBF_files_202603` / `OSM_files_202603`; those names are only examples.

---

## Step 1 — Download `.osm.pbf` files

**Script:** `step1_download.sh`

**Purpose:** Recursively read every `.txt` URL list under the input directory and download the listed Geofabrik `.osm.pbf` files into a mirrored output tree.

**Usage:**

```bash
./step1_download.sh <input_download_link_dir> <output_pbf_dir>
```

**Example:**

```bash
./step1_download.sh \
  ./download_link \
  /path/to/PBF_files_202603
```

**Notes:**

- `<input_download_link_dir>` must already exist (this repo ships `download_link/`).
- `<output_pbf_dir>` is created if it does not exist.
- Downloads use 4 parallel `curl` processes per txt file (`curl -L -O -C -`), with resume support.
- Files are saved next to the mirrored relative path of each txt, e.g. links under `download_link/Asia/Japan/` go to `PBF_files_.../Asia/Japan/`.

---

## Step 2 — Convert `.osm.pbf` to `.osm`

**Script:** `step2_convert.sh`

**Purpose:** Convert every `.osm.pbf` under an input root into `.osm` XML with `osmium cat`, keeping the same relative directory structure.

**Usage:**

```bash
./step2_convert.sh <input_pbf_dir> <output_osm_dir> [workers]
```

**Example:**

```bash
./step2_convert.sh \
  /path/to/PBF_files_202603 \
  /path/to/OSM_files_202603

# optional: override parallelism (default: 16)
./step2_convert.sh \
  /path/to/PBF_files_202603 \
  /path/to/OSM_files_202603 \
  8
```

**Notes:**

- `<input_pbf_dir>` must exist and should contain the full continent tree (e.g. `Africa/`, `Asia/`, `Europe/`, ...).
- `<output_osm_dir>` is created if missing.
- Existing `.osm` outputs are skipped so you can resume after interruption.
- If `osmium` is not installed, the script attempts to install `osmium-tool` via `apt-get` / `yum` / `brew` (may require sudo/root).

---

## Step 3 — Split `.osm` into CSV files

**Script:** `step3_split.py`

**Purpose:** Recursively parse every `.osm` file and write three `@`-delimited CSV files per region:

| Output file | Content |
|---|---|
| `<stem>_node.csv` | Nodes (coordinates + selected tags) |
| `<stem>_fulltag_edge.csv` | Ways / edges with tag attributes (no node sequence) |
| `<stem>_split_edge.csv` | Consecutive node pairs along each way: `osmid, osmid_start, osmid_end` |

**Usage:**

```bash
python step3_split.py <input_osm_dir> <output_csv_dir> [--workers N] [--overwrite]
```

**Example:**

```bash
python step3_split.py \
  /path/to/OSM_files_202603 \
  /path/to/CSV_files_202603

# optional: override parallelism (default: 16)
python step3_split.py \
  /path/to/OSM_files_202603 \
  /path/to/CSV_files_202603 \
  --workers 8

# optional: regenerate even if all three CSVs already exist
python step3_split.py \
  /path/to/OSM_files_202603 \
  /path/to/CSV_files_202603 \
  --overwrite
```

**Notes:**

- You can pass the entire `OSM_files_202603` root; the script searches recursively for `*.osm`.
- Processing is multiprocess via `ProcessPoolExecutor` (default `--workers 16`).
- If all three CSVs for a file already exist, that file is skipped unless `--overwrite` is set.
- OSM `relation` elements are skipped.

---

## End-to-End Example

```bash
cd OSM-dataset/preprocessing

# 1) Download PBF
./step1_download.sh ./download_link /path/to/PBF_files_202603

# 2) PBF -> OSM
./step2_convert.sh /path/to/PBF_files_202603 /path/to/OSM_files_202603 16

# 3) OSM -> CSV
python step3_split.py /path/to/OSM_files_202603 /path/to/CSV_files_202603 --workers 16
```

## Resume Behavior

All three steps are designed to be restart-friendly:

1. **Step 1:** `curl -C -` resumes partial downloads.
2. **Step 2:** skips targets that already have an `.osm` file.
3. **Step 3:** skips targets that already have all three CSV outputs (unless `--overwrite`).

## Tips

- Disk usage grows quickly from PBF → OSM → CSV. Prefer large local/NAS storage and monitor free space.
- For debugging, run Step 1 / Step 2 / Step 3 on a single subtree first (e.g. only `download_link/Antarctica` or a copied small region).
- Keep input/output roots separate so a failed conversion cannot overwrite your downloaded PBF archive.
