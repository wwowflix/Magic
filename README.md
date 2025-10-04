# Magic

[![CI](https://github.com/wwowflix/Magic/actions/workflows/ci.yml/badge.svg)](https://github.com/wwowflix/Magic/actions)
[![codecov](https://codecov.io/gh/wwowflix/Magic/branch/main/graph/badge.svg)](https://codecov.io/gh/wwowflix/Magic)

![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Release](https://img.shields.io/badge/release-v1.0--stable-blue)
## Run with Docker

```bash
docker pull wwowdocker/magic:latest

# Show help
docker run --rm wwowdocker/magic:latest --help

# Version
docker run --rm wwowdocker/magic:latest --version

# Run self-healing summary
docker run --rm -v ${PWD}/outputs/logs:/app/outputs/logs `
  wwowdocker/magic:latest --summary /app/outputs/logs/runner_summary.tsv
## Status

[![Docker Pulls](https://img.shields.io/docker/pulls/wwowdocker/magic)](https://hub.docker.com/r/wwowdocker/magic)
[![GitHub Actions CI](https://github.com/wwowflix/Magic/actions/workflows/publish.yml/badge.svg)](https://github.com/wwowflix/Magic/actions/workflows/publish.yml)
[![Release](https://img.shields.io/github/v/release/wwowflix/Magic)](https://github.com/wwowflix/Magic/releases)
