from openai import OpenAI 

client = OpenAI(
    api_key="your zhipuai api key",
    #base_url="http://localhost:8000/v1/completions"
    base_url="http://localhost:8000/v1"
) 

# completion = client.chat.completions.create(
#     model="glm-4-9b/",  
#     messages=[    
#         {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},    
#         {"role": "user", "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"} 
#     ],
#     top_p=0.7,
#     temperature=0.9
#  ) 
 #print(completion.choices[0].message)
text="""
深圳市罗湖区人民法院民 事 裁 定 书（2012）深罗法民二初字第353号原告广发银行股份有限公司深圳分行，住所地深圳市深南东路123号百货广场大厦西座19-22层。负责人杨小舟，行长。被告林镜鹏。上列原告诉被告信用卡欠款纠纷一案，本院于2012年1月9日受理后通知原告在七日内预交案件受理费，原告在规定期间内未预交又不提出缓交、减交、免交申请。依照最高人民法院《关于适用若干问题的意见》第143条以及《诉讼费用交纳办法》第二十二条的规定，裁定如下：本案按撤诉处理。审　判　长　　饶　弢代理审判员　　袁晶晶代理审判员　　刘　娟二〇一二年一月十九日"""
completion = client.completions.create(model="falv",
                                      prompt=text,
temperature=0
)

# print("Completion result:", completion)
print("Completion result:", completion.choices[0])

