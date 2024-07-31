
---

# JsonModeler

JsonModeler is a tool that converts JSON data into model code in multiple programming languages, including C++, C#, Dart, Go, Java, JavaScript, Kotlin, Objective-C, PHP, Python, Swift, and TypeScript.

# Project structure

```
JsonModeler/
├── jsonmodeler/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── json_parser.py      # JSON parser
│   ├── model_generator.py  # Model generator main interface
│   ├── languages/          # Each language support module
│   │   ├── __init__.py
│   │   ├── base.py         # Basic language generator class
│   │   ├── cpp.py          # C++ Model Builder
│   │   ├── csharp.py       # C# Model Builder
│   │   ├── python.py       # Python Model Builder
│   │   └── ...             # Other language generators
├── tests/
│   ├── __init__.py
│   ├── test_json_parser.py
│   ├── test_model_generator.py
│   └── ...               # Other tests
├── scripts/
│   ├── __init__.py
│   ├── convert.py        # Command line tools
│   └── ...               # Other scripts
├── README.md
├── README_Chinese.md
└── setup.py
```

## Installation

You can install JsonModeler using pip:

```bash
pip install jsonmodeler
```

## Usage

### Command Line

To use the command-line tool, you can run:

```bash
jsonmodeler [options]
```

You can use the `--help` option to view all available command line options:

```bash
jsonmodeler --help
```

### Example

Here's an example of how to use command line tools to convert JSON data into Python model code:

```bash
jsonmodeler example.json -l python -o output.py
```

Here's an example of how to use JsonModeler in your Python code:

```python
from jsonmodeler.config import Config
from jsonmodeler.json_parser import JSONParser
from jsonmodeler.model_generator import ModelGenerator

# Example usage
config = Config(input_language='json', output_language='python')
generator = ModelGenerator(config)
model_code = generator.generate({
    "Person": {
        "name": "John",
        "age": 30,
        "is_student": False
    }
})
print(model_code)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
