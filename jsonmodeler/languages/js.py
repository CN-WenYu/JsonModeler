from jsonmodeler.languages.base import BaseGenerator


class JSGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 JavaScript 数据类代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 JavaScript 数据类代码。
        """

        def map_type(json_type):
            type_mapping = {
                "str": "string",
                "int": "number",
                "float": "number",
                "bool": "boolean",
                "list": "Array",
                "dict": "object"
            }
            return type_mapping.get(json_type, "any")

        def generate_class(name, obj):
            properties = []
            constructor_params = []

            for key, value in obj.items():
                json_type = type(value).__name__
                js_type = map_type(json_type)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    this.{key} = {key};")
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(f"    this.{key} = {key};")
                    else:
                        properties.append(f"    this.{key} = {key};")
                else:
                    properties.append(f"    this.{key} = {key};")

                # Add constructor params
                constructor_params.append(f"{key}")

            constructor_params_str = ", ".join(constructor_params)
            constructor_body = "\n".join([f"        this.{key} = {key};" for key in obj.keys()])

            return (f"class {name} {{\n"
                    f"    constructor({constructor_params_str}) {{\n"
                    f"{constructor_body}\n"
                    f"    }}\n"
                    f"}}\n\n")

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
    generator = JSGenerator()
    js_code = generator.generate(parsed_data)
    print(js_code)
