from jsonmodeler.languages.base import BaseGenerator


class JavaGenerator(BaseGenerator):
    @staticmethod
    def generate(parsed_data):
        """
        生成 Java 模型代码。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的 Java 模型代码。
        """

        def map_type(json_type, is_list=False):
            type_mapping = {
                "str": "String",
                "int": "int",
                "float": "double",
                "bool": "boolean",
                "list": "List",
                "dict": "Map<String, Object>"
            }
            if is_list:
                return type_mapping.get(json_type, "Object")
            return type_mapping.get(json_type, "Object")

        def generate_class(name, obj):
            properties = []
            getters_setters = []
            constructor_params = []
            constructor_body = []

            for key, value in obj.items():
                json_type = type(value).__name__
                if json_type == 'dict':
                    class_name = key.capitalize()
                    if class_name not in known_classes:
                        known_classes[class_name] = value
                    properties.append(f"    private {class_name} {key};")
                    getter_setter_type = class_name
                elif json_type == 'list':
                    if value and isinstance(value[0], dict):
                        item_class_name = key.capitalize() + 'Item'
                        if item_class_name not in known_classes:
                            known_classes[item_class_name] = value[0]
                        list_type = f"List<{item_class_name}>"
                    elif value:
                        item_type = map_type(type(value[0]).__name__, is_list=True)
                        list_type = f"List<{item_type}>"
                    else:
                        list_type = "List<Object>"
                    properties.append(f"    private {list_type} {key};")
                    getter_setter_type = list_type
                else:
                    java_type = map_type(json_type)
                    properties.append(f"    private {java_type} {key};")
                    getter_setter_type = java_type

                # Generate getters and setters
                getters_setters.append(f"    public {getter_setter_type} get{key.capitalize()}() {{ return {key}; }}")
                getters_setters.append(f"    public void set{key.capitalize()}({getter_setter_type} {key}) {{ this.{key} = {key}; }}")

                # Prepare constructor parameters and body
                constructor_params.append(f"{getter_setter_type} {key}")
                constructor_body.append(f"        this.{key} = {key};")

            properties_str = "\n".join(properties)
            getters_setters_str = "\n".join(getters_setters)
            constructor_params_str = ", ".join(constructor_params)
            constructor_body_str = "\n".join(constructor_body)

            return (f"public class {name} {{\n"
                    f"{properties_str}\n"
                    f"\n"
                    f"    // Getters and Setters\n"
                    f"{getters_setters_str}\n"
                    f"\n"
                    f"    public {name}() {{}}\n"
                    f"\n"
                    f"    public {name}({constructor_params_str}) {{\n"
                    f"{constructor_body_str}\n"
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
                            collect_classes(key.capitalize() + "Item", value[0])

        # Start collection from top-level and add a Root class
        root_name = "Root"
        collect_classes(root_name, parsed_data)

        # Generate code for all collected classes including the root
        for class_name, class_data in known_classes.items():
            model_code += generate_class(class_name, class_data)
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
    generator = JavaGenerator()
    java_code = generator.generate(parsed_data)
    print(java_code)
