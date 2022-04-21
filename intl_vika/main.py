import re
import json
import click
from vika import Vika
from collections import (
    OrderedDict,
    defaultdict,
)

# Key[code=key] => key
# Key[code=zh] => zh
CODE_EXTRACT_RE = re.compile(r'\[code=(.*)\]')


def extract_code(name):
    if not name:
        return None
    m = CODE_EXTRACT_RE.search(name)
    if not m:
        return None
    return m.group(1)


class IntlField:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.is_key = code == 'key'


class IntlHeader:
    def __init__(self, fields):
        self.fields = fields

    @classmethod
    def from_vika_fields(cls, fields):
        # key => header
        trans_fields = []
        for field in fields:
            name = field.name
            code = extract_code(name)
            if code:
                trans_fields.append(IntlField(code, name))

        return cls(trans_fields)

    def __iter__(self):
        return iter(self.fields)


class I18n:
    def __init__(self, output_dir, indent):
        self.container = defaultdict(OrderedDict)
        self.indent = indent
        self.outputh_dir = output_dir if output_dir.endswith(
            '/') else output_dir + '/'

    def add_item(self, locale_code, key, value):
        self.container[locale_code][key] = value

    def to_files(self):
        """ 生成json文件
        [TODO]: 是否要自动根据路径创建文件夹
        """
        for local_code in self.container.keys():
            self.to_file(local_code)

    def to_file(self, locale):
        dic = self.container[locale]
        local_data = self.transform(dic)
        file_path = self.outputh_dir + locale + '.json'

        with open(file_path, 'w') as f:
            json.dump(local_data, f, ensure_ascii=False, indent=self.indent)

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


class Intl:
    def __init__(self, header, output_dir, indent):
        self.header = header
        self.i18n = I18n(output_dir, indent)

    def add_record(self, record):
        key_field = None
        items = []
        key = None
        for field in self.header:
            if field.name not in record:
                continue
            code = field.code
            text = record[field.name]
            if field.is_key:
                key_field = field
                key = text
            else:
                items.append((code, text))

        if key_field and key:
            for item in items:
                local_code, text = item
                self.i18n.add_item(local_code, key, text)


def run(token, sheet_id, output_dir, indent):
    vika = Vika(token)
    datasheet = vika.datasheet(sheet_id)
    header = IntlHeader.from_vika_fields(datasheet.fields)
    intl = Intl(header, output_dir, indent)

    records = datasheet.records.all()
    for record in records:
        intl.add_record(record.json())

    intl.i18n.to_files()


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--output-dir', required=True, help='导出文件的路径')
@click.option('--indent', default=4, help='导出json的缩进长度')
def cli(token, sheet, output_dir, indent):
    """
    intl_vika 是一个用vika的表格来管理多语言资源的工具 

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """
    run(token, sheet, output_dir, indent)


if __name__ == '__main__':
    cli()
