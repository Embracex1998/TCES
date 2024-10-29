import json
import csv
import random
import time
import argparse
from openai import OpenAI

def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    contents = [item['content'] for item in data]
    return contents

def select_data(contents, mode, N):
    if mode == 'random':
        if N > len(contents):
            N = len(contents)
        selected = random.sample(contents, N)
    elif mode == 'first':
        selected = contents[:N]
    elif mode == 'all':
        selected = contents
    else:
        raise ValueError("模式应为 'random'、'first' 或 'all'")
    return selected

def truncate_text(text, percentages):
    truncations = []
    length = len(text)
    for p in percentages:
        idx = int(length * p)
        truncated = text[:idx]
        truncations.append((p, truncated))
    return truncations

def get_continuation(client, model_name, prompt):
    try:
        response = client.completions.create(
            model=model_name,
            prompt=prompt,
            temperature=0.7,
            max_tokens=200,
            top_p=0.9,
            n=1
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"出错：{e}"

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='续写能力测试脚本')
    parser.add_argument('--json_file', type=str, required=True, help='输入的JSON文件路径')
    parser.add_argument('--mode', type=str, choices=['random', 'first', 'all'], default='all', help='数据选择模式')
    parser.add_argument('--num_samples', type=int, default=5, help='随机或前N条数据的N值')
    parser.add_argument('--output_file', type=str, default='continuation_test_results.csv', help='输出的CSV文件名')
    parser.add_argument('--model1', type=str, required=True, help='模型1的名称')
    parser.add_argument('--model2', type=str, required=True, help='模型2的名称')
    parser.add_argument('--api_key', type=str, required=True, help='API密钥')
    parser.add_argument('--api_base', type=str, default='http://localhost:8000/v1', help='API基础URL')
    args = parser.parse_args()
    
    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=args.api_key,
        base_url=args.api_base
    )
    
    # 读取数据
    contents = load_data(args.json_file)
    
    # 根据模式选择数据
    selected_contents = select_data(contents, args.mode, args.num_samples)
    
    # 定义截断百分比
    percentages = [0.2, 0.4, 0.6, 0.8]
    
    # 创建CSV文件并写入标题行
    with open(args.output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['文本编号', '原始文本', '截断百分比', '模型', '续写结果']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 遍历选定的文本
        for idx, text in enumerate(selected_contents):
            print(f"正在处理第 {idx+1} 条文本")
            # 对每个文本进行截断
            truncations = truncate_text(text, percentages)
            for p, truncated_text in truncations:
                # 对截断的文本进行续写，分别使用两个模型
                for model_name in [args.model1, args.model2]:
                    continuation = get_continuation(client, model_name, truncated_text)
                    # 将结果写入CSV
                    writer.writerow({
                        '文本编号': f'文本 {idx+1}',
                        '原始文本': text,
                        '截断百分比': f'{int(p*100)}%',
                        '模型': model_name,
                        '续写结果': continuation
                    })
                    time.sleep(1)  # 避免请求过快

if __name__ == '__main__':
    main()
