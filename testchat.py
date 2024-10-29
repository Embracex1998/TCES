import csv
import time
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="your zhipuai api key",  # 请替换为您的API密钥
    base_url="http://localhost:8000/v1"
)

# 定义两个模型的名称
model1 = "/mnt/af0931a4-88fe-4e4d-86ed-54f4a275dad4/gutai/vllm_test/glm-4-9b-chat"  # 替换为模型1的名称
model2 = "falv"  # 替换为模型2的名称

# 定义十个问题
questions = [
    "中国法院在民事案件中常见的裁定理由有哪些？",
    "申请人应如何提供财产担保以解除对财产的查封？",
    "在执行程序中，申请人发现被执行人无财产可供执行时，可以采取哪些法律措施？",
    "法院在何种情况下会按撤诉处理案件？",
    "民事诉讼中，缺席审判的适用条件和后果是什么？",
    "人民检察院对民事裁判提起抗诉的程序是怎样的？",
    "财产保全措施在民事诉讼中起到什么作用？",
    "如何理解法院裁定书中的“本裁定送达后即发生法律效力”？",
    "当事人对生效判决不服，发现新证据后应如何申请再审？",
    "民事案件中，审判员和书记员的职责分别是什么？"
]

# 函数：向指定模型发送问题并获取回答
def get_response(model_name, question):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model=model_name,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"出错：{e}"

# 创建CSV文件并写入标题行
with open('model_comparison.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['问题', '模型1回答', '模型2回答'])

    # 遍历问题列表
    for question in questions:
        print(f"正在处理问题：{question}")
        # 获取模型1的回答
        answer1 = get_response(model1, question)
        # 等待一段时间，避免请求过快
        time.sleep(1)
        # 获取模型2的回答
        answer2 = get_response(model2, question)
        # 等待一段时间
        time.sleep(1)
        # 将结果写入CSV文件
        csvwriter.writerow([question, answer1, answer2])

print("对比完成，结果已保存到 model_comparison.csv 文件中。")
