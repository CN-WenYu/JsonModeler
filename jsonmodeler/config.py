class Config:
    def __init__(self, input_language: str, output_language: str):
        """
        初始化配置类。

        :param input_language: 输入语言类型（通常是 'json'）。
        :param output_language: 输出语言类型（如 'objc', 'swift' 等）。
        """
        self.input_language = input_language
        self.output_language = output_language

    def __repr__(self):
        """
        返回配置类的字符串表示形式。
        """
        return f"Config(input_language='{self.input_language}', output_language='{self.output_language}')"
