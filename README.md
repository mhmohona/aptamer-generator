# Aptamer Generator

A Python package for generating candidate aptamers using established bioinformatics principles.

## Installation

```bash
pip install git+https://github.com/YOUR_USERNAME/aptamer-generator.git
# Replace YOUR_USERNAME with your GitHub username.
```
Or by downloading it as a zip file, extracting it, and then running `pip install -e .` in the extracted directory.

## Usage
```bash
python -m examples.usage --num-candidates 5 
```

The output will be saved in the `output` folder. 

## Configuration

The package uses a configuration system for flexible parameter setting:
```python
from aptamer_generator.config import Config

config = Config()
config.core.min_length = 20
config.core.max_length = 80
config.sequence.gc_min = 0.3
config.sequence.gc_max = 0.7
```

## Testing

```bash
pytest
```

## Project Structure

````markdown
aptamer-generator/
├── src/
│   ├── aptamer_generator/
│   │   ├── __init__.py
│   │   ├── aptamers.py
│   │   └── utils.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_aptamers.py
│   └── test_utils.py
├── examples/
│   ├── __init__.py
│   └── usage.py
├── .gitignore
├── pyproject.toml
└── setup.py
```
