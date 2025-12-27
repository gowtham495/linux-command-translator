# This file will have all the model registry used in the application.

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExperimentConfig:
    model_name: str
    model_version: str
    prompt_template: str
    temperature: float
    top_p: float
    num_predict: int


EXPERIMENTS: Dict[str, ExperimentConfig] = {
    "phi3-mini:default": ExperimentConfig(
        model_name="phi3:mini",
        model_version="4k-instruct-q4",
        prompt_template="linux_cmd_v1",
        temperature=0.1,
        top_p=0.9,
        num_predict=80,
    ),
    "phi3-mini:exp": ExperimentConfig(
        model_name="phi3:mini",
        model_version="4k-instruct-q4",
        prompt_template="linux_cmd_v2",
        temperature=0.4,
        top_p=0.9,
        num_predict=80,
    ),
}
