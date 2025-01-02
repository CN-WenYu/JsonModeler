import argparse
import sys
from jsonmodeler.json_parser import JSONParser
from jsonmodeler.json_modeler import JsonModeler, Language


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON data to model code in various programming languages.",
        usage="jsonmodeler [-l <language>] <input_file> [-o <output_file>] [--interactive]"
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        help="Target language for model code. Choices: cpp, csharp, dart, go, java, js, kotlin, objc, php, python, swift, ts."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs='?',
        help="Path to the input JSON file. If not provided, reads from stdin."
    )
    parser.add_argument(
        "-o", "--output_file",
        type=str,
        help="Path to the output file. Defaults to stdout if not specified."
    )
    parser.add_argument(
        "--interactive",
        action='store_true',
        help="Run in interactive mode."
    )
    args = parser.parse_args()

    if args.interactive:
        run_interactive_mode()
        return

    if not args.language:
        parser.error("the following arguments are required: -l/--language")

    try:
        # 读取并解析 JSON 数据
        if args.input_file:
            parsed_data = JSONParser.from_file(args.input_file)
        else:
            # 从标准输入读取
            json_input = sys.stdin.read()
            parsed_data = JSONParser.parse(json_input)

        # 将命令行选项中的语言字符串映射到枚举常量
        language = Language(args.language)

        # 生成模型代码
        model_code = JsonModeler.generate(language, parsed_data)

        # 输出生成的代码
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(model_code)
            print(f"Model code has been written to {args.output_file}")
        else:
            print(model_code)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def run_interactive_mode():
    print("Interactive mode:")
    language = input("Enter target language (cpp, csharp, dart, go, java, js, kotlin, objc, php, python, swift, ts): ")
    json_input = input("Enter JSON data: ")
    try:
        parsed_data = JSONParser.parse(json_input)
        language_enum = Language(language)
        model_code = JsonModeler.generate(language_enum, parsed_data)
        print("Generated model code:")
        print(model_code)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
