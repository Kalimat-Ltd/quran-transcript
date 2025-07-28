from dataclasses import dataclass
import re

from .moshaf_attributes import MoshafAttributes


@dataclass
class ConversionOperation:
    name: str
    arabic_name: str = ""
    input_regs: str | None = None
    output_regs: str | None = None

    def apply(self, text: str, moshaf: MoshafAttributes) -> str:
        if self.input_regs is not None and self.output_regs is not None:
            return re.sub(self.input_regs, self.output_regs, text)
        else:
            raise ValueError(
                f"No Operaton to apply input_regs is `{self.input_regs}` and output_regs is `{self.output_regs}` "
            )
