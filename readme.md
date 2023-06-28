# cf-contest-bot

*sbqq bot 总是风控或者在风控的路上，不维护了，转到新项目：[Yescafe/cf-summary](https://github.com/Yescafe/cf-summary)。*

可以爬取 Codeforces 和 LeetCode 的一些信息的 QQ Bot。随手写的玩具，想到了什么有能力能加上的会加上，没能力加上的就没能力加上。

## 依赖

下载 <https://github.com/Mrs4s/go-cqhttp> 的 release 解压到本项目根目录下。

按需配置 go-cqhttp，注意要配出 8000 端口的 http server 和 5700 端口的 ws server，参考：

```yaml
servers:
  - http:
      host: 127.0.0.1
      port: 8000
      timeout: 5
      middlewares:
          <<: *default
      post:

  - ws:
      host: 127.0.0.1
      port: 5700
      middlewares:
          <<: *default
```

## 新建 `secret_tokens.py`

在根目录中新建 `secret_tokens.py` 模块，配置以下内容：

```python
# 在哪些群工作
GROUP_ID_LIST = [
    12345,
    12345678,
    114514,
]

OPTIONS = {
    # 管理员 QQ 号
    "admin": [
        7654321,
        1234567,
    ]
}

# cfr 指令会获取以下用户
RATING_LIST = ['giangly', 'dourisd']
```

## 安装 Python 依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python3 main.py
```
