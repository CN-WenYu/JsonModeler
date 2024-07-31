from jsonmodeler.languages.base import BaseGenerator


class SwiftGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 Swift 模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 Swift 模型代码。
        """

        def generate_property(name, type_):
            return f"    var {name}: {type_}"

        def map_type(json_type, is_list=False):
            type_mapping = {
                "str": "String",
                "int": "Int",
                "float": "Double",
                "bool": "Bool",
                "list": "Array",
                "dict": "Dictionary<String, Any>"
            }
            swift_type = type_mapping.get(json_type, "Any")
            return f"Array<{swift_type}>" if is_list else swift_type

        def parse_object(name, obj, known_classes):
            properties = []
            for key, value in obj.items():
                json_type = type(value).__name__
                is_list = json_type == 'list'
                swift_type = map_type(json_type, is_list)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(generate_property(key, class_name))
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + "Item"
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(generate_property(key, f"Array<{item_class_name}>"))
                    else:
                        # Determine the type of list items
                        item_type = "Any"
                        if value:
                            item_type = map_type(type(value[0]).__name__)
                        properties.append(generate_property(key, f"Array<{item_type}>"))
                else:
                    properties.append(generate_property(key, swift_type))
            return "\n".join(properties)

        def generate_class_code(name, obj):
            code = f"struct {name} {{\n"
            code += parse_object(name, obj, known_classes)
            code += "\n}\n\n"
            return code

        # Initialize
        model_code = ""
        known_classes = {}

        # Collect all classes from the root object
        def collect_classes(name, obj):
            if isinstance(obj, dict):
                class_name = name
                if class_name not in known_classes:
                    known_classes[class_name] = obj
                    for key, value in obj.items():
                        if isinstance(value, dict):
                            collect_classes(key.capitalize(), value)
                        elif isinstance(value, list) and value and isinstance(value[0], dict):
                            collect_classes(key.capitalize() + "Item", value[0])

        # Start collection from top-level and add a Root class
        root_name = "Root"
        collect_classes(root_name, parsed_data)

        # Generate code for all collected classes including the root
        for class_name, class_data in known_classes.items():
            model_code += generate_class_code(class_name, class_data)

        return model_code.strip()


if __name__ == "__main__":
    import json

    # 示例 JSON 数据
    json_data = """
    {
        "person": {
            "name": "Alice Smith",
            "age": 30,
            "is_student": false,
            "address": {
                "street": "789 Maple Drive",
                "city": "Springfield",
                "postal_code": "12345"
            },
            "phone_numbers": [
                {
                    "type": "home",
                    "number": "555-555-1234"
                },
                {
                    "type": "work",
                    "number": "555-555-5678"
                }
            ],
            "favorites": ["reading", "hiking", "cooking"],
            "favorites_numbers": [1, 2, 3]
        },
        "message": "Hello, world!",
        "code": 200
    }
    """

    parsed_data = json.loads(json_data)
    generator = SwiftGenerator()
    swift_code = generator.generate(parsed_data)
    print(swift_code)
