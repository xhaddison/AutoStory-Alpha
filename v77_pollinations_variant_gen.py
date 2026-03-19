import requests
import os
import time
import hashlib

# 存儲路徑
OUTPUT_DIR = "/Users/addison/repository/AutoStory-Alpha/v77_hejin_variants"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Pollinations 頻率限制占位圖的 MD5 特徵值
PLACEHOLDER_MD5 = "2090a5dc21c32952cbf8496339752bd1"

# 何進多風格樣片定義 (基於 EP01 劇情)
# 加入英雄厚塗、水墨、復古漫劃等四種對照風
VARIANTS = {
    "HeJin_Koei_Baseline": "Koei Romance of the Three Kingdoms 14 official art style, heroic He Jin in golden armor, majestic beard, thick oil painting texture, 1994 CCTV TV series realism, cinematic lighting.",
    "HeJin_Ink_Wash": "Traditional Chinese ink wash painting style, artistic brush strokes, black and white ink with light colors, majestic general He Jin, ethereal and poetic atmosphere.",
    "HeJin_Retro_Anime": "90s retro anime style, hand-drawn cell shading, high-contrast shadows, 1990s TV animation look, cinematic action pose, thick outlines.",
    "HeJin_Hyper_Real": "Hyper-realistic photographic still, inspired by 1994 TV series, 35mm film grain, authentic Han dynasty costume textures, dramatic side lighting, chiaroscuro."
}

def get_md5(content):
    return hashlib.md5(content).hexdigest()

def generate_variants():
    print(f"🚀 開始生成何進 4 大風格樣片 (V77.2 匿名 GET 穩定版)...", flush=True)
    
    # 匿名接口前綴
    base_url = "https://image.pollinations.ai/prompt/"
    
    for style_id, prompt in VARIANTS.items():
        file_path = os.path.join(OUTPUT_DIR, f"{style_id}.jpg")
        
        # 為了保證匿名接口成功率，對 Prompt 進行適當壓縮並 URL 編碼
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        
        # 構建帶 seed 和 寬高的 GET URL
        target_url = f"{base_url}{encoded_prompt}?width=1024&height=1024&nologo=true&seed={int(time.time())}"

        success = False
        for attempt in range(5):
            try:
                print(f"📡 正在生成: {style_id} (嘗試 {attempt+1})...", flush=True)
                # 匿名 GET 請求
                response = requests.get(target_url, timeout=120) 
                
                if response.status_code == 200:
                    content = response.content
                    current_md5 = get_md5(content)
                    
                    # 檢測占位圖 (頻率限制)
                    if current_md5 == PLACEHOLDER_MD5:
                        print(f"⚠️ 觸發頻率限制 (占位圖)，等待 {60*(attempt+1)} 秒...", flush=True)
                        time.sleep(60 * (attempt + 1))
                        continue
                    
                    # 檢測二進制內容是否有效
                    if len(content) < 5000: # 太小肯定不對
                        print(f"⚠️ 內容過小，可能生成失敗，重試...", flush=True)
                        time.sleep(10)
                        continue

                    with open(file_path, "wb") as f:
                        f.write(content)
                    print(f"✅ 生成成功: {file_path}", flush=True)
                    success = True
                    break
                else:
                    print(f"❌ HTTP 錯誤: {response.status_code}", flush=True)
                    time.sleep(30)
            except Exception as e:
                print(f"⚠️ 異常: {str(e)}", flush=True)
                time.sleep(20)
        
        if success:
            print(f"⏳ 間隔休眠 60 秒 (保持匿名通道通暢)...", flush=True)
            time.sleep(60)

if __name__ == "__main__":
    generate_variants()
