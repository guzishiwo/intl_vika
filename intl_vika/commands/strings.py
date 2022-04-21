import click

from intl_vika.core import Formater
from intl_vika.core import export_vika_sheet, pick_vkia_sheet


class StringsFormater(Formater):
    def __init__(self, output_dir, table):
        self.table = table
        super().__init__(output_dir)

    def to_file(self, locale):
        dic = self.container[locale]
        # 文件夹格式 例如：en.lproj 、zh-Hans.lproj
        string_dir = f'{locale}.lproj'
        file_path = self.outputh_dir + f'{string_dir}/{self.table}.strings'

        with open(file_path, 'w') as f:
            for key, value in dic.items():
                line = '"{0}" = "{1}";\n'.format(key, value)
                f.write(line)


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--table', default="Localizable", help='iOS Table 名字')
@click.option('--output-dir', required=True, help='zh-Hans.lproj的父目录')
def strings(token, sheet, output_dir, table):
    """
    strings格式编码 (iOS)

    模板参考地址：https://vika.cn/share/shrer6Lqzo6KUgLCN2deb
    """

    sheet = pick_vkia_sheet(token, sheet)
    formater = StringsFormater(output_dir, table)
    export_vika_sheet(sheet, formater)
