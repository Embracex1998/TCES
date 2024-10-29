import csv
import time
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="your zhipuai api key",  # 请替换为您的API密钥
    base_url="http://localhost:8000/v1"
)

# 定义两个模型的名称
model1 = "falv"       # 替换为模型1的名称
model2 = "/mnt/af0931a4-88fe-4e4d-86ed-54f4a275dad4/gutai/vllm_test/glm-4-9b-chat"  # 替换为模型2的名称

# 定义需要续写的文本列表
texts = [
    """深圳市罗湖区人民法院民 事 裁 定 书（2012）深罗法民二初字第353号原告广发银行股份有限公司深圳分行，住所地深圳市深南东路123号百货广场大厦西座19-22层。负责人杨小舟，行长。被告林镜鹏。上列原告诉被告信用卡欠款纠纷一案，本院于2012年1月9日受理后通知原告在七日内预交案件受理费，原告在规定期间内未预交又不提出缓交、减交、免交申请。依照最高人民法院《关于适用若干问题的意见》第143条以及《诉讼费用交纳办法》第二十二条的规定，裁定如下：本案按撤诉处理。审　判　长　　饶　弢代理审判员　　袁晶晶代理审判员　　刘　娟二〇一二年一月十九日""",
    # 可以在此添加更多的文本片段
    """河北省邯郸市中级人民法院民 事 裁 定 书（2012）邯市民监字第7号抗诉机关：河北省邯郸市人民检察院。申诉人（原审原告）：永年县金谷粮食购销有限公司。住所地：永年县苗庄村。法定代表人：孔令勇，该公司经理。被申诉人（原审被告）：周运才。申诉人永年县金谷粮食购销有限公司与被申诉人周运才劳动争议纠纷一案，河北省永年县人民法院于2011年9月5日作出（2010）永民初字第3070号民事裁定，已经发生法律效力。永年县金谷粮食购销有限公司不服，向检察机关申诉。2011年12月20日，河北省邯郸市人民检察院作出邯检民行抗（2011）96号民事抗诉书，以（2010）永民初字第3070号民事裁定适用法律确有错误为由，于2012年1月12日对本案向本院提出抗诉。依照《中华人民共和国民事诉讼法》第一百八十八条、第一百八十五条的规定，裁定如下：""",
    # 添加更多文本
]

# 函数：向指定模型发送文本并获取续写结果
def get_continuation(model_name, text):
    try:
        response = client.completions.create(
            model=model_name,
            prompt=text,
            temperature=0.1,   # 调整温度以控制随机性
            max_tokens=200,    # 设置续写的最大长度
            top_p=0.9,         # 核采样参数
            n=1,               # 生成一个续写结果
            stop=None          # 可以设置停止符号
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"出错：{e}"

# 创建CSV文件并写入标题行
with open('continuation_comparison.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['原始文本', '模型1续写', '模型2续写'])

    # 遍历文本列表
    for text in texts:
        print("正在处理文本：")
        print(text[:50] + '...')  # 打印前50个字符作为预览

        # 获取模型1的续写结果
        continuation1 = get_continuation(model1, text)
        time.sleep(1)  # 等待一段时间，避免请求过快

        # 获取模型2的续写结果
        continuation2 = get_continuation(model2, text)
        time.sleep(1)

        # 将结果写入CSV文件
        csvwriter.writerow([text, continuation1, continuation2])

print("续写对比完成，结果已保存到 continuation_comparison.csv 文件中。")
