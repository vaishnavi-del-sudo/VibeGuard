
from member5.finding_schema import Finding


def explain_finding(finding: Finding):

    explanations = {
        "fake_package": (
            "A suspicious package was detected. "
            "Verify its identity and source before installing it."
        ),

        "typosquat": (
            "This package name resembles another package. "
            "Check whether it is an incorrectly named dependency."
        ),

        "known_vuln": (
            "This dependency may contain a known vulnerability. "
            "Check the affected version and available updates."
        ),

        "secret": (
            "A possible sensitive credential was detected. "
            "Review the file and secure any exposed credential."
        ),

        "insecure_pattern": (
            "This code contains a potentially unsafe pattern. "
            "Review it and consider a safer alternative."
        ),

        "hidden_char": (
            "Unusual hidden characters were detected. "
            "Inspect the file for unexpected content."
        ),

        "ai_config": (
            "This configuration may introduce a security risk. "
            "Review the settings and apply secure defaults."
        )
    }

    explanation = explanations.get(
        finding.type,
        "Please review this security finding carefully."
    )

    severity_guidance = {
        "critical": "Immediate attention required. Prioritise this issue.",
        "high": "Investigate and resolve this issue as soon as possible.",
        "medium": "Review this issue and plan an appropriate resolution.",
        "low": "Include this issue in your routine security review."
    }

    guidance = severity_guidance.get(
        finding.severity,
        "Review the severity of this issue."
    )

    return {
        "title": finding.title,
        "severity": finding.severity,
        "description": finding.description,
        "explanation": explanation,
        "guidance": guidance,
        "file": finding.file,
        "line": finding.line
    }


if __name__ == "__main__":

    sample_finding = Finding(
        type="fake_package",
        severity="high",
        file="requirements.txt",
        line=4,
        title="Suspicious package detected",
        description="An unusual package was detected.",
        evidence="Unknown package detected"
    )

    result = explain_finding(sample_finding)

    print("\n===== VIBEGUARD AI EXPLANATION =====")

    for key, value in result.items():
        print(f"{key}: {value}")



