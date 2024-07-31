from jsonmodeler.languages.base import BaseGenerator


class TSGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 TypeScript 类型定义代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 TypeScript 类型定义代码。
        """

        def map_type(json_type):
            type_mapping = {
                "str": "string",
                "int": "number",
                "float": "number",
                "bool": "boolean",
                "list": "Array<any>",  # 默认类型
                "dict": "Record<string, any>"
            }
            return type_mapping.get(json_type, "any")

        def generate_class(name, obj):
            properties = []
            for key, value in obj.items():
                json_type = type(value).__name__
                ts_type = map_type(json_type)

                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    {key}: {class_name};")
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        properties.append(f"    {key}: Array<{item_class_name}>;")
                    else:
                        # Assuming arrays with non-dict items are arrays of constants
                        element_type = map_type(type(value[0]).__name__) if value else 'any'
                        properties.append(f"    {key}: Array<{element_type}>;")
                else:
                    properties.append(f"    {key}: {ts_type};")

            properties_str = "\n".join(properties)
            return f"interface {name} {{\n{properties_str}\n}}\n\n"

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
    generator = TSGenerator()
    ts_code = generator.generate(parsed_data)
    print(ts_code)
