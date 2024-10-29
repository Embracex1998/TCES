# 文本续写评测系统 (Text Continuation Evaluation System, TCES)

### TCES 是一个面向大型语言模型（LLM）评估的系统，旨在解决模型对知识掌握和续写能力难以量化的挑战。通过 TCES，可以自动化生成续写内容并进行系统化评估，帮助我们衡量模型在垂直领域的知识掌握程度、逻辑性和内容连贯性。
#### 功能概述
续写内容生成：自动生成续写内容的 CSV 文件，便于数据的批量处理和分析。
    
    基于模型的测试：
        使用 llmbaseapi.py 运行 base 模型 的续写测试。
        使用 llmchatapi.py 运行 chat 模型 的总结性问答。
    评估标准：为特定垂直领域模型的自动化评分建立初步标准，确保在知识掌握和逻辑性方面的精确评估。

### 安装依赖


```
pip install -r requirements.txt
```

### 文件说明

    csvjudge.py:大模型评分脚本.
    testbasepro.txt：包含项目运行的测试命令。
    testbasepro.py：用于生成续写内容的 CSV 文件。
    llmbaseapi.py：用于执行 base 模型的续写测试。
    llmchatapi.py：用于执行 chat 模型的总结性问答。

### 使用说明

#### 运行续写内容生成
使用 testbasepro.py 自动生成续写内容的 CSV 文件，运行命令如下：

```
python testbasepro.py
```
#### Base 模型续写测试
运行 llmbaseapi.py 进行 base 模型的续写测试：

```
python llmbaseapi.py
```

#### Chat 模型总结性问答
运行 llmchatapi.py 进行 chat 模型的总结性问答：

```
python llmchatapi.py
```
#### 使用大模型对回复内容进行打分
运行：
```
python csvjudge.py
```

### 项目结构


```
.
├── requirements.txt       # 项目依赖文件
├── csvjudge.py            # 大模型评分脚本
├── testbasepro.txt        # 测试命令文件
├── testbasepro.py         # 生成续写内容的脚本
├── llmbaseapi.py          # Base模型续写测试脚本
├── llmchatapi.py          # Chat模型总结性问答脚本
└── README.md              # 项目说明文件
```

### 开发计划

    实现续写内容的自动生成与格式化输出。
    定义和实现自动化评分模块，标准化各领域模型的续写评估。
    不断优化评分算法，以提高在知识掌握和逻辑准确性方面的评价精度。