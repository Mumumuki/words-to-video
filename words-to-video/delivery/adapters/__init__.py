"""Delivery 适配器包：把一段 payload 提交到视频生成平台并轮询状态。

每个适配器实现两个方法：
  submit(payload: dict) -> job_id: str
  get_status(job_id: str) -> (status: str, detail: str)
status ∈ {pending, running, succeeded, failed}
"""
from __future__ import annotations

import importlib
from typing import Tuple


def load_adapter(adapter_cfg: dict):
    """按 cfg['type'] 动态加载 adapters/<type>.py 中的 Adapter 类。"""
    atype = adapter_cfg.get("type")
    if not atype:
        raise ValueError("adapter 配置缺少 type")
    module = importlib.import_module(f"adapters.{atype}")
    cls = getattr(module, "Adapter")
    return cls(adapter_cfg)


class BaseAdapter:
    def __init__(self, cfg: dict):
        self.cfg = cfg

    def submit(self, payload: dict) -> str:
        raise NotImplementedError

    def get_status(self, job_id: str) -> Tuple[str, str]:
        raise NotImplementedError
