# intl_vika

intl_vika 是一个用vika的表格来管理多语言资源的工具.  可以使用到web、flutter、iOS、Android的项目中，配合维格表非常快速高效的维护多语言

![int_vika.png](./images/int_vika.png)

支持导出的格式

- json

- strings

- xml

- [todo] sql

## 为什么要开发

最初的原因不愿意花钱，Locale在线管理工具太贵了。于是想想有什么可以替代方案，一开始打算使用google-sheet、aritable来维护，由于墙和API的不稳定性，遂放弃了。正好看到国内的维格表支持API，本身表格共享、多人同步、编辑历史、API都支持，正好满足我Locale的使用，于是基于维格表API开发一个Python命令行工具。

## 用法

运行命令在所需的目录，将会生成一系列语言文件

```shell
> python intl_vika/main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

  intl_vika 是一个用vika的表格来管理多语言资源的工具

  模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M

Options:
  --help  Show this message and exit.

Commands:
  json     json格式编码 (Web、Flutter)
  sql      [Todo] sql格式编码
  strings  strings格式编码 (iOS)
  xml      xml格式编码 (Android)
```

## 表格例子

[维格表的模板](https://vika.cn/share/shrotLJ6naeinkBELMH3M)

| Key `[code=key]` | Chinese `[code=zh]` | English `[code=en]`            | Japanese `[code=ja]` |
| ---------------- | ------------------- | ------------------------------ | -------------------- |
| hello            | 你好                  | hello                          | こんにちは                |
| world            | 世界                  | world                          | 世界                   |
| home.message     | 今天天气如何？             | How is the weather like today? | 今日の天気はどうですか？         |

### json 格式命令

```shell
python3 intl_vika/main.py json --token=填写你的token --sheet=填写你的sheetid --output-dir=./example/json/
# 输出格式
example/json
├── en.json
├── ja.json
└── zh.json
```

### strings 格式命令

```shell
python3 intl_vika/main.py strings --token=填写你的token --sheet=填写你的sheetid --output-dir=./example/strings/
# 输出格式
.
├── en.lproj
│   └── Localizable.strings
└── zh-Hans.lproj
    └── Localizable.strings
```

### xml 格式命令

```shell
python3 intl_vika/main.py xml --token=填写你的token --sheet=填写你的sheetid --output-dir=./example/xml/
# 输出格式
example/xml
├── en.xml
├── ja.xml
└── zh.xml
```

## 元数据

表格中需要解析的列，必须包含以下的格式

### 表头支持的格式

| `[code=key]`      | 标识存储key的列 |
| ----------------- | --------- |
| `[code={Locale}]` | 标识存储本地化的列 |

### Code={key} 列的数据

JSON 模式 key默认支持以点分割，导出的时候以map嵌套的方式展开

```
{"hello.world" : "hello world!"}
=>
{"hello": {"world": "hello world!"}} 
```
