# API 错误码处理指南

在使用 Pollinations 与火山引擎过程中，常见的错误及处理方案如下：

## Pollinations.ai 常见错误
- **401 Unauthorized**: 检查 `POLLINATIONS_API_KEY` 是否正确设置。
- **429 Too Many Requests**: 
  - 免费版：需等待几分钟。
  - 鉴权版：通常不限频，若出现则需检查并发数是否过高。
- **504 Gateway Timeout**: 网络波动或任务堆积，建议增加 `timeout` 并重试。

## 火山引擎常见错误
- **Invalid Authorization**: `API_KEY` 格式或效期问题。
- **Account Insufficiency**: 检查火山引擎账户余额。
- **Model Unavailable**: 指定的模型 ID 错误或无操作权限。

## 通用处理逻辑
1. 监控 HTTP 状态码。
2. 异常捕获后执行指数退避重试 (Exponential Backoff)。
3. 记录失败日志并触发告警。
