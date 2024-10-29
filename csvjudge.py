from openai import OpenAI
import csv
import pandas as pd
import time

def load_results(csv_file):
    """
    从CSV文件中加载续写测试结果数据。
    """
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return pd.DataFrame(data)

def score_with_model(text, continuation, api_key):
    """
    使用大模型对续写的准确性和逻辑性进行评分。
    """
    prompt = f"原文：{text}\n\n续写：{continuation}\n\n请根据以下标准对续写内容进行评分：\n" \
             "1. 续写准确性（0-10分）：内容是否延续了原文主题，保持了逻辑一致性。\n" \
             "2. 逻辑准确性（0-10分）：续写的内容是否具备合理的逻辑性和连贯性。\n" \
             "请提供准确性和逻辑性的分数以及简单的评分理由。\n" \
             "输出格式如下：续写准确性：x分 \n 逻辑准确性：x分 \n 不要回复任何多余内容！"

    try:
        client = OpenAI(
            api_key=api_key,
            base_url='http://localhost:8000/v1'
        )
        response = client.chat.completions.create(
            model="/mnt/af0931a4-88fe-4e4d-86ed-54f4a275dad4/gutai/vllm_test/glm-4-9b-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        reply = response.choices[0].message.content.strip()
        
        # 从模型回复中提取评分
        accuracy_score = int(reply.split("续写准确性")[1].split("：")[1].split("分")[0].strip())
        logic_score = int(reply.split("逻辑准确性")[1].split("：")[1].split("分")[0].strip())
        
        return accuracy_score, logic_score, reply
    except Exception as e:
        print(e)
        return None, None, f"评分出错：{e}"

def main():
    # 输入API密钥
    api_key = "YOUR_API_KEY"

    # 加载续写结果数据
    csv_file = 'continuation_test_results.csv'
    results_df = load_results(csv_file)
    
    # 准备输出的评分结果
    scores = []

    # 遍历每条续写内容进行评分
    for _, row in results_df.iterrows():
        text = row['原始文本']
        continuation = row['续写结果']

        # 使用大模型进行评分
        accuracy_score, logic_score, model_feedback = score_with_model(text, continuation, api_key)
        
        # 添加到评分结果列表
        scores.append({
            '文本编号': row['文本编号'],
            '模型': row['模型'],
            '截断百分比': row['截断百分比'],
            '续写准确性': accuracy_score,
            '逻辑准确性': logic_score,
            '评分反馈': model_feedback,
            '续写结果': continuation
        })
        
        time.sleep(1)  # 避免API调用过快

    # 保存评分结果到CSV文件
    scored_df = pd.DataFrame(scores)
    scored_df.to_csv('continuation_scores_with_model.csv', index=False, encoding='utf-8')
    print("评分完成，结果已保存到 continuation_scores_with_model.csv")

if __name__ == '__main__':
    main()
