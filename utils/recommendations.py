# =========================
# RECOMMENDATION ENGINE
# =========================
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class UserProfile:
    """User health profile."""
    weight: float  # kg
    height: float  # cm
    age: int
    gender: str  # 'Male' or 'Female'
    
    def calculate_bmi(self) -> float:
        """Calculate BMI.
        
        Returns:
            BMI value
        """
        height_m = self.height / 100
        bmi = self.weight / (height_m ** 2)
        return round(bmi, 1)
    
    def get_bmi_category(self) -> str:
        """Get BMI category.
        
        Returns:
            BMI category string
        """
        bmi = self.calculate_bmi()
        
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal Weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_daily_calorie_needs(self) -> float:
        """Calculate daily calorie needs using Mifflin-St Jeor equation.
        
        Returns:
            Daily calorie recommendation
        """
        if self.gender.lower() == "male":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        
        # Assume moderate activity (1.55)
        tdee = bmr * 1.55
        return round(tdee, 0)


@dataclass
class MealAnalysis:
    """Meal nutrition analysis."""
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    total_sugar: float
    total_fiber: float
    total_sodium: float
    other_sodium: float = 1000  # Additional sodium from hidden sources
    
    def get_macro_ratios(self) -> Dict[str, float]:
        """Get macronutrient ratios as percentages.
        
        Returns:
            Dictionary with macro percentages
        """
        if self.total_calories == 0:
            return {"protein": 0, "fat": 0, "carbs": 0}
        
        protein_cals = self.total_protein * 4
        fat_cals = self.total_fat * 9
        carbs_cals = self.total_carbs * 4
        
        total_macro_cals = protein_cals + fat_cals + carbs_cals
        
        if total_macro_cals == 0:
            return {"protein": 0, "fat": 0, "carbs": 0}
        
        return {
            "protein": round((protein_cals / total_macro_cals) * 100, 1),
            "fat": round((fat_cals / total_macro_cals) * 100, 1),
            "carbs": round((carbs_cals / total_macro_cals) * 100, 1),
        }


class HealthAnalyzer:
    """Analyze meal health and generate recommendations."""
    
    @staticmethod
    def evaluate_meal_health(meal: MealAnalysis, 
                            user: UserProfile) -> Dict[str, any]:
        """Comprehensive meal health evaluation.
        
        Args:
            meal: Meal analysis
            user: User profile
            
        Returns:
            Dictionary with health metrics and indicators
        """
        daily_needs = user.get_daily_calorie_needs()
        
        evaluation = {
            "calorie_percentage": (meal.total_calories / daily_needs) * 100,
            "calorie_status": HealthAnalyzer._evaluate_calories(
                meal.total_calories, daily_needs
            ),
            "fat_status": HealthAnalyzer._evaluate_fat(meal.total_fat),
            "protein_status": HealthAnalyzer._evaluate_protein(meal.total_protein),
            "sodium_status": HealthAnalyzer._evaluate_sodium(
                meal.total_sodium + meal.other_sodium
            ),
            "sugar_status": HealthAnalyzer._evaluate_sugar(meal.total_sugar),
            "fiber_status": HealthAnalyzer._evaluate_fiber(meal.total_fiber),
        }
        
        return evaluation
    
    @staticmethod
    def _evaluate_calories(calories: float, daily_needs: float) -> str:
        """Evaluate calorie level."""
        percentage = (calories / daily_needs) * 100
        
        if percentage < 25:
            return "Light meal"
        elif percentage < 50:
            return "Moderate meal"
        elif percentage < 75:
            return "Heavy meal"
        else:
            return "Very heavy meal"
    
    @staticmethod
    def _evaluate_fat(fat: float) -> str:
        """Evaluate fat content."""
        if fat < 10:
            return "Low fat"
        elif fat < 15:
            return "Moderate fat"
        elif fat < 25:
            return "High fat"
        else:
            return "Very high fat ⚠️"
    
    @staticmethod
    def _evaluate_protein(protein: float) -> str:
        """Evaluate protein content."""
        if protein < 10:
            return "Low protein"
        elif protein < 20:
            return "Moderate protein"
        elif protein < 35:
            return "High protein"
        else:
            return "Very high protein"
    
    @staticmethod
    def _evaluate_sodium(sodium: float) -> str:
        """Evaluate sodium content."""
        if sodium < 400:
            return "Low sodium"
        elif sodium < 800:
            return "Moderate sodium"
        elif sodium < 1200:
            return "High sodium"
        else:
            return "Very high sodium ⚠️"
    
    @staticmethod
    def _evaluate_sugar(sugar: float) -> str:
        """Evaluate sugar content."""
        if sugar < 5:
            return "Low sugar"
        elif sugar < 15:
            return "Moderate sugar"
        elif sugar < 30:
            return "High sugar"
        else:
            return "Very high sugar ⚠️"
    
    @staticmethod
    def _evaluate_fiber(fiber: float) -> str:
        """Evaluate fiber content."""
        if fiber < 2:
            return "Low fiber"
        elif fiber < 5:
            return "Moderate fiber"
        else:
            return "Good fiber"


