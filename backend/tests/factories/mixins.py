from typing import Any

import factory


class UniqueStringMixin(factory.Faker):
    """Mixin for creating guaranteed unique values for text fields with unique=True."""

    def evaluate(self, instance: Any, step: factory.builder.BuildStep, extra: Any) -> str:
        text_char_value = super().evaluate(instance, step, extra)
        return f'{step.sequence} {text_char_value}'
