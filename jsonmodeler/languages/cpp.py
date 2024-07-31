from jsonmodeler.languages.base import BaseGenerator


class CPPGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 C++ 类定义代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 C++ 类定义代码。
        """

        def map_type(json_type, is_array_item=False):
            type_mapping = {
                "str": "std::string",
                "int": "int",
                "float": "float",
                "bool": "bool",
                "list": "std::vector",  # 默认类型
                "dict": "std::unordered_map<std::string, std::any>"
            }
            if is_array_item:
                # Return vector with specific type for list items
                return type_mapping.get(json_type, "std::any")
            return type_mapping.get(json_type, "std::any")

        def generate_class(name, obj):
            properties = []
            for key, value in obj.items():
                json_type = type(value).__name__
                is_array_item = json_type == 'list' and value and isinstance(value[0], (dict, list))
                cpp_type = map_type(json_type, is_array_item)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    {class_name} {key};")
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + "Item"
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(f"    std::vector<{item_class_name}> {key};")
                    else:
                        # Determine type for list elements
                        element_type = map_type(type(value[0]).__name__) if value else 'std::any'
                        properties.append(f"    std::vector<{element_type}> {key};")
                else:
                    properties.append(f"    {cpp_type} {key};")

            properties_str = "\n".join(properties)
            return f"class {name} {{\npublic:\n{properties_str}\n}};\n\n"

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
                        elif isinstance(value, list) and value and isinstance(value[0], (dict, list)):
                            collect_classes(key.capitalize() + "Item", value[0])

        # Start collection from top-level and add a Root class
        root_name = "Root"
        collect_classes(root_name, parsed_data)

        # Generate code for all collected classes
        # Generate declarations first
        for class_name in known_classes:
            model_code += f"class {class_name};\n"
        model_code += "\n"

        # Generate definitions
        for class_name, class_data in known_classes.items():
            model_code += generate_class(class_name, class_data)

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
    generator = CPPGenerator()
    cpp_code = generator.generate(parsed_data)
    print(cpp_code)
