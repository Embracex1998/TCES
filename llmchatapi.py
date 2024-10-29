from openai import OpenAI 

client = OpenAI(
    api_key="your zhipuai api key",
    #base_url="http://localhost:8000/v1/completions"
    base_url="http://localhost:8000/v1"
) 


# completion = client.completions.create(
# model="gpt-3.5-turbo",
# messages=[{"role": "user", "content": prompt}],
# temperature=0.1
# )
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "财产保全措施在民事诉讼中起到什么作用？",
        }
    ],
    # model="/mnt/af0931a4-88fe-4e4d-86ed-54f4a275dad4/gutai/vllm_test/glm-4-9b-chat",
    model="falv",
)
# print("Completion result:", completion)
#print("Completion result:", completion.choices[0])
print("Completion result:", chat_completion.choices[0].message)
