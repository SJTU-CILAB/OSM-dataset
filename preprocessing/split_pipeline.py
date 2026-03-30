#!/usr/bin/env python3
"""Convert every .osm file under an input directory into legacy-compatible CSVs.

Outputs for each input file <stem>.osm:
    <output_root>/<relative_parent>/<stem>/<stem>_node.csv
    <output_root>/<relative_parent>/<stem>/<stem>_split_edge.csv
    <output_root>/<relative_parent>/<stem>/<stem>_fulltag_edge.csv

The script keeps the legacy column layout from the user's old scripts, but removes the
intermediate edge.csv step and writes CSV rows incrementally while streaming the XML.
"""

from __future__ import annotations

import argparse
import csv
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Iterable

from lxml import etree

# Legacy-compatible node column order from stream_osm.py
NODE_COLUMNS = [
    "osmid", "x", "y", "continent", "name", "aerialway", "aeroway", "amenity",
    "barrier", "boundary", "admin_level", "building", "entrance", "height", "craft",
    "emergency", "geological", "healthcare", "highway", "ford", "lit", "historic",
    "landuse", "leisure", "man_made", "military", "natural", "office", "place",
    "population", "is_in", "power", "public_transport", "railway", "shop", "sport",
    "telecom", "tourism", "water", "waterway", "crossing",
]

# Legacy-compatible edge column order from stream_osm.py (including nodes in the original step)
LEGACY_EDGE_COLUMNS = [
    "osmid", "nodes", "continent", "name", "aerialway", "aeroway", "amenity", "barrier",
    "boundary", "admin_level", "building", "entrance", "craft", "emergency", "geological",
    "healthcare", "highway", "footway", "sidewalk", "cycleway", "abutters", "bus_bay",
    "junction", "lanes", "lit", "motorroad", "oneway", "overtaking", "priority_road",
    "service", "smoothness", "surface", "turn", "historic", "landuse", "leisure",
    "man_made", "military", "natural", "office", "place", "population", "is_in", "power",
    "public_transport", "railway", "usage", "route", "shop", "sport", "telecom", "tourism",
    "water", "waterway", "area", "bridge", "access", "est_width", "maxwidth",
    "maxaxleload", "maxheight", "maxlength", "maxstay", "maxweight", "maxspeed", "minspeed",
]

EDGE_FULLTAG_COLUMNS = [col for col in LEGACY_EDGE_COLUMNS if col != "nodes"]
SPLIT_EDGE_COLUMNS = ["osmid", "osmid_start", "osmid_end"]


def legacy_region_name(stem: str) -> str:
    """Keep the old 'continent' naming behavior, but handle generic names better.

    Example:
        kiribati-260325 -> kiribati
        north-rhine-westphalia-latest -> north_rhine_westphalia
        test -> test
    """
    base = stem.rsplit("-", 1)[0] if "-" in stem else stem
    return base.replace("-", "_")


def normalize_csv_value(value: object) -> str:
    if value is None:
        return ""
    text = str(value)
    # The old scripts tried to remove problematic Unicode line separators and broken entities.
    # We keep the data, but normalize only the known line-breaking characters that often break CSV consumers.
    return text.replace("\u2028", " ").replace("\u2029", " ")


@dataclass
class ConversionStats:
    osm_file: str
    output_dir: str
    node_rows: int = 0
    fulltag_edge_rows: int = 0
    split_edge_rows: int = 0
    relation_rows_skipped: int = 0
    duration_seconds: float = 0.0
    skipped_existing: bool = False
    error: str = ""


class DelimitedCsvWriter:
    def __init__(self, path: Path, header: list[str], delimiter: str = "@") -> None:
        self.path = path
        self.header = header
        self.delimiter = delimiter
        self._fh = None
        self._writer = None

    def __enter__(self) -> "DelimitedCsvWriter":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("w", encoding="utf-8-sig", newline="")
        self._writer = csv.writer(
            self._fh,
            delimiter=self.delimiter,
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )
        self._writer.writerow(self.header)
        return self

    def writerow(self, row: Iterable[object]) -> None:
        assert self._writer is not None
        self._writer.writerow([normalize_csv_value(value) for value in row])

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._fh is not None:
            self._fh.close()



def output_dir_for_file(input_root: Path, output_root: Path, osm_file: Path) -> Path:
    relative_parent = osm_file.relative_to(input_root).parent
    return output_root / relative_parent / osm_file.stem



def clear_lxml_element(elem: etree._Element) -> None:
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]



