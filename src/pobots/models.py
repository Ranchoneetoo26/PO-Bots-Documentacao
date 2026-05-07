from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    name: str = Field(min_length=3)
    objective: str = Field(min_length=10)
    audience: str = Field(min_length=3)
    deadline: str = Field(min_length=3)
    stack: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class FunctionalRequirement(BaseModel):
    id: str = Field(pattern=r"^RF\d{3}$")
    title: str = Field(min_length=5)
    description: str = Field(min_length=10)
    business_rules: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)
    priority: str = Field(default="M")
    labels: List[str] = Field(default_factory=lambda: ["backend", "frontend", "qa"])


class NonFunctionalRequirement(BaseModel):
    id: str = Field(pattern=r"^RNF\d{3}$")
    title: str = Field(min_length=5)
    description: str = Field(min_length=10)


class ProjectDefinition(BaseModel):
    project: ProjectInfo
    functional_requirements: List[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: List[NonFunctionalRequirement] = Field(default_factory=list)


class Card(BaseModel):
    rf_id: str
    title: str
    objective: str
    scope: str
    out_of_scope: List[str] = Field(default_factory=list)
    business_rules: List[str] = Field(default_factory=list)
    technical_checklist: List[str] = Field(default_factory=list)
    qa_checklist: List[str] = Field(default_factory=list)
    gherkin: List[str] = Field(default_factory=list)
    priority: str = "M"
    labels: List[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    rf_id: str
    severity: str
    message: str


class CardValidationResult(BaseModel):
    rf_id: str
    score: int
    status: str
    issues: List[ValidationIssue] = Field(default_factory=list)


class ValidationSummary(BaseModel):
    global_score: int
    results: List[CardValidationResult]


class Paths(BaseModel):
    root: Path
    dist: Path
