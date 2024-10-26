# Nerva Python Library

[![Ruff](https://github.com/Sn1F3rt/nerva-py/actions/workflows/ruff.yml/badge.svg)](https://github.com/Sn1F3rt/nerva-py/actions/workflows/ruff.yml)
[![Build](https://github.com/Sn1F3rt/nerva-py/actions/workflows/build.yml/badge.svg)](https://github.com/Sn1F3rt/nerva-py/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/Sn1F3rt/nerva-py)](LICENSE)

## Table of Contents

- [About](#about)
- [Installation](#installation)
    * [Requirements](#requirements)
    * [Setup](#setup)
- [Documentation](#documentation)
- [Support](#support)
- [License](#license)

## About

Python bindings for the JSON RPC interface of the Nerva cryptocurrency.

## Installation

### Requirements

- Python 3.8+
- [`uv`](https://docs.astral.sh/uv/) (for development only)

### Setup

To install current latest release you can use following command:
```sh
pip install nerva-py
```

To install the latest development version you can use following command:
```sh
uv add git+https://github.com/Sn1F3rt/nerva-py.git --branch main
```

## Documentation

Developers please refer to the docstrings in the code for more information. Full API reference will be available soon.

Here is a simple example to get you started:

```python
import asyncio

from nerva.daemon import DaemonJSONRPC


async def main():
    daemon = DaemonJSONRPC(
        host="x.y.z.w",
    )

    print(await daemon.get_info())


asyncio.run(main())
```

## Support

- [Issues](https://github.com/Sn1F3rt/nerva-py/issues)
- [Discord](https://discord.gg/ufysfvcFwe) - `Development > #nerva-py`

## License

[MIT License](LICENSE)

Copyright &copy; 2024 [Sayan "Sn1F3rt" Bhattacharyya](https://sn1f3rt.dev)
