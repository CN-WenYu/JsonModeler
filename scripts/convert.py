import argparse
from jsonmodeler.config import Config
from jsonmodeler.json_parser import JSONParser
from jsonmodeler.model_generator import ModelGenerator


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to model code.")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file.")
    parser.add_argument("-l", "--language", type=str, choices=[
        'c++', 'csharp', 'dart', 'go', 'java', 'js', 'kotlin', 'objc', 'php', 'python', 'swift', 'ts'
    ], help="Target programming language for model code "
            "(c++, csharp, dart, go, java, js, kotlin, objc, php, python, swift, ts).")
    parser.add_argument("-o", "--output_file", type=str,
                        help="Path to the output file. If not specified, prints to stdout.")
    args = parser.parse_args()

    try:
        # 读取并解析 JSON 数据
        parsed_data = JSONParser.from_file(args.input_file)

        # 配置生成器
        config = Config(input_language='json', output_language=args.language)
        generator = ModelGenerator(config)

        # 生成模型代码
        model_code = generator.generate(parsed_data)

        # 输出生成的代码
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(model_code)
            print(f"Model code has been written to {args.output_file}")
        else:
            print(model_code)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
