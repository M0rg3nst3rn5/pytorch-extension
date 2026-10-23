# Trajectory operations

## Install and run a ready wheel

Put the ready `trajectory_ops-*.whl` file in this directory.

### 1. Create an environment

```bash
python3 -m venv .venv
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 2. Install the wheel

```bash
.venv/bin/pip install ./trajectory_ops-*.whl
```

### 3. Try a small Python program

```bash
.venv/bin/python examples/try_acceleration.py
```

It prints the input positions and `acceleration: tensor([ 6., 12., 18.])`.

## Build, test, and check the project

This section is for the team building the wheel from this repository.

### Build

From the repository directory:

```bash
python3 -m venv /tmp/trajectory-build
/tmp/trajectory-build/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/tmp/trajectory-build/bin/pip wheel . --no-deps -w dist
ls dist
```

The resulting `dist/trajectory_ops-*.whl` is the file to install using the first section.

### Test the installed wheel

From the repository directory:

```bash
python3 -m venv /tmp/trajectory-test
/tmp/trajectory-test/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/tmp/trajectory-test/bin/pip install pytest dist/*.whl
rm -rf /tmp/trajectory-tests && cp -r tests /tmp/trajectory-tests
(cd /tmp && /tmp/trajectory-test/bin/python -m pytest -q /tmp/trajectory-tests)
```

Expected output: `7 passed`.

### Required checks

From the repository directory:

```bash
/tmp/trajectory-test/bin/pip install ruff
/tmp/trajectory-test/bin/ruff check .
./tools/smoke.sh
docker build -t trajectory-ops:0.1 .
docker run --rm trajectory-ops:0.1
```

The smoke script prints `OK`; Docker prints `7 passed`.

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

A new test, `test_input_dtype` (commit `3444f2a`), passed a plain Python list to the op and asserted that the output was *not* `float32`. The extension only accepts tensors, and a float32 input always gives a float32 output, so the test could never pass. It surfaced as a red test: after the list was replaced with a tensor, `pytest` failed with `assert torch.float32 != torch.float32` (1 failed, 6 passed). The fix in commit `994b3a6` passes a `float32` tensor and asserts `dtype == torch.float32`; the suite then showed `7 passed`.

The C++ loop computes `(x[i + 2] - x[i + 1]) - (x[i + 1] - x[i])`, the same two sequential subtractions as `torch.diff`. The shorter expression `x[i + 2] - 2 * x[i + 1] + x[i]` rounds differently: on `[-4339991.0, -14491808.0, -10363169.0]` it gives `14280457.0` instead of `14280456.0`, which would fail the exact `torch.equal` comparison.

Inputs with fewer than three values on the last dimension are intentionally unsupported and raise `RuntimeError`.

Profile the installed wheel on a `(1024, 7, 500)` float32 input (about 3.6 million values), inside the project image built above, from the repository directory:

```bash
docker run --rm -v "$PWD/tools:/tools:ro" -w /tmp trajectory-ops:0.1 \
  python3 -m cProfile -s cumulative /tools/profile.py
```

cProfile reported `cumtime` `0.005` seconds for the single `trajectory_acceleration` call, about half the `0.009` seconds that `torch.randn` took to generate the same input.
