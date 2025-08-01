from dataclasses import dataclass
import re
from typing import Literal

from .moshaf_attributes import MoshafAttributes


@dataclass
class ConversionOperation:
    regs: list[tuple[str, str]] | tuple[str, str]
    arabic_name: str = ""
    ops_before: list["ConversionOperation"] | None = None

    def __post_init__(self):
        if isinstance(self.regs, tuple):
            self.regs = [self.regs]

        if self.ops_before is None:
            self.ops_before = []

    def forward(self, text, moshaf: MoshafAttributes) -> str:
        for input_reg, out_reg in self.regs:
            text = re.sub(input_reg, out_reg, text)
        return text

    def apply(
        self,
        text: str,
        moshaf: MoshafAttributes,
        mode: Literal["inference", "test"] = "inference",
    ) -> str:
        if mode == "test":
            for op in self.ops_before:
                print(f"Applying: {type(op)}")
                text = op.apply(text, moshaf, mode="test")

        if mode in {"inference", "test"}:
            return self.forward(text, moshaf)
        else:
            raise ValueError(f"Invalid Model got: `{mode}`")
