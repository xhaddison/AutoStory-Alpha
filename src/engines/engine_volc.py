import requests
import json
import base64
import os
import time
from typing import Dict, Any, Optional

class VolcEngine:
    """
    火山引擎 SeaDream 5.0 生图接口封装类
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VOLC_API_KEY")
        self.url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        self.default_model = "doubao-seedream-5-0-260128"

    def generate_image(self, prompt: str, name: str, size: str = "2048x2048", retries: int = 3) -> bool:
        """
        调用火山引擎生成单张图片并保存，支持重试机制
        """
        payload = {
            "model": self.default_model,
            "prompt": prompt,
            "size": size,
            "n": 1,
            "watermark": False
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        for attempt in range(retries):
            try:
                print(f"[*] 正在调用火山引擎生成: {name} (尝试 {attempt + 1}/{retries}) ...")
                response = requests.post(self.url, headers=headers, json=payload, timeout=60)
                res_json = response.json()
                
                if response.status_code == 200:
                    image_url = res_json['data'][0]['url']
                    img_data = requests.get(image_url).content
                    output_path = f"visual_assets/{name}.png"
                    
                    # 确保目录存在
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    with open(output_path, 'wb') as f:
                        f.write(img_data)
                    print(f"[✔] {name} 生成成功并保存至: {output_path}")
                    return True
                else:
                    print(f"[!] {name} 生成失敗 (代碼 {response.status_code}): {res_json}")
            except Exception as e:
                print(f"[x] 第 {attempt + 1} 次嘗試出錯: {e}")
            
            if attempt < retries - 1:
                time.sleep(2) # 等待后重试
        
        return False

def run_v56_preview():
    # 保持向后兼容的预览运行逻辑
    engine = VolcEngine()
    
    tasks = {
        "HeJin_Butcher": "光荣三国志14风格，大将军何进金甲束发，在深宫中挥舞屠刀劈砍带有现代合格印章的猪肉。",
        "HeYuan_Plot": "1994版三国质感，何进与袁绍共谋，低头查看发出幽幽荧光的现代智能手机。"
    }

    for name, prompt in tasks.items():
        engine.generate_image(prompt, f"v56_{name}")

if __name__ == "__main__":
    run_v56_preview()
