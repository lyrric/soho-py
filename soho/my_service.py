import asyncio
import threading
import time
from typing import Optional


class SingleThreadCoroutineRunner:
    def __init__(self):
        """初始化单线程协程运行器"""
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self._start_thread()

    def _start_thread(self) -> None:
        """启动一个线程并在其中运行事件循环"""

        def run_loop():
            # 创建并运行事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        # 启动线程
        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

        # 等待事件循环初始化完成
        while self.loop is None:
            time.sleep(0.01)

    def submit_coroutine(self, coro, *args, **kwargs) -> asyncio.Future:
        """向事件循环提交协程任务（线程安全）"""
        if not self.loop or not self.thread.is_alive():
            raise RuntimeError("事件循环未运行或已停止")

        # 线程安全地提交协程
        return asyncio.run_coroutine_threadsafe(
            coro(*args, **kwargs),
            loop=self.loop
        )

    def stop(self) -> None:
        """停止事件循环和线程"""
        if self.loop and self.thread.is_alive():
            # 线程安全地停止事件循环
            self.loop.call_soon_threadsafe(self.loop.stop)
            # 等待线程结束
            self.thread.join()
            print("事件循环和线程已停止")
