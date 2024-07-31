from jsonmodeler.languages.base import BaseGenerator


class CSharpGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 C# 模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 C# 模型代码。
        """

        def map_type(json_type, class_name=None):
            type_mapping = {
                "str": "string",
                "int": "int",
                "float": "double",
                "bool": "bool",
                "list": "List",
                "dict": f"{class_name}" if class_name else "Dictionary<string, object>"
            }
            return type_mapping.get(json_type, "object")

        def generate_class(name, obj):
            properties = []
            constructor_params = []

            for key, value in obj.items():
                json_type = type(value).__name__
                cs_type = map_type(json_type, class_name=name)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    cs_type = class_name
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        cs_type = f"List<{item_class_name}>"
                    else:
                        element_type = map_type(type(value[0]).__name__) if value else 'string'
                        cs_type = f"List<{element_type}>"

                properties.append(f"    public {cs_type} {key} {{ get; set; }}")

                # Add constructor params
                constructor_params.append(f"{cs_type} {key}")

            constructor_params_str = ", ".join(constructor_params)
            constructor_body = "\n".join([f"        this.{key} = {key};" for key in obj.keys()])

            class_definition = (
                "public class {name} {{\n"
                "{properties_str}\n"
                "\n"
                "    public {name}() {{}}\n"
                "\n"
                "    public {name}({constructor_params_str}) {{\n"
                "{constructor_body}\n"
                "    }}\n"
                "}}\n\n"
            ).format(
                name=name,
                properties_str='\n'.join(properties),
                constructor_params_str=constructor_params_str,
                constructor_body=constructor_body
            )

            return class_definition

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
    generator = CSharpGenerator()
    cs_code = generator.generate(parsed_data)
    print(cs_code)
