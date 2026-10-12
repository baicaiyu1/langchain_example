import asyncio
import time
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from rich import print as rprint
import os

from sqlalchemy.sql.base import elements

# 加载环境变量
load_dotenv(override=True)

DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model=DEEPSEEK_MODEL,
    model_provider="openai"
)

async def demo_async_batch():
    rprint("===演示：abatch 的异步（非阻塞）效果===")
    start_time = time.perf_counter()  # 记录开始时间

    rprint("程序开始执行...")

    # 1 创建任务（Task）
    rprint(">>> 发起异步模型调用（abatch）...")
    batch_task = asyncio.create_task(model.abatch(["用一句话解释人工智能"]))

    # 并行执行其他任务
    rprint(">>> 模型请求已在后台执行，继续执行本地逻辑...")
    for i in range(3):
        await asyncio.sleep(1) # 异步等待，释放控制权
        rprint(f">>> 正在执行{i+1}个任务...（已耗时 {time.perf_counter() - start_time:.2f}s）")

    # 获取模型结果
    rprint(">>> 本地任务完成，检查模型状态...")
    response = await batch_task
    end_time = time.perf_counter()
    rprint(f">>> 流式输出: ",end="",flush=True)

    for response in response:
        content = response.content if hasattr(response,'content') else str(response)
        rprint(content,end="",flush=True)
    rprint("\n >>> 流式输出结束 \n")
    rprint(f"=== 总耗时：{end_time - start_time:.2f}s ===")

async def main():
    """主函数"""
    await demo_async_batch()


if __name__ == '__main__':
    asyncio.run(main())