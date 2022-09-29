def validate_recipe_data(recipe_data, serializer):
    """Validate recipe data from frontend."""
    recipe_create_serializer = serializer(data=recipe_data)
    recipe_create_serializer.is_valid(raise_exception=True)
    return recipe_create_serializer.validated_data
