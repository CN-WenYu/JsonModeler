class Config:
    def __init__(self, output_language: str):
        """
        初始化配置类。
        :param output_language: 输出语言类型（如 'objc', 'swift' 等）。
        """
        self.output_language = output_language

    def __repr__(self):
        """
        返回配置类的字符串表示形式。
        """
        return f"Config(output_language='{self.output_language}')"
