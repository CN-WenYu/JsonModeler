import unittest
from jsonmodeler.json_modeler import JsonModeler, Language


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
        model_code = JsonModeler.generate(Language.OBJC, self.valid_json)
        expected_code = (
            "@interface Root : NSObject\n\n"
            "@property (nonatomic, strong) Person *Person;\n"
            "@property (nonatomic, strong) Address *Address;\n"
            "@end\n\n"
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
        model_code = JsonModeler.generate(Language.SWIFT, self.valid_json)
        expected_code = (
            "struct Root {\n"
            "    var Person: Person\n"
            "    var Address: Address\n"
            "}\n\n"
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
        model_code = JsonModeler.generate(Language.PYTHON, self.valid_json)
        expected_code = (
            "class Root:\n"
            "    def __init__(self, Person: Person, Address: Address):\n"
            "        self.Person = Person\n"
            "        self.Address = Address\n"
            "\n\n"
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
