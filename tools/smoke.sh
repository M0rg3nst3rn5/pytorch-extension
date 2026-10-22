#!/bin/bash
set -euo pipefail

build_env=/tmp/trajectory-ops-build
run_env=/tmp/trajectory-ops-run

rm -rf "$build_env" "$run_env"
python3 -m venv "$build_env" && \
"$build_env/bin/pip" install torch --index-url https://download.pytorch.org/whl/cpu && \
"$build_env/bin/pip" wheel . --no-deps -w dist && \
ls dist | grep linux && \
python3 -m venv "$run_env" && \
"$run_env/bin/pip" install torch --index-url https://download.pytorch.org/whl/cpu && \
"$run_env/bin/pip" install dist/*.whl && \
cd /tmp && "$run_env/bin/python" -c 'import torch; from trajectory_ops import trajectory_acceleration; result = trajectory_acceleration(torch.tensor([0.0, 1.0, 8.0])); assert torch.equal(result, torch.tensor([6.0])); print("OK")'
