# AutoStory-Alpha 架构设计说明

## 1. 整体设计哲学
AutoStory-Alpha 采用**模块化引擎 + 统一 EntryPoint** 的设计模式。核心目标是将复杂的生图与视频生成逻辑抽象化，为上层业务流（如 EP01 连载生产）提供稳定的原子能力。

## 2. 核心组件
- **Engines (src/engines/)**:
    - `VolcEngine`: 封装火山引擎 SeaDream 接口，侧重于高稳定性与正统画风。
    - `PollinationsEngine`: 封装 Pollinations.ai 鉴权版接口，侧重于灵活性与多样化风格实验。
- **Tools (src/tools/)**:
    - `PollinationsMonitor`: 实时监控流量平衡，确保持续生产。
- **CLI (main.py)**:
    - 提供统一的命令行操作界面。

## 3. 数据流
1. 用户通过 CLI 传入 Prompt。
2. 调度器根据 `engine` 参数选择对应模块。
3. 引擎执行 API 调用，处理重试逻辑。
4. 生成的图片归档至 `visual_assets/`。
5. 状态信息记录至 `logs/`。
