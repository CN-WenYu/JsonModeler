import unittest
from jsonmodeler.config import Config
from jsonmodeler.json_parser import JSONParser
from jsonmodeler.model_generator import ModelGenerator


class TestModelGenerator(unittest.TestCase):
    def setUp(self):
        # 准备一些测试数据
        self.valid_json = {
            "Person": {
                "name": "John",
                "age": 30,
                "is_student": False
            },
            "Address": {
                "street": "123 Main St",
                "city": "Anytown"
            }
        }

    def test_generate_objc(self):
        config = Config(input_language='json', output_language='objc')
        generator = ModelGenerator(config)
        model_code = generator.generate(self.valid_json)
        expected_code = (
            "@interface Person : NSObject\n\n"
            "@property (nonatomic, strong) NSString *name;\n"
            "@property (nonatomic, strong) NSNumber *age;\n"
            "@property (nonatomic, assign) BOOL is_student;\n"
            "@end\n\n"
            "@interface Address : NSObject\n\n"
            "@property (nonatomic, strong) NSString *street;\n"
            "@property (nonatomic, strong) NSString *city;\n"
            "@end\n\n"
        )

        # 移除额外的空行，以确保输出格式一致
        model_code_lines = [line.strip() for line in model_code.splitlines() if line.strip()]
        expected_code_lines = [line.strip() for line in expected_code.splitlines() if line.strip()]

        self.assertEqual(model_code_lines, expected_code_lines)

    def test_generate_swift(self):
        config = Config(input_language='json', output_language='swift')
        generator = ModelGenerator(config)
        model_code = generator.generate(self.valid_json)
        expected_code = (
            "struct Person {\n"
            "    var name: String\n"
            "    var age: Int\n"
            "    var is_student: Bool\n"
            "}\n\n"
            "struct Address {\n"
            "    var street: String\n"
            "    var city: String\n"
            "}\n\n"
        )
        self.assertEqual(model_code.strip(), expected_code.strip())

    def test_generate_python(self):
        config = Config(input_language='json', output_language='python')
        generator = ModelGenerator(config)
        model_code = generator.generate(self.valid_json)
        expected_code = (
            "class Person:\n"
            "    def __init__(self, name: str, age: int, is_student: bool):\n"
            "        self.name = name\n"
            "        self.age = age\n"
            "        self.is_student = is_student\n"
            "\n\n"
            "class Address:\n"
            "    def __init__(self, street: str, city: str):\n"
            "        self.street = street\n"
            "        self.city = city\n"
            "\n\n"
        )
        self.assertEqual(model_code.strip(), expected_code.strip())


if __name__ == "__main__":
    unittest.main()
