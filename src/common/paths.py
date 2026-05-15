"""路径与配置加载。编程 Agent 可按项目改默认值。"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def project_root() -> Path:
    return ROOT


def data_dir() -> Path:
    return Path(os.getenv("DATA_DIR", ROOT / "data"))


def breakdown_output_dir() -> Path:
    p = Path(os.getenv("OUTPUT_BREAKDOWN_DIR", ROOT / "outputs" / "breakdown"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def reports_output_dir() -> Path:
    p = Path(os.getenv("OUTPUT_REPORTS_DIR", ROOT / "outputs" / "reports"))
    p.mkdir(parents=True, exist_ok=True)
    return p
