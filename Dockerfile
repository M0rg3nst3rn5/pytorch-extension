FROM python:3.11-slim AS build
WORKDIR /src
ENV MAX_JOBS=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
COPY . .
RUN python3 -m pip wheel . --no-deps --no-build-isolation -w /wheels

FROM python:3.11-slim
RUN python3 -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN python3 -m pip install --no-cache-dir pytest
COPY --from=build /wheels /wheels
RUN python3 -m pip install /wheels/*.whl
COPY tests /opt/tests
CMD ["python3", "-m", "pytest", "-q", "/opt/tests"]
