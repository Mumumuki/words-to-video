"""ComfyUI 本地适配器：向 /prompt 提交工作流，轮询 /history。

依赖：标准库 urllib（无需第三方包）。
真实工作流加载与节点映射以 references/platforms/comfyui-minimax.md 为准；此处给出最小可用骨架。
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Tuple

from . import BaseAdapter


class Adapter(BaseAdapter):
    def _post(self, endpoint: str, data: dict) -> dict:
        url = self.cfg["base_url"].rstrip("/") + endpoint
        req = urllib.request.Request(
            url, data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get(self, endpoint: str) -> dict:
        url = self.cfg["base_url"].rstrip("/") + endpoint
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def submit(self, payload: dict) -> str:
        workflow = self._load_workflow()
        workflow = self._inject(workflow, payload)
        result = self._post(self.cfg["prompt_endpoint"], {"prompt": workflow})
        return result.get("prompt_id") or result.get("job_id") or ""

    def get_status(self, job_id: str) -> Tuple[str, str]:
        try:
            hist = self._get(self.cfg["history_endpoint"])
            if job_id in hist:
                return "succeeded", "ok"
            return "running", "queued/pending"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "running", "not found yet"
            return "failed", str(e)

    # ----- 与具体工作流对接的接缝，按平台文档实现 -----
    def _load_workflow(self) -> dict:
        # 真实实现：从 cfg["workflow_file"] 读取 JSON 工作流
        return {}

    def _inject(self, workflow: dict, payload: dict) -> dict:
        # 真实实现：把 payload["prompt"] / payload["refs"] / payload["params"]
        # 映射到 ComfyUI 节点（六段式文本节点、参考图 LoadImage 槽、时长/分辨率/seed）。
        return workflow
