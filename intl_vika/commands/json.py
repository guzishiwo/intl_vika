import click
from json import dump as json_dump
from collections import OrderedDict
from intl_vika.core import Formater
from intl_vika.core import export_vika_sheet, pick_vkia_sheet


class JSONFormater(Formater):
    def __init__(self, output_dir, indent):
        self.indent = indent
        super().__init__(output_dir)

    def to_file(self, locale):
        dic = self.container[locale]
        local_data = self.transform(dic)
        file_path = self.outputh_dir + locale + '.json'

        with open(file_path, 'w') as f:
            json_dump(local_data, f, ensure_ascii=False, indent=self.indent)

    def transform(self, dic):
        """ 把key转换成dict嵌套的格式

        Args:
            dic: OrderDict() 保持新增的顺序
            example: {"hello.world" : "hello world!"}

        Returns:
            dict: {"hello": {"world": "hello world!"}}
        """
        order_dict = OrderedDict()
        for key, value in dic.items():
            keys = key.split('.')
            length = len(keys) - 1
            inner_dict = order_dict
            for idx, k in enumerate(keys):
                if idx == length:
                    inner_dict[k] = value
                else:
                    guess = inner_dict.get(k)
                    # 提前创建
                    if type(guess) != OrderedDict:
                        inner_dict[k] = OrderedDict()
                    inner_dict = inner_dict[k]

        return order_dict


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--output-dir', required=True, help='导出文件的路径')
@click.option('--indent', default=4, help='导出json的缩进长度')
def json(token, sheet, output_dir, indent):
    """
    json格式编码 (Web、Flutter)

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """
    sheet = pick_vkia_sheet(token, sheet)
    formatter = JSONFormater(output_dir, indent)
    export_vika_sheet(sheet, formatter)
