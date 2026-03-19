import requests
import os
import time
import urllib.parse
from typing import Dict, Any, Optional

class PollinationsEngine:
    """
    Pollinations.ai 鉴权版生图接口封装类
    """
    def __init__(self, api_key: Optional[str] = None):
        # 优先从环境变量获取
        self.api_key = api_key or os.getenv("POLLINATIONS_API_KEY")
        self.base_url = "https://gen.pollinations.ai/image/"
        self.default_model = "flux"
        self.request_delay = 2 # 默认请求间隔秒数

    def generate_image(self, prompt: str, name: str, model: Optional[str] = None, 
                       width: int = 1024, height: int = 1024, enhance: bool = True) -> bool:
        """
        调用 Pollinations 鉴权接口生成图片
        """
        model = model or self.default_model
        encoded_prompt = urllib.parse.quote(prompt)
        seed = int(time.time())
        
        # 鉴权模式下支持高级参数
        target_url = (
            f"{self.base_url}{encoded_prompt}?"
            f"model={model}&enhance={str(enhance).lower()}&"
            f"seed={seed}&width={width}&height={height}"
        )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            print(f"[*] 正在通过 Pollinations 鉴权接口生成: {name} ...")
            response = requests.get(target_url, headers=headers, timeout=120)
            
            if response.status_code == 200:
                output_path = f"visual_assets/{name}.jpg"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"[✔] {name} 生成成功: {output_path}")
                return True
            else:
                print(f"[!] {name} 生成失败 (HTTP {response.status_code}): {response.text[:200]}")
                return False
        except Exception as e:
            print(f"[x] Pollinations 接口调用异常: {e}")
            return False

def run_v78_styles():
    engine = PollinationsEngine()
    styles = {
        "A_Koei_Heroic": "Koei Romance of the Three Kingdoms 14 style, General He Jin in golden armor and butcher apron, realistic oil painting, 1994 CCTV realism.",
        "B_Ink_Wash": "Traditional Chinese ink wash painting, General He Jin, artistic brush strokes, black and light red ink.",
        "C_Retro_Anime": "90s retro anime style, hand-drawn cell shading, General He Jin, high contrast shadows."
    }
    
    for style_id, prompt in styles.items():
        engine.generate_image(prompt, f"v78_{style_id}")
        time.sleep(2) # 鉴权间隔可缩短

if __name__ == "__main__":
    run_v78_styles()
