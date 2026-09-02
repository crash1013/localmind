#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# source /opt/intel/oneapi/setvars.sh
ONEAPI_VARS="/opt/intel/oneapi/setvars.sh"

if [[ ! -f "${ONEAPI_VARS}" ]]; then
    echo "[ERROR] Intel oneAPI environment script not found:"
    echo "        ${ONEAPI_VARS}"
    exit 1
fi

if [[ -z "${ONEAPI_ROOT:-}" ]]; then
    echo "[INFO] Loading Intel oneAPI environment..."
    set +u
    # shellcheck disable=SC1091
    source "${ONEAPI_VARS}"
    set -u
else
    echo "[INFO] Intel oneAPI environment already loaded: ${ONEAPI_ROOT}"
fi

export LD_LIBRARY_PATH="$HOME/.local/lib64:${LD_LIBRARY_PATH:-}"
export ONEAPI_DEVICE_SELECTOR=level_zero:gpu

exec .venv/bin/python src/localmind/gui/workbench.py
