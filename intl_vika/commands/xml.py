import click

from intl_vika.core import Formater
from intl_vika.core import export_vika_sheet, pick_vkia_sheet


class XMLFormatter(Formater):
    def __init__(self, output_dir):
        super().__init__(output_dir)

    def to_file(self, locale):
        raise NotImplementedError


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--output-dir', required=True, help='导出文件的路径')
def xml(token, sheet_id, output_dir):
    """
    [todo] xml格式编码 (Android)

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """

    sheet = pick_vkia_sheet(token, sheet_id)
    formatter = XMLFormatter(output_dir)
    export_vika_sheet(sheet, formatter)