class RecommendationEngine:
    """Generate AI-style personalized recommendations."""
    
    @staticmethod
    def generate_meal_recommendations(meal: MealAnalysis, 
                                     user: UserProfile) -> List[str]:
        """Generate personalized recommendations based on meal and user profile.
        
        Args:
            meal: Meal analysis
            user: User profile
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        macros = meal.get_macro_ratios()
        daily_needs = user.get_daily_calorie_needs()
        
        # Calorie-based recommendations
        meal_percentage = (meal.total_calories / daily_needs) * 100
        
        if meal_percentage > 100:
            recommendations.append(
                "🔴 This meal exceeds your daily calorie needs. Consider: "
                "reducing portion sizes or sharing with others."
            )
        elif meal_percentage > 75:
            recommendations.append(
                "🟡 This is a substantial meal. It represents "
                f"{meal_percentage:.0f}% of your daily needs."
            )
        elif meal_percentage < 15:
            recommendations.append(
                "🟢 Light meal - great for a snack or small portion."
            )
        
        # Macro distribution
        if macros["protein"] < 15:
            recommendations.append(
                "💪 Low protein content. Add grilled chicken, fish, or legumes."
            )
        elif macros["protein"] > 35:
            recommendations.append(
                "✅ Excellent protein! This supports muscle building."
            )
        
        if macros["fat"] > 50:
            recommendations.append(
                "⚠️ High fat content. Consider: grilled instead of fried options."
            )
        
        if macros["carbs"] > 70:
            recommendations.append(
                "🌾 Very high carbs. Balance with leafy greens or vegetables."
            )
        elif macros["carbs"] < 30:
            recommendations.append(
                "🥗 Low carbs meal - suitable for low-carb diets."
            )
        
        # Health status-based recommendations
        if meal.total_sodium > 1200:
            recommendations.append(
                "🧂 High sodium alert! Aim to reduce salt intake for better cardiovascular health."
            )
        
        if meal.total_sugar > 25:
            recommendations.append(
                "🍬 High sugar content. Consider: fresh fruits instead of added sugars."
            )
        else:
            recommendations.append(
                "✅ Sugar content is well controlled."
            )
        
        if meal.total_fiber < 3:
            recommendations.append(
                "🌾 Low fiber. Add whole grains, vegetables, or legumes for digestive health."
            )
        else:
            recommendations.append(
                "✅ Good fiber content for digestive wellness."
            )
        
        # BMI-based recommendations
        bmi_category = user.get_bmi_category()
        
        if bmi_category == "Underweight":
            recommendations.append(
                f"📈 As an {bmi_category.lower()} individual, focus on nutrient-dense foods "
                "like nuts, avocados, and whole grains."
            )
        elif bmi_category == "Overweight":
            recommendations.append(
                "⚖️ Consider meals with more vegetables and lean proteins "
                "to support healthy weight management."
            )
        elif bmi_category == "Obese":
            recommendations.append(
                "⚠️ Prioritize balanced meals with high protein and fiber, "
                "lower calorie density."
            )
        
        # Diet pattern recommendations
        if meal_percentage < 35 and macros["protein"] > 25:
            recommendations.append(
                "💪 Perfect for post-workout recovery!"
            )
        elif macros["carbs"] > 60 and meal_percentage > 50:
            recommendations.append(
                "🏃 Good for pre-workout fueling!"
            )
        
        # Generic positive
        if len(recommendations) < 3:
            recommendations.append(
                "✅ Enjoy your meal mindfully!"
            )
        
        return recommendations
    
    @staticmethod
    def get_diet_category(meal: MealAnalysis) -> str:
        """Categorize meal type.
        
        Args:
            meal: Meal analysis
            
        Returns:
            Diet category string
        """
        macros = meal.get_macro_ratios()
        
        # Keto check
        if macros["carbs"] < 10 and macros["fat"] > 70:
            return "🥩 Keto-Friendly"
        
        # High protein
        if macros["protein"] > 40:
            return "💪 High Protein"
        
        # Balanced
        if 30 <= macros["carbs"] <= 50 and 25 <= macros["protein"] <= 35:
            return "⚖️ Balanced Diet"
        
        # High carb
        if macros["carbs"] > 60:
            return "🌾 High Carb"
        
        # Low fat
        if macros["fat"] < 20 and macros["protein"] > 25:
            return "🍗 Lean & Clean"
        
        return "🍽️ Mixed Macros"
