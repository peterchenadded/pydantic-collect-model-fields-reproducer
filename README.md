# Pydantic-collect-model-fields-reproducer

## Overview

Simple test to test pydantic subclass construction.

Created for https://github.com/pydantic/pydantic/issues/12647.

## Usage

1. Clone this repo
2. Open folder in VS Code
3. Run below command

```bash
uv run main.py
```

Example output

```text
2026-01-13 22:33:24,328 INFO     Starting generation of 10000 subclasses
2026-01-13 22:33:26,169 INFO     Generated 10000 subclasses
2026-01-13 22:33:26,183 INFO     DynamicModel0.__mro__=(<class '__main__.DynamicModel0'>, <class '__main__.AWSCloudContainer'>, <class '__main__.CloudContainer'>, <class '__main__.Container'>, <class '__main__.Component'>, <class 'pydantic.main.BaseModel'>, <class '__main__.VersionMetadata'>, <class '__main__.AuthorMetadata'>, <class 'object'>)
2026-01-13 22:33:26,183 INFO     DynamicModel0.__bases__=(<class '__main__.AWSCloudContainer'>,)
```

## Profiling

```bash
uv run pytest --profile
uv run snakeviz prof/combined.prof
```

![alt text](docs/images/snakeviz_table.png)

![alt text](docs/images/snakeviz_icicle.png)

## Analysis

From the profile you can see `collect_model_fields` being high because it uses `get_model_type_hints`. `get_model_type_hints` then uses `obj.__mro__` to eval every annotation for every base class.

This means when there are lots of pydantic classes with a large hierarchy of bare classes, private attributes, class attributes or public attributes it is repeatedly scanning the hierarchy tree every single time.