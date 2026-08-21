from dataclasses import dataclass, field
from typing import Any


@dataclass
class FabricAnalysis:
    fabric: str
    is_delicate: bool
    temperature: str
    programme: str
    spin: str
    notes: list[str] = field(default_factory=list)


@dataclass
class ColorAnalysis:
    color_group: str
    separate: bool
    prefer_low_temperature: bool
    avoid_bleach: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class StainAnalysis:
    stain: str
    pretreatment: str
    avoid: list[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    status: str
    final_response: str
    trace: dict[str, Any] = field(default_factory=dict)
