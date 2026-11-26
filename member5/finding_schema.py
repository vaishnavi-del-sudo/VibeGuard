
from pydantic import BaseModel
from typing import Literal, Optional


class Finding(BaseModel):

    type: Literal[
        "fake_package",
        "typosquat",
        "known_vuln",
        "secret",
        "insecure_pattern",
        "hidden_char",
        "ai_config"
    ]

    severity: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]

    file: str
    line: Optional[int] = None
    title: str
    description: str
    evidence: str
    description: str



if __name__ == "__main__":

    finding = Finding(
        type="fake_package",
        severity="high",
        file="requirements.txt",
        line=4,
        title="Suspicious package detected",
        description="A package with an unusual name was detected.",
        evidence="Unknown package detected"
    )

    print(finding.model_dump_json(indent=4))
