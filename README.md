
---

# JsonModeler

JsonModeler is a tool that converts JSON data into model code in multiple programming languages, including C++, C#, Dart, Go, Java, JavaScript, Kotlin, Objective-C, PHP, Python, Swift, and TypeScript.

# Project structure

```
JsonModeler/
├── jsonmodeler/
│   ├── __init__.py
│   ├── json_modeler.py     # Model generator main interface
│   ├── json_parser.py      # JSON parser
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
jsonmodeler [-l <language>] <input_file> [-o <output_file>] [--interactive]
```

- `-l <language>`: Target programming language for model code. Supported languages include `cpp`, `csharp`, `dart`, `go`, `java`, `js`, `kotlin`, `objc`, `php`, `python`, `swift`, `ts`.
- `<input_file>`: Path to the input JSON file. If not provided, the tool will read from standard input.
- `-o <output_file>`: (Optional) Path to the output file. If not specified, the generated code will be printed to the console.
- `--interactive`: Run the tool in interactive mode, allowing you to input parameters step-by-step.

You can use the `--help` option to view all available command line options:

```bash
jsonmodeler --help
```

### Examples

#### Convert JSON to Python Model Code

```bash
jsonmodeler -l python example.json -o output.py
```

This command converts the JSON data in `example.json` to Python model code and writes it to `output.py`.

#### Convert JSON to Java Model Code and Print to Console

```bash
jsonmodeler -l java example.json
```

This command converts the JSON data in `example.json` to Java model code and prints the result to the console.

#### Interactive Mode

```bash
jsonmodeler --interactive
```

This command starts the tool in interactive mode, allowing you to input the target language and JSON data directly.

### Using in Python Code

Here's an example of how to use JsonModeler in your Python code:

```python
from jsonmodeler.json_modeler import JsonModeler, Language

# Example usage
model_code = JsonModeler.generate(Language.PYTHON, {
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
