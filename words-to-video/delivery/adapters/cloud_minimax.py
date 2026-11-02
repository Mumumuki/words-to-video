"""云端 MiniMax 视频适配器（骨架）。

真实端点/字段以 MiniMax 官方文档为准；此处给出可迁移的结构与 seam。
凭据从环境变量读取，不落盘。
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Tuple

from . import BaseAdapter


class Adapter(BaseAdapter):
    def _headers(self) -> dict:
        key = os.environ.get(self.cfg["api_key_env"], "")
        gid = os.environ.get(self.cfg["group_id_env"], "")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "GroupId": gid,
        }

    def submit(self, payload: dict) -> str:
        url = self.cfg["api_base"].rstrip("/") + "/video_generation"
        body = {
            "model": self.cfg.get("model", "video-01"),
            "prompt": payload.get("prompt", ""),
            "ref_images": payload.get("refs", []),
        }
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"),
            headers=self._headers(), method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("task_id") or data.get("id") or ""

    def get_status(self, job_id: str) -> Tuple[str, str]:
        url = self.cfg["api_base"].rstrip("/") + f"/video_generation/{job_id}"
        try:
            req = urllib.request.Request(url, headers=self._headers(), method="GET")
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            state = data.get("status", "unknown")
            if state in ("SUCCESS", "succeeded"):
                return "succeeded", data.get("file_url", "")
            if state in ("FAILED", "failed"):
                return "failed", data.get("reason", "")
            return "running", state
        except urllib.error.HTTPError as e:
            return "failed", str(e)
