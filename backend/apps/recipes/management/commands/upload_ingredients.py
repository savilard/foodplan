import csv
import json
from pathlib import Path
from typing import List, Set

from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser

import pydantic

from apps.recipes.management.commands.schemas import Ingredient


class Command(BaseCommand):
    """Django manage.py command."""

    def add_arguments(self, parser: CommandParser):
        """Add arguments to command."""  # noqa: DAR101
        parser.add_argument(
            '--file',
            help='Path to the local ingredient file.',
            type=str,
            required=True,
        )

    def handle(self, *args, **options):  # noqa: WPS110
        """Launch command work."""  # noqa: DAR101
        file_path = Path(options.get('file', ''))
        file_ext = file_path.suffix
        supported_ext = {'.json', '.csv'}

        _check_file(file_path=file_path, file_ext=file_ext, supported_ext=supported_ext)

        ingredients = []
        if file_ext == '.json':
            ingredients = _get_ingredients_from_json_file(file_path=file_path)
        if file_ext == 'csv':
            ingredients = _get_ingredients_from_csv_file(file_path=file_path)

        _save_ingredients_to_db(ingredients)


def _check_file(file_path: Path, file_ext: str, supported_ext: Set[str]) -> None:
    """Checks input file.

    Args:
        file_path: path to file with ingredients
        file_ext: ingredients file extension
        supported_ext: supported file extensions

    Raises:
        CommandError: django command error
    """
    if file_ext not in supported_ext:
        raise CommandError(f'Only files with extensions are supported {supported_ext}')
    if not file_path.exists() or not file_path.is_file():
        raise CommandError('File not found.')


def _get_ingredients_from_json_file(file_path: Path) -> List[Ingredient]:
    """Gets ingredients from json file.

    Args:
        file_path: path to file with ingredients

    Returns:
        object: ingredients list
    """
    with open(file_path, 'r') as file_content:
        raw_ingredients = json.load(file_content)
        return pydantic.parse_obj_as(List[Ingredient], raw_ingredients)


def _get_ingredients_from_csv_file(file_path: Path) -> List[Ingredient]:
    """Gets ingredients from csv file.

    Args:
        file_path: path to file with ingredients

    Returns:
        object: ingredients list
    """
    ingredient_fields = list(Ingredient.schema()['properties'].keys())
    with open(file_path, 'r') as file_content:
        reader = csv.DictReader(file_content, fieldnames=ingredient_fields)
        return pydantic.parse_obj_as(List[Ingredient], list(reader))


def _save_ingredients_to_db(ingredients: List[Ingredient]) -> None:
    """Save ingredients to db.

    Args:
        ingredients: ingredients list
    """
    ingredient_model = apps.get_model('recipes', 'Ingredient')
    ingredient_model.objects.bulk_create(
        [
            ingredient_model(**ingredient.dict())
            for ingredient in ingredients
        ],
        ignore_conflicts=True,
    )
