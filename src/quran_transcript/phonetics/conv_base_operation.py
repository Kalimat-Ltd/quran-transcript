from dataclasses import dataclass
import re
from typing import Literal

from .moshaf_attributes import MoshafAttributes


@dataclass
class ConversionOperation:
    regs: list[tuple[str, str]] | tuple[str, str]
    arabic_name: str = ""
    ops_before: list[str] | None = None

    def __post_init__(self):
        if isinstance(self.regs, tuple):
            self.regs = [self.regs]

        if self.ops_before is None:
            self.ops_before = []

    def forward(self, text, moshaf: MoshafAttributes) -> str:
        for input_reg, out_reg in self.regs:
            text = re.sub(input_reg, out_reg, text)
        return text

    def _get_operation(op_name: str) -> "ConversionOperation":
        """
        Retrieves a ConversionOperation subclass by class name
        """
        # Collect all subclasses recursively
        subclasses = []
        to_check = [ConversionOperation]
        while to_check:
            parent = to_check.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.append(child)
                    to_check.append(child)

        for cls in subclasses:
            # Skip base class
            if cls is ConversionOperation:
                continue

            # Match by class name only
            if cls.__name__ == op_name:
                return cls()
        raise ValueError(f"Operation '{op_name}' not found")

    def apply(
        self,
        text: str,
        moshaf: MoshafAttributes,
        mode: Literal["inference", "test"] = "inference",
    ) -> str:
        if mode == "test":
            for op_name in self.ops_before:
                op = self._get_operation(op_name)
                text = op.apply(text, moshaf, mode="test")

        if mode in {"inference", "test"}:
            return self.forward(text, moshaf)
        else:
            raise ValueError(f"Invalid Model got: `{mode}`")
