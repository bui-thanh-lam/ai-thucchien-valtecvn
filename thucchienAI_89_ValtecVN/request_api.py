import requests
import json
import base64
import wave
from openai import OpenAI


API_KEY = "sk-XCoZZc1g4tHDcBEH3C2a9Q"
AI_API_BASE = "https://api.thucchien.ai"

usage_url = "https://api.thucchien.ai/key/info"

usage_headers = {
  "accept": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(usage_url, headers=usage_headers)

if response.status_code == 200:
    key_info = response.json()
    info = key_info['info']
    print("Key Alias:", info['key_alias'])
    print("Spend: $" + str(info['spend']))
    print("Max Budget:", info.get('max_budget', 'Unlimited'))
    print("Models:", info['models'])
    print("Created:", info['created_at'])
else:
    print("Error:", response.status_code)
    print(response.text)

import base64

gen_image_url = f"{AI_API_BASE}/images/generations"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

imagen4_prompt = """

CHo tôi 1 ảnh icon để thể hiện kêu gọi hành động để đạt được các trọng tâm trong 2026
chủ đạo màu đỏ và xám

"""

data = {
  "model": "imagen-4",
  "prompt": imagen4_prompt,
  "n": "4",
  "size": "1536x1024",
}

response = requests.post(gen_image_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
  result = response.json()
  for i, data in enumerate(result['data']):
    b64_data = data['b64_json']
    image_data = base64.b64decode(b64_data)
    with open(f"slide_2_{i+1}.png", "wb") as f:
      f.write(image_data)
  print("Image saved")
else:
  print(f"Error: {response.status_code}")
  print(response.text)