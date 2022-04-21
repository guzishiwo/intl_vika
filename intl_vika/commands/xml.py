import click

from intl_vika.core import Formater
from intl_vika.core import export_vika_sheet, pick_vkia_sheet
from xml.dom import minidom


class XMLFormatter(Formater):
    def __init__(self, output_dir):
        super().__init__(output_dir)

    def to_file(self, locale):
        dic = self.container[locale]
        file_path = self.outputh_dir + f'{locale}.xml'

        doc = minidom.Document()
        resources = doc.createElement('resources')
        doc.appendChild(resources)
        # 文件夹格式 例如：en.lproj 、zh-Hans.lproj
        with open(file_path, 'w') as f:
            for key, value in dic.items():
                string_ele = doc.createElement('string')
                string_ele.setAttribute('name', key)
                string_ele.appendChild(doc.createTextNode(value))
                resources.appendChild(string_ele)
            f.write(doc.toprettyxml(indent='    '))


@click.command()
@click.option('-t', '--token', required=True, help='维格表API Token')
@click.option('-s', '--sheet', required=True, help='维格表 id')
@click.option('--output-dir', required=True, help='导出文件的路径')
def xml(token, sheet, output_dir):
    """
    xml格式编码 (Android)

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """

    sheet = pick_vkia_sheet(token, sheet)
    formatter = XMLFormatter(output_dir)
    export_vika_sheet(sheet, formatter)
