import re
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


class Formater:
    def __init__(self, output_dir):
        self.container = defaultdict(OrderedDict)
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
    
    def to_file(self, _):
        raise NotImplementedError()



class Intl:
    def __init__(self, header, formater):
        self.header = header
        self.formater = formater

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
                self.formater.add_item(local_code, key, text)


def pick_vkia_sheet(token, sheet_id):
    vika = Vika(token)
    datasheet = vika.datasheet(sheet_id)
    return datasheet

def export_vika_sheet(vika_sheet, formater):
    header = IntlHeader.from_vika_fields(vika_sheet.fields)
    intl = Intl(header, formater)

    records = vika_sheet.records.all()
    for record in records:
        intl.add_record(record.json())

    intl.formater.to_files()
