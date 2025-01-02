from enum import Enum

from jsonmodeler.languages.cpp import CPPGenerator
from jsonmodeler.languages.csharp import CSharpGenerator
from jsonmodeler.languages.dart import DartGenerator
from jsonmodeler.languages.go import GoGenerator
from jsonmodeler.languages.java import JavaGenerator
from jsonmodeler.languages.js import JSGenerator
from jsonmodeler.languages.kotlin import KotlinGenerator
from jsonmodeler.languages.objc import ObjCGenerator
from jsonmodeler.languages.php import PHPGenerator
from jsonmodeler.languages.python import PythonGenerator
from jsonmodeler.languages.swift import SwiftGenerator
from jsonmodeler.languages.ts import TSGenerator


class Language(Enum):
    CPP = 'cpp'
    CSHARP = 'c#'
    DART = 'dart'
    GO = 'go'
    JAVA = 'java'
    JS = 'js'
    KOTLIN = 'kotlin'
    OBJC = 'objc'
    PHP = 'php'
    PYTHON = 'python'
    SWIFT = 'swift'
    TYPESCRIPT = 'ts'

class JsonModeler:
    generator_map = {
        Language.CPP: CPPGenerator,
        Language.CSHARP: CSharpGenerator,
        Language.DART: DartGenerator,
        Language.GO: GoGenerator,
        Language.JAVA: JavaGenerator,
        Language.JS: JSGenerator,
        Language.KOTLIN: KotlinGenerator,
        Language.OBJC: ObjCGenerator,
        Language.PHP: PHPGenerator,
        Language.PYTHON: PythonGenerator,
        Language.SWIFT: SwiftGenerator,
        Language.TYPESCRIPT: TSGenerator
    }

    @staticmethod
    def generate(language: Language, parsed_data):
        """
        生成目标语言的模型代码。

        :param language: 语言类型
        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的模型代码。
        :raises ValueError: 如果输出语言不支持，则抛出 ValueError 异常。
        """

        if language is None:
            raise ValueError(f"Unsupported output language: {language}")

        generator_class = JsonModeler.generator_map.get(language)
        if generator_class is None:
            raise ValueError(f"Unsupported output language: {language}")

        # 处理已解析的数组
        if isinstance(parsed_data, list):
            # 如果顶层是一个列表，则将其包装在带有通用键的字典中
            parsed_data = {"RootArray": parsed_data}

        return generator_class.generate(parsed_data)
