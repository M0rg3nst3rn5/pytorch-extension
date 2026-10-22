# Trajectory operations

## Install and run a ready wheel

Put the ready `trajectory_ops-*.whl` file in this directory.

### 1. Create an environment

```bash
uv venv .venv
uv pip install --python .venv/bin/python torch --index https://download.pytorch.org/whl/cpu
```

### 2. Install the wheel

```bash
uv pip install --python .venv/bin/python ./trajectory_ops-*.whl
```

### 3. Try a small Python program

```bash
.venv/bin/python examples/try_acceleration.py
```

It prints the input positions and `acceleration: tensor([ 6., 12., 18.])`.

## Build, test, and check the project

This section is for the team building the wheel from this repository.

### Build

```bash
uv venv /tmp/trajectory-build
uv pip install --python /tmp/trajectory-build/bin/python torch --index https://download.pytorch.org/whl/cpu
uv build --wheel --no-build-isolation --python /tmp/trajectory-build/bin/python --out-dir dist
ls dist
```

The resulting `dist/trajectory_ops-*.whl` is the file to install using the first section.

### Test the installed wheel

```bash
uv venv /tmp/trajectory-test
uv pip install --python /tmp/trajectory-test/bin/python torch --index https://download.pytorch.org/whl/cpu
uv pip install --python /tmp/trajectory-test/bin/python pytest dist/*.whl
cp -r tests /tmp/trajectory-tests
cd /tmp && /tmp/trajectory-test/bin/python -m pytest -q /tmp/trajectory-tests
```

Expected output: `6 passed`.

### Required checks

```bash
uv run --with ruff ruff check .
./tools/smoke.sh
docker build -t trajectory-ops:0.1 .
docker run --rm trajectory-ops:0.1
```

The smoke script prints `OK`; Docker prints `6 passed`.

## Operation

Python name: `trajectory_ops.trajectory_acceleration`.

Specification:

```python
torch.diff(x, n=2, dim=-1)
```

The operation calculates trajectory acceleration along the last dimension. It accepts CPU `torch.float32` tensors of shape `(..., T)` where `T >= 3`, and returns shape `(..., T - 2)`. Invalid dtype, device, rank, or time length raises `RuntimeError` from C++.

`pyproject.toml` defines the package and build backend. PyTorch is used to compile the extension but is not bundled into the wheel; every environment installs CPU PyTorch itself.

## Other project commands

`make wheel`, `make install`, `make test`, and `make clean` are available. CI runs `ruff` and `pytest` on each push and pull request. The Docker image builds the wheel in its first stage, installs it in its final stage, and tests only the installed wheel.

## Project note

The shorter expression `x[i + 2] - 2 * x[i + 1] + x[i]` rounded differently from `torch.diff`: on `[-4339991.0, -14491808.0, -10363169.0]` it produced `14280457.0` instead of `14280456.0`. The C++ loop therefore keeps two sequential subtractions. Add the fixing commit hash here when the team commits it.

Inputs with fewer than three values on the last dimension are intentionally unsupported and raise `RuntimeError`.

Profile the installed wheel with:

```bash
cd /tmp && /tmp/trajectory-test/bin/python -m cProfile -s cumulative /path/to/trajectory-ops/tools/profile.py
```

This development machine reported `3.370 seconds`, including PyTorch import time.
