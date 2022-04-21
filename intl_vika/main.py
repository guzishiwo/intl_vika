import click
from intl_vika.commands.json import json
from intl_vika.commands.strings import strings
from intl_vika.commands.xml import xml
from intl_vika.commands.sql import sql

@click.group()
def cli():
    """
    intl_vika 是一个用vika的表格来管理多语言资源的工具 

    模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M
    """
    pass

cli.add_command(json)
cli.add_command(strings)
cli.add_command(xml)
cli.add_command(sql)

if __name__ == '__main__':
    cli()
