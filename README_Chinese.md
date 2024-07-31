
---

# JsonModeler

JsonModeler 是一个将 JSON 数据转换为多种编程语言模型代码的工具，包括 C++、C#、Dart、Go、Java、JavaScript、Kotlin、Objective-C、PHP、Python、Swift、TypeScript。

# 项目结构

```
JsonModeler/
├── jsonmodeler/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── json_parser.py      # JSON 解析器
│   ├── model_generator.py  # 模型生成器主接口
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
或者使用 brew 安装：

```bash
brew install jsonmodeler
```

## 用法

### 命令行

要使用命令行工具，您可以运行：

```bash
jsonmodeler [options]
```

您可以使用 `--help` 选项查看所有可用的命令行选项：

```bash
jsonmodeler --help
```

### 示例

以下是如何使用命令行工具将 JSON 数据转换为 Python 模型代码的示例：

```bash
jsonmodeler example.json -l python -o output.py
```

以下是如何在 Python 代码中使用 JsonModeler 的示例：

```python
from jsonmodeler.config import Config
from jsonmodeler.json_parser import JSONParser
from jsonmodeler.model_generator import ModelGenerator

# 创建配置对象
config = Config(input_language='json', output_language='python')

# 创建模型生成器对象
generator = ModelGenerator(config)

# 生成模型代码
model_code = generator.generate({
    "Person": {
        "name": "John",
        "age": 30,
        "is_student": False
    }
})

# 打印生成的模型代码
print(model_code)
```

## 许可证

该项目根据 MIT 许可证授权 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---