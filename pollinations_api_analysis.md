# Pollinations API 深度解析報告 (V78)

> [!IMPORTANT]
> **接口核心**：使用 `https://gen.pollinations.ai/image/{prompt}`
> **模型矩陣**：
> - `flux`: 高性能，推薦。
> - `nanobanana`: 與 AI Studio 共享的模型系列。
> - `zimage`: 默認模型。

## 1. 關鍵參數規範 (Parameters)
| 參數 | 類型 | 功能與理解 |
| :--- | :--- | :--- |
| `seed` | Integer | 用於固定隨機性，保證畫風一致性。 |
| `enhance` | Boolean | **重要**：默認為 `false`。若設置為 `true`，AI 會自動優化提示詞。 |
| `model` | String | 指定模型。匿名訪問時建議鎖定 `model=flux`。 |
| `width / height` | Integer | 分辨率。匿名接口受帶寬限制，建議不超過 1024。 |

## 2. 鑑權與頻率 (Auth & Rate Limits)
- **Secret Key (`sk_`)**：無頻率限制，最穩定的循環方案。
- **匿名模式**：支持 <img> 標籤嵌入，免代碼。受 IP 突發保護。
- **異常識別**：若返回 1.3MB 的占位圖或特定 MD5 碼，則觸發了 429 或流量管制。

## 3. 穩定生產工作流 (Proposed Workflow)
1. **短 Prompt 策略**：利用 `enhance=true`，縮短 URL 長度，提高 GET 請求成功率。
2. **指數級退避**：代碼中加入 429/500 的退避重試（從 60s 開始遞增）。
3. **域名切換**：優先使用 `gen.` 前綴，而非 `image.`（後者可能較舊或為公共緩存）。
