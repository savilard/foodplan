from typing import Any

from factory import Faker
from factory.builder import BuildStep


class UniqueStringMixin(Faker):
    """Mixin for creating guaranteed unique values for text fields with unique=True."""

    def evaluate(self, instance: Any, step: BuildStep, extra: Any) -> str:
        text_char_value = super().evaluate(instance, step, extra)
        return f'{step.sequence} {text_char_value}'
