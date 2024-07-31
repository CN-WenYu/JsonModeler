import json


class JSONParser:
    @staticmethod
    def parse(json_data: str):
        """
        解析 JSON 数据。

        :param json_data: 字符串格式的 JSON 数据。
        :return: 解析后的 Python 字典。
        :raises ValueError: 如果 JSON 数据无效，则抛出 ValueError 异常。
        """
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")

    @staticmethod
    def from_file(file_path: str):
        """
        从文件中读取并解析 JSON 数据。

        :param file_path: JSON 文件的路径。
        :return: 解析后的 Python 字典。
        :raises ValueError: 如果文件读取失败或 JSON 数据无效，则抛出 ValueError 异常。
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = file.read()
                return JSONParser.parse(json_data)
        except (IOError, OSError) as e:
            raise ValueError(f"Error reading file {file_path}: {e}")
