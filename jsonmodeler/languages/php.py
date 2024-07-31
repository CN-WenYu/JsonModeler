from jsonmodeler.languages.base import BaseGenerator


class PHPGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 PHP 模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 PHP 模型代码。
        """

        def map_type(json_type):
            type_mapping = {
                "str": "string",
                "int": "int",
                "float": "float",
                "bool": "bool",
                "list": "array",
                "dict": "array"  # We will treat all dicts as arrays for PHP
            }
            return type_mapping.get(json_type, "mixed")

        def generate_class(name, obj):
            properties = []
            getters_setters = []
            constructor_params = []
            constructor_body = []

            for key, value in obj.items():
                json_type = type(value).__name__
                php_type = map_type(json_type)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    php_type = class_name
                    php_type_annotation = class_name  # Using class name for dicts
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        php_type = "array"
                        php_type_annotation = f"array<{item_class_name}>"
                    else:
                        php_type = "array"
                        php_type_annotation = "array"
                else:
                    php_type_annotation = php_type

                properties.append(f"    /** @var {php_type_annotation} */\n    private {php_type} ${key};")

                # Generate constructor parameters and body
                constructor_params.append(f"${key}")
                constructor_body.append(f"        $this->{key} = ${key};")

                # Generate getters and setters
                php_get_type = php_type if php_type != 'array' else 'mixed'
                php_set_type = php_type if php_type != 'array' else 'mixed'
                getters_setters.append(f"""
    /**
     * @return {php_get_type}
     */
    public function get{key.capitalize()}() {{
        return $this->{key};
    }}

    /**
     * @param {php_set_type} ${key}
     */
    public function set{key.capitalize()}(${key}: {php_set_type}): void {{
        $this->{key} = ${key};
    }}""")

            properties_str = "\n".join(properties)
            getters_setters_str = "\n".join(getters_setters)
            constructor_params_str = ", ".join(constructor_params)
            constructor_body_str = "\n".join(constructor_body)

            return (f"<?php\n\n"
                    f"class {name} {{\n"
                    f"{properties_str}\n"
                    f"\n"
                    f"    public function __construct({constructor_params_str}) {{\n"
                    f"{constructor_body_str}\n"
                    f"    }}\n"
                    f"\n"
                    f"{getters_setters_str}\n"
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
    generator = PHPGenerator()
    php_code = generator.generate(parsed_data)
    print(php_code)
