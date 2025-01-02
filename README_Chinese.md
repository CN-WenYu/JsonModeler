
---

# JsonModeler

JsonModeler 是一个将 JSON 数据转换为多种编程语言模型代码的工具，包括 C++、C#、Dart、Go、Java、JavaScript、Kotlin、Objective-C、PHP、Python、Swift、TypeScript。

# 项目结构

```
JsonModeler/
├── jsonmodeler/
│   ├── __init__.py
│   ├── json_modeler.py     # 模型生成器主接口
│   ├── json_parser.py      # JSON 解析器
│   ├── languages/          # 各语言支持模块
│   │   ├── __init__.py
│   │   ├── base.py         # 基础语言生成器类
│   │   ├── cpp.py          # c++ 模型生成器
│   │   ├── csharp.py       # C# 模型生成器
│   │   ├── python.py       # Python 模型生成器
│   │   └── ...             # 其他语言生成器
├── tests/
│   ├── __init__.py
│   ├── test_json_parser.py  # JSON 解析器测试
│   ├── test_model_generator.py # 模型生成器测试
│   └── ...               # 其他测试
├── scripts/
│   ├── __init__.py
│   ├── convert.py        # 命令行工具
│   └── ...               # 其他脚本
├── README.md
├── README_Chinese.md
└── setup.py
```

## 安装

您可以使用 pip 安装 JsonModeler：

```bash
pip install jsonmodeler
```

## 用法

### 命令行

要使用命令行工具，您可以运行：

```bash
jsonmodeler [-l <language>] <input_file> [-o <output_file>] [--interactive]
```

- `-l <language>`: 目标编程语言。支持的语言包括 `cpp`、`csharp`、`dart`、`go`、`java`、`js`、`kotlin`、`objc`、`php`、`python`、`swift`、`ts`。
- `<input_file>`: 输入 JSON 文件的路径。如果未提供，工具将从标准输入读取。
- `-o <output_file>`: （可选）输出文件的路径。如果未指定，生成的代码将打印到控制台。
- `--interactive`: 以交互模式运行工具，允许您逐步输入参数。

您可以使用 `--help` 选项查看所有可用的命令行选项：

```bash
jsonmodeler --help
```

### 示例

以下是如何使用命令行工具将 JSON 数据转换为 Python 模型代码的示例：

```bash
jsonmodeler -l python example.json -o output.py
```

### 在 Python 代码中使用

以下是如何在 Python 代码中使用 JsonModeler 的示例：

```python
from jsonmodeler.json_modeler import JsonModeler, Language

# 使用示例
model_code = JsonModeler.generate(Language.PYTHON, {
    "Person": {
        "name": "John",
        "age": 30,
        "is_student": False
    }
})
print(model_code)
```

## 许可证

该项目根据 MIT 许可证授权 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---
