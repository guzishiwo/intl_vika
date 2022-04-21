import click

from intl_vika.core import Formater
from intl_vika.core import export_vika_sheet, pick_vkia_sheet


class SQLFormater(Formater):
    def __init__(self, output_dir, indent):
        self.indent = indent
        super().__init__(output_dir)

    def to_file(self, locale):
        """
        [todo]: 增加导出sql给后端
        """
        raise NotImplementedError


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--output-dir', required=True, help='导出文件的路径')
def sql(token, sheet_id, output_dir):
    """
    [Todo] sql格式编码

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """

    sheet = pick_vkia_sheet(token, sheet_id)
    formatter = SQLFormatter(output_dir)
    export_vika_sheet(sheet, formatter)
