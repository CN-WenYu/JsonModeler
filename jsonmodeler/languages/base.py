class BaseGenerator:
    @staticmethod
    def generate(parsed_data) -> str:
        """
        生成目标语言的模型代码。这个方法应该在子类中实现。

        :param parsed_data: 解析后的 JSON 数据。
        :return: 生成的模型代码。
        :raises NotImplementedError: 如果子类没有实现该方法，则抛出 NotImplementedError 异常。
        """
        raise NotImplementedError("This method should be overridden by subclasses")
