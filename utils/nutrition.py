# =========================
# NUTRITION DATABASE
# =========================
# Complete nutrition database for 12 food classes
# All values per serving/standard portion

NUTRITION_DATABASE = {
    "cake": {
        "calories": 400,
        "protein": 5,
        "fat": 15,
        "carbs": 60,
        "sugar": 35,
        "fiber": 1,
        "sodium": 250,
        "description": "Delicious cake - high in sugar"
    },
    "chicken curry": {
        "calories": 195,
        "protein": 25,
        "fat": 8,
        "carbs": 5,
        "sugar": 1,
        "fiber": 1,
        "sodium": 450,
        "description": "Protein-rich curry dish"
    },
    "croissant": {
        "calories": 310,
        "protein": 8,
        "fat": 17,
        "carbs": 35,
        "sugar": 8,
        "fiber": 2,
        "sodium": 320,
        "description": "Buttery pastry - high fat content"
    },
    "french fries": {
        "calories": 290,
        "protein": 3,
        "fat": 15,
        "carbs": 37,
        "sugar": 0,
        "fiber": 3,
        "sodium": 246,
        "description": "Fried potatoes - high sodium"
    },
    "fried chicken": {
        "calories": 290,
        "protein": 28,
        "fat": 18,
        "carbs": 8,
        "sugar": 0,
        "fiber": 0,
        "sodium": 320,
        "description": "Crispy chicken - protein-rich"
    },
    "hamburger": {
        "calories": 341,
        "protein": 17,
        "fat": 19,
        "carbs": 29,
        "sugar": 8,
        "fiber": 1,
        "sodium": 504,
        "description": "Classic burger - balanced macros"
    },
    "nasi goreng": {
        "calories": 637,
        "protein": 12,
        "fat": 28,
        "carbs": 85,
        "sugar": 5,
        "fiber": 2,
        "sodium": 820,
        "description": "Fried rice - high calorie, high fat"
    },
    "noodles": {
        "calories": 660,
        "protein": 14,
        "fat": 25,
        "carbs": 90,
        "sugar": 3,
        "fiber": 2,
        "sodium": 856,
        "description": "Noodles - high carbs and sodium"
    },
    "pasta": {
        "calories": 444,
        "protein": 12,
        "fat": 8,
        "carbs": 70,
        "sugar": 2,
        "fiber": 4,
        "sodium": 2,
        "description": "Carb-rich pasta"
    },
    "pizza": {
        "calories": 155,
        "protein": 6,
        "fat": 6,
        "carbs": 18,
        "sugar": 4,
        "fiber": 1,
        "sodium": 336,
        "description": "Slice of pizza"
    },
    "roast chicken": {
        "calories": 239,
        "protein": 35,
        "fat": 10,
        "carbs": 0,
        "sugar": 0,
        "fiber": 0,
        "sodium": 75,
        "description": "Lean protein - excellent health choice"
    },
    "waffle": {
        "calories": 380,
        "protein": 7,
        "fat": 17,
        "carbs": 48,
        "sugar": 18,
        "fiber": 1,
        "sodium": 680,
        "description": "Sweet waffle - high sugar content"
    }
}


def get_nutrition_info(food_name: str) -> dict:
    """Get nutrition info for a food item.
    
    Args:
        food_name: Name of the food item
        
    Returns:
        Dictionary with nutrition information
    """
    food_name_lower = food_name.lower().strip()
    
    # Try exact match first
    if food_name_lower in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[food_name_lower]
    
    # Try partial match
    for key in NUTRITION_DATABASE:
        if key in food_name_lower or food_name_lower in key:
            return NUTRITION_DATABASE[key]
    
    # Return default if not found
    return {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "sugar": 0,
        "fiber": 0,
        "sodium": 0,
        "description": "Unknown food item"
    }


def calculate_daily_values(nutrition: dict) -> dict:
    """Calculate daily value percentages (based on 2000 calorie diet).
    
    Args:
        nutrition: Nutrition dictionary
        
    Returns:
        Dictionary with daily value percentages
    """
    daily_values = {
        "calories_dv": (nutrition["calories"] / 2000) * 100,
        "protein_dv": (nutrition["protein"] / 50) * 100,
        "fat_dv": (nutrition["fat"] / 78) * 100,
        "carbs_dv": (nutrition["carbs"] / 275) * 100,
        "sugar_dv": (nutrition["sugar"] / 50) * 100,
        "fiber_dv": (nutrition["fiber"] / 28) * 100,
        "sodium_dv": (nutrition["sodium"] / 2300) * 100,
    }
    return daily_values


def get_all_food_names() -> list:
    """Get list of all food names in database."""
    return list(NUTRITION_DATABASE.keys())
