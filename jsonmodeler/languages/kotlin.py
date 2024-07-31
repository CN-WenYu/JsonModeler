from jsonmodeler.languages.base import BaseGenerator


class KotlinGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 Kotlin 数据类代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 Kotlin 数据类代码。
        """

        def map_type(json_type):
            type_mapping = {
                "str": "String",
                "int": "Int",
                "float": "Double",
                "bool": "Boolean",
                "list": "List",
                "dict": "Map<String, Any>"
            }
            return type_mapping.get(json_type, "Any")

        def generate_data_class(name, obj):
            properties = []
            for key, value in obj.items():
                json_type = type(value).__name__
                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    val {key}: {class_name}? = null")
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(f"    val {key}: List<{item_class_name}>? = null")
                    else:
                        item_type = map_type('str')
                        if isinstance(value[0], int):
                            item_type = "Int"
                        elif isinstance(value[0], float):
                            item_type = "Double"
                        elif isinstance(value[0], bool):
                            item_type = "Boolean"
                        properties.append(f"    val {key}: List<{item_type}>? = null")
                else:
                    kotlin_type = map_type(json_type)
                    properties.append(f"    val {key}: {kotlin_type}? = null")

            properties_str = "\n".join(properties)
            return (f"data class {name} (\n"
                    f"{properties_str}\n"
                    f")\n\n")

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
                            collect_classes(key.capitalize() + 'Item', value[0])

        # Start collection from top-level and add a Root class
        root_name = "Root"
        collect_classes(root_name, parsed_data)

        # Generate code for all collected classes including the root
        for class_name, class_data in known_classes.items():
            model_code += generate_data_class(class_name, class_data)
            model_code += "\n"

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
    generator = KotlinGenerator()
    kotlin_code = generator.generate(parsed_data)
    print(kotlin_code)