def process_one_file(osm_file_str: str, input_root_str: str, output_root_str: str, overwrite: bool) -> dict:
    osm_file = Path(osm_file_str)
    input_root = Path(input_root_str)
    output_root = Path(output_root_str)
    target_dir = output_dir_for_file(input_root, output_root, osm_file)
    stem = osm_file.stem
    region_name = legacy_region_name(stem)

    node_csv = target_dir / f"{stem}_node.csv"
    split_edge_csv = target_dir / f"{stem}_split_edge.csv"
    fulltag_edge_csv = target_dir / f"{stem}_fulltag_edge.csv"

    stats = ConversionStats(osm_file=str(osm_file), output_dir=str(target_dir))
    start = perf_counter()

    try:
        if not overwrite and node_csv.exists() and split_edge_csv.exists() and fulltag_edge_csv.exists():
            stats.duration_seconds = perf_counter() - start
            stats.skipped_existing = True
            return asdict(stats)

        with (
            DelimitedCsvWriter(node_csv, NODE_COLUMNS) as node_writer,
            DelimitedCsvWriter(split_edge_csv, SPLIT_EDGE_COLUMNS) as split_writer,
            DelimitedCsvWriter(fulltag_edge_csv, EDGE_FULLTAG_COLUMNS) as fulltag_writer,
        ):
            # recover=True makes the parser more tolerant of minor XML issues, which matches
            # the spirit of the old scripts that manually stripped some problematic characters.
            context = etree.iterparse(
                str(osm_file),
                events=("end",),
                tag=("node", "way", "relation"),
                recover=True,
                huge_tree=True,
            )

            for _, elem in context:
                if elem.tag == "node":
                    tags: dict[str, str] = {}
                    for child in elem:
                        if child.tag == "tag":
                            key = child.get("k")
                            if key:
                                tags[key] = child.get("v", "")

                    row = [
                        elem.get("id", ""),
                        elem.get("lon", ""),  # legacy x
                        elem.get("lat", ""),  # legacy y
                        region_name,
                    ]
                    row.extend(tags.get(column, "") for column in NODE_COLUMNS[4:])
                    node_writer.writerow(row)
                    stats.node_rows += 1

                elif elem.tag == "way":
                    nd_refs: list[str] = []
                    tags = {}
                    for child in elem:
                        if child.tag == "nd":
                            ref = child.get("ref")
                            if ref:
                                nd_refs.append(ref)
                        elif child.tag == "tag":
                            key = child.get("k")
                            if key:
                                tags[key] = child.get("v", "")

                    way_id = elem.get("id", "")
                    fulltag_row = [way_id, region_name]
                    fulltag_row.extend(tags.get(column, "") for column in EDGE_FULLTAG_COLUMNS[2:])
                    fulltag_writer.writerow(fulltag_row)
                    stats.fulltag_edge_rows += 1

                    if len(nd_refs) >= 2:
                        for start_osmid, end_osmid in zip(nd_refs, nd_refs[1:]):
                            split_writer.writerow([way_id, start_osmid, end_osmid])
                            stats.split_edge_rows += 1

                elif elem.tag == "relation":
                    stats.relation_rows_skipped += 1

                clear_lxml_element(elem)

        stats.duration_seconds = perf_counter() - start
        return asdict(stats)

    except Exception as exc:  # pragma: no cover - kept for operational robustness
        stats.duration_seconds = perf_counter() - start
        stats.error = f"{type(exc).__name__}: {exc}"
        return asdict(stats)



def discover_osm_files(input_root: Path) -> list[Path]:
    return sorted(path for path in input_root.rglob("*.osm") if path.is_file())



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert every .osm file under an input directory into legacy-compatible CSV outputs.")
    parser.add_argument("input_dir", type=Path, help="Directory that contains .osm files (searched recursively).")
    parser.add_argument("output_dir", type=Path, help="Root directory for converted CSV outputs.")
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, (os.cpu_count() or 1) - 1),
        help="Number of worker processes. Default: cpu_count - 1.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite outputs even if all three CSVs already exist.",
    )
    return parser.parse_args()



def main() -> int:
    args = parse_args()
    input_root = args.input_dir.resolve()
    output_root = args.output_dir.resolve()

    if not input_root.exists() or not input_root.is_dir():
        raise SystemExit(f"Input directory does not exist or is not a directory: {input_root}")

    osm_files = discover_osm_files(input_root)
    if not osm_files:
        raise SystemExit(f"No .osm files found under: {input_root}")

    output_root.mkdir(parents=True, exist_ok=True)

    print(f"Discovered {len(osm_files)} .osm file(s) under {input_root}")
    print(f"Output root: {output_root}")
    print(f"Workers: {args.workers}")

    overall_start = perf_counter()
    total_nodes = 0
    total_fulltag_edges = 0
    total_split_edges = 0
    failures: list[dict] = []

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        future_to_file = {
            executor.submit(process_one_file, str(osm_file), str(input_root), str(output_root), args.overwrite): osm_file
            for osm_file in osm_files
        }
        for future in as_completed(future_to_file):
            result = future.result()
            if result["error"]:
                failures.append(result)
                print(f"[FAILED] {result['osm_file']} -> {result['error']}")
                continue

            if result["skipped_existing"]:
                print(f"[SKIPPED] {result['osm_file']} -> {result['output_dir']} (all 3 outputs already exist)")
                continue

            total_nodes += result["node_rows"]
            total_fulltag_edges += result["fulltag_edge_rows"]
            total_split_edges += result["split_edge_rows"]
            print(
                "[DONE] {osm_file} | nodes={node_rows:,} fulltag_edges={fulltag_edge_rows:,} "
                "split_edges={split_edge_rows:,} relations_skipped={relation_rows_skipped:,} "
                "time={duration_seconds:.2f}s -> {output_dir}".format(**result)
            )

    total_seconds = perf_counter() - overall_start
    print("=" * 80)
    print(f"Finished in {total_seconds:.2f}s")
    print(f"Total nodes written: {total_nodes:,}")
    print(f"Total fulltag edges written: {total_fulltag_edges:,}")
    print(f"Total split edges written: {total_split_edges:,}")
    print(f"Failures: {len(failures)}")

    if failures:
        print("Failed files:")
        for failure in failures:
            print(f"  - {failure['osm_file']}: {failure['error']}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
