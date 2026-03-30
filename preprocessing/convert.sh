#!/usr/bin/env bash
set -euo pipefail

# 用法：
#   ./convert_continent.sh Asia
#   ./convert_continent.sh Europe
#
# 如果脚本不放在主目录，也可以手动传入主目录：
#   ./convert_continent.sh Asia /path/to/main_dir

usage() {
    echo "用法: $0 <Continent> [BASE_DIR]"
    echo "例如: $0 Asia"
    echo "例如: $0 Europe /data/your_main_dir"
    exit 1
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage
fi

CONTINENT="$1"

# 默认主目录 = 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${2:-$SCRIPT_DIR}"

PBF_ROOT="${BASE_DIR}/PBF_files"
OSM_ROOT="${BASE_DIR}/OSM_files"

SRC_DIR="${PBF_ROOT}/${CONTINENT}"
DST_DIR="${OSM_ROOT}/${CONTINENT}"

# 检查 osmium 是否存在
if ! command -v osmium >/dev/null 2>&1; then
    echo "错误：没有找到 osmium，请先安装 osmium-tool。"
    exit 1
fi

# 检查目录
if [[ ! -d "${PBF_ROOT}" ]]; then
    echo "错误：找不到目录 ${PBF_ROOT}"
    exit 1
fi

if [[ ! -d "${OSM_ROOT}" ]]; then
    echo "错误：找不到目录 ${OSM_ROOT}"
    exit 1
fi

if [[ ! -d "${SRC_DIR}" ]]; then
    echo "错误：找不到大洲目录 ${SRC_DIR}"
    exit 1
fi

# 目标大洲目录不存在就创建
mkdir -p "${DST_DIR}"

total=0
converted=0
skipped=0
failed=0

# 查找该大洲下所有 .osm.pbf 文件
while IFS= read -r -d '' pbf_file; do
    total=$((total + 1))

    # 计算相对路径（相对于该大洲目录）
    rel_path="${pbf_file#${SRC_DIR}/}"

    # 把后缀 .osm.pbf 改成 .osm
    out_file="${DST_DIR}/${rel_path%.osm.pbf}.osm"
    out_dir="$(dirname "${out_file}")"

    # 创建输出目录，保持层次结构
    mkdir -p "${out_dir}"

    # 如果已经存在就跳过，方便断点续跑
    if [[ -f "${out_file}" ]]; then
        echo "[跳过] 已存在: ${out_file}"
        skipped=$((skipped + 1))
        continue
    fi

    echo "[转换] ${pbf_file} -> ${out_file}"

    if osmium cat "${pbf_file}" -o "${out_file}"; then
        converted=$((converted + 1))
    else
        echo "[失败] ${pbf_file}"
        rm -f "${out_file}"
        failed=$((failed + 1))
    fi

done < <(find "${SRC_DIR}" -type f -name "*.osm.pbf" -print0)

echo "----------------------------------------"
echo "完成：${CONTINENT}"
echo "总文件数: ${total}"
echo "成功转换: ${converted}"
echo "跳过已有: ${skipped}"
echo "失败数量: ${failed}"
echo "输出目录: ${DST_DIR}"