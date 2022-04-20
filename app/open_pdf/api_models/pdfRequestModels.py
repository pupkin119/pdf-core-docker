from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ManualPdfModel:
    name: str
    town: str
    course: str

