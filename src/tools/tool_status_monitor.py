import requests
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class PollinationsMonitor:
    """
    Pollinations.ai 账户配额与刷新频率监控类
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("POLLINATIONS_API_KEY")
        self.balance_url = "https://gen.pollinations.ai/account/balance"
        self.profile_url = "https://gen.pollinations.ai/account/profile"

    def get_status(self) -> Dict[str, Any]:
        """
        获取当前账户余额、等级及下次刷新时间
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        status = {
            "success": False,
            "balance": 0,
            "next_reset": "Unknown",
            "minutes_left": -1
        }
        
        try:
            print(f"🔍 正在查询 Pollinations 账户状态...", flush=True)
            b_resp = requests.get(self.balance_url, headers=headers)
            p_resp = requests.get(self.profile_url, headers=headers)
            
            if b_resp.status_code == 200 and p_resp.status_code == 200:
                balance_data = b_resp.json()
                profile_data = p_resp.json()
                
                status["success"] = True
                status["balance"] = balance_data.get("balance", 0)
                status["next_reset"] = profile_data.get("nextResetAt", "Unknown")
                
                if status["next_reset"] != "Unknown":
                    # 处理 ISO 格式时间 (兼容 Z 结尾)
                    reset_time = datetime.fromisoformat(status["next_reset"].replace("Z", "+00:00"))
                    now = datetime.now(reset_time.tzinfo)
                    delta = reset_time - now
                    status["minutes_left"] = int(delta.total_seconds() / 60)
                
                # 导出 JSON 记录
                self._save_json(status)
                self._log_status(status)
            else:
                print(f"[!] 查询失败: Http Code {b_resp.status_code}/{p_resp.status_code}")
                
        except Exception as e:
            print(f"[x] 监控工具异常: {e}")
            
        return status

    def _save_json(self, status: Dict[str, Any]):
        """
        将当前状态保存为 JSON 文件
        """
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(log_dir, f"status_{timestamp}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=4, ensure_ascii=False)
        print(f"[*] 状态已导出至: {file_path}")

    def _log_status(self, status: Dict[str, Any]):
        """
        打印结构化日志
        """
        print("-" * 30)
        print(f"💰 账户余额: {status['balance']} pollen")
        print(f"⏰ 刷新时间: {status['next_reset']}")
        if status["minutes_left"] >= 0:
            print(f"⏳ 恢复倒计时: {status['minutes_left']} 分钟")
        print("-" * 30)

if __name__ == "__main__":
    monitor = PollinationsMonitor()
    monitor.get_status()
