# AutoStory-Alpha

AutoStory-Alpha 是一个专注于**自媒体视频全自动化生产**的轻量级框架。它集成了多种主流 AI 生图与视频生成引擎，旨在通过提示词工程与自动化脚本，实现从创意到成片的高效产出。

## 🚀 核心功能
- **多引擎支持**：集成 Pollinations (Auth 版) 与火山引擎 SeaDream 5.0。
- **视觉 DNA 锚定**：通过角色锚定图（Character Anchor）保持多镜头的视觉一致性。
- **配额监控**：实时监控 Pollinations 账号配额与刷新状态。
- **风格模板**：内置多套汉代、写意水墨、复古漫风格化提示词模板。

## 🛠️ 安装说明
1. 确保已安装 Python 3.10+。
2. 克隆仓库并安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置 API Keys：
   在 `src/engines/` 相关脚本中填入您的 Secret Key。

## 📂 项目结构
- `src/engines/`：核心生产引擎。
- `src/tools/`：辅助监控与管理工具。
- `docs/`：提示词指南与 API 分析报告。
- `visual_assets/`：视觉資產庫。

---
*本项目由 Addison (xhaddison) 维护，致力探索 AI 创作的无限可能。*
