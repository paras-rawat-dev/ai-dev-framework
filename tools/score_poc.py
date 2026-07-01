#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POC = ROOT / "poc"


@dataclass(frozen=True)
class Criterion:
    name: str
    tokens: tuple[str, ...]
    weight: int = 1

    def score(self, text: str) -> bool:
        lowered = text.lower()
        return all(token.lower() in lowered for token in self.tokens)


CRITERIA = [
    Criterion("objective", ("objective",)),
    Criterion("users", ("users",)),
    Criterion("non_goals", ("non-goals",)),
    Criterion("stack_packs", ("stack", "python-fastapi", "react-vite")),
    Criterion("ui_member", ("ui member", "shadcn")),
    Criterion("data_handling", ("data", "sensitivity")),
    Criterion("quality_gates", ("quality gates", "pytest")),
    Criterion("tests", ("minimum tests", "parser")),
    Criterion("performance", ("performance", "1,000 rows")),
    Criterion("ai_workflow", ("ai workflow", "independent review")),
    Criterion("dependency_control", ("do not add a second ui library",)),
    Criterion("definition_of_done", ("definition of done",)),
]


def evaluate(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    passed = []
    score = 0
    for criterion in CRITERIA:
        if criterion.score(text):
            score += criterion.weight
            passed.append(criterion.name)
    return score, passed


def main() -> int:
    files = [
        POC / "baseline-output.md",
        POC / "framework-output.md",
    ]

    max_score = sum(c.weight for c in CRITERIA)
    results = []
    for file in files:
        score, passed = evaluate(file)
        results.append((file.name, score, passed))

    print("POC readiness score")
    print("===================")
    for name, score, passed in results:
        print(f"{name}: {score}/{max_score}")
        print(f"  passed: {', '.join(passed) if passed else 'none'}")

    baseline = results[0][1]
    framework = results[1][1]
    delta = framework - baseline
    print()
    print(f"delta: +{delta} criteria")

    if framework <= baseline:
        print("FAIL: framework artifact did not improve readiness score")
        return 1

    if framework < max_score:
        print("FAIL: framework artifact is still missing required readiness criteria")
        return 1

    print("PASS: framework artifact covers all readiness criteria and improves on baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

