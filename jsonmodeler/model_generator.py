from jsonmodeler.config import Config
from jsonmodeler.languages.base import BaseGenerator


class ModelGenerator:
    def __init__(self, config: Config):
        """
        初始化模型生成器。

        :param config: 配置对象，指定输入语言和输出语言。
        """
        self.config = config
        self.language_map = {
            'c++': 'cpp',
            'csharp': 'c#',
            'c#': 'c#',
            'c-sharp': 'c#',
            'csharp.net': 'c#',
            'objectivec': 'objc',
            'objective-c': 'objc',
            'objc': 'objc',
            'oc': 'objc',
            'dart': 'dart',
            'go': 'go',
            'java': 'java',
            'js': 'js',
            'javascript': 'js',
            'kotlin': 'kotlin',
            'php': 'php',
            'python': 'python',
            'swift': 'swift',
            'typescript': 'ts',
            'ts': 'ts'
        }

    def generate(self, parsed_data):
        """
        生成目标语言的模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的模型代码。
        :raises ValueError: 如果输出语言不支持，则抛出 ValueError 异常。
        """
        language = self.language_map.get(self.config.output_language.lower(), None)

        if language is None:
            raise ValueError(f"Unsupported output language: {self.config.output_language}")

        if language == 'cpp':
            from jsonmodeler.languages.cpp import CPPGenerator
            return CPPGenerator.generate(parsed_data)
        elif language == 'c#':
            from jsonmodeler.languages.csharp import CSharpGenerator
            return CSharpGenerator.generate(parsed_data)
        elif language == 'dart':
            from jsonmodeler.languages.dart import DartGenerator
            return DartGenerator.generate(parsed_data)
        elif language == 'go':
            from jsonmodeler.languages.go import GoGenerator
            return GoGenerator.generate(parsed_data)
        elif language == 'java':
            from jsonmodeler.languages.java import JavaGenerator
            return JavaGenerator.generate(parsed_data)
        elif language == 'js':
            from jsonmodeler.languages.js import JSGenerator
            return JSGenerator.generate(parsed_data)
        elif language == 'kotlin':
            from jsonmodeler.languages.kotlin import KotlinGenerator
            return KotlinGenerator.generate(parsed_data)
        elif language == 'objc':
            from jsonmodeler.languages.objc import ObjCGenerator
            return ObjCGenerator.generate(parsed_data)
        elif language == 'php':
            from jsonmodeler.languages.php import PHPGenerator
            return PHPGenerator.generate(parsed_data)
        elif language == 'python':
            from jsonmodeler.languages.python import PythonGenerator
            return PythonGenerator.generate(parsed_data)
        elif language == 'swift':
            from jsonmodeler.languages.swift import SwiftGenerator
            return SwiftGenerator.generate(parsed_data)
        elif language == 'ts':
            from jsonmodeler.languages.ts import TSGenerator
            return TSGenerator.generate(parsed_data)
        else:
            raise ValueError(f"Unsupported output language: {self.config.output_language}")
