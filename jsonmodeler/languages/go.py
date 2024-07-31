from jsonmodeler.languages.base import BaseGenerator


class GoGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 Go 语言模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 Go 语言模型代码。
        """

        def map_type(json_type, is_array_item=False):
            type_mapping = {
                "str": "string",
                "int": "int",
                "float": "float64",
                "bool": "bool",
                "list": "[]",
                "dict": "map[string]interface{}"
            }
            if is_array_item:
                # Return slice with specific type for list items
                return type_mapping.get(json_type, "interface{}")
            return type_mapping.get(json_type, "interface{}")

        def generate_struct(name, obj):
            properties = []
            for key, value in obj.items():
                json_type = type(value).__name__
                go_type = map_type(json_type)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    {key.capitalize()} {class_name} `json:\"{key}\"`")
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + "Item"
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(f"    {key.capitalize()} []{item_class_name} `json:\"{key}\"`")
                    else:
                        element_type = map_type(type(value[0]).__name__) if value else 'interface{}'
                        properties.append(f"    {key.capitalize()} []{element_type} `json:\"{key}\"`")
                else:
                    properties.append(f"    {key.capitalize()} {go_type} `json:\"{key}\"`")

            properties_str = "\n".join(properties)
            return f"type {name} struct {{\n{properties_str}\n}}\n\n"

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

        # Start collection from top-level and add a Root struct
        root_name = "Root"
        collect_classes(root_name, parsed_data)

        # Generate code for all collected structs including the root
        for class_name, class_data in known_classes.items():
            model_code += generate_struct(class_name, class_data)

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
    generator = GoGenerator()
    go_code = generator.generate(parsed_data)
    print(go_code)
