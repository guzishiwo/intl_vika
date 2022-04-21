# intl_vika

intl_vika 是一个用vika的表格来管理多语言资源的工具

## 用法

运行命令在所需的目录，将会生成一系列语言文件

```shell
> python main.py --help

Usage: main.py [OPTIONS]

  intl_vika 是一个用vika的表格来管理多语言资源的工具

  模板参考地址：https://vika.cn/share/shrotLJ6naeinkBELMH3M

Options:
  -t, --token TEXT   维格表API Token  [required]
  -s, --sheet TEXT   维格表 id  [required]
  --output-dir TEXT  导出json文件的路径  [required]
  --indent INTEGER   导出json文件的路径
  --help             Show this message and exit.
```

## 表格例子

[维格表的模板](https://vika.cn/share/shrotLJ6naeinkBELMH3M)

| Key `[code=key]` | Chinese `[code=zh]` | English `[code=en]`            | Japanese `[code=ja]` |
| ---------------- | ------------------- | ------------------------------ | -------------------- |
| hello            | 你好                  | hello                          | こんにちは                |
| world            | 世界                  | world                          | 世界                   |
| home.message     | 今天天气如何？             | How is the weather like today? | 今日の天気はどうですか？         |

运行下面的命令

```shell
python3 intl_vika/main.py --token=填写你的token --sheet=填写你的sheetid --output-dir=./example
```

```shell
example
├── en.json
├── ja.json
└── zh.json
```

## 元数据

表格中需要解析的列，必须包含以下的格式

### 表头支持的格式

| `[code=key]`      | 标识存储key的列    |
| ----------------- | ------------ |
| `[code={Locale}]` | 标识存储本地化的列|

### Code={key} 列的数据
key默认支持以点分割，导出的时候以map嵌套的方式展开
```
{"hello.world" : "hello world!"}
=>
{"hello": {"world": "hello world!"}}
```
