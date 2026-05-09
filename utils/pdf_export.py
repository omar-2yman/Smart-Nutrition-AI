# =========================
# PDF REPORT EXPORT
# =========================
from fpdf import FPDF
from PIL import Image
import io
from typing import List, Dict, Optional
from datetime import datetime
from utils.recommendations import UserProfile, MealAnalysis


class NutritionReportPDF(FPDF):
    """Custom PDF class for nutrition reports."""
    
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        """Add header to each page."""
        self.set_fill_color(44, 55, 74)  # Dark blue
        self.rect(0, 0, self.WIDTH, 30, 'F')
        
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 25, 'Smart Nutrition AI Report', 0, 1, 'C')
        
        self.ln(5)
    
    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def section_title(self, title: str):
        """Add a section title."""
        title = title.encode('ascii', 'ignore').decode('ascii').strip()
        self.set_font('Arial', 'B', 14)
        self.set_text_color(44, 55, 74)
        self.set_fill_color(230, 240, 250)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', True)
        self.ln(3)
    
    def add_text(self, text: str, size: int = 10, bold: bool = False):
        """Add formatted text."""
        text = text.encode('ascii', 'ignore').decode('ascii').strip()
        self.set_font('Arial', 'B' if bold else '', size)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(2)
    
    def add_key_value(self, key: str, value: str, indent: int = 0):
        """Add key-value pair."""
        key = key.encode('ascii', 'ignore').decode('ascii').strip()
        value = str(value).encode('ascii', 'ignore').decode('ascii').strip()
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        spacing = ' ' * indent
        self.cell(0, 7, f'{spacing}* {key}: {value}', 0, 1)
    
    def add_nutrition_table(self, meal: MealAnalysis):
        """Add nutrition information table."""
        self.set_font('Arial', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(100, 120, 150)
        
        # Header
        col_width = self.WIDTH / 7 - 5
        headers = ['Nutrient', 'Amount', 'Unit', 'Nutrient', 'Amount', 'Unit']
        for header in headers:
            self.cell(col_width - 2, 8, header, 1, 0, 'C', True)
        self.ln()
        
        # Data
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        
        data_pairs = [
            ('Calories', f'{meal.total_calories:.0f}', 'kcal',
             'Sugar', f'{meal.total_sugar:.1f}', 'g'),
            ('Protein', f'{meal.total_protein:.1f}', 'g',
             'Fiber', f'{meal.total_fiber:.1f}', 'g'),
            ('Fat', f'{meal.total_fat:.1f}', 'g',
             'Sodium', f'{meal.total_sodium:.0f}', 'mg'),
            ('Carbs', f'{meal.total_carbs:.1f}', 'g',
             '', '', ''),
        ]
        
        for left_data in data_pairs:
            for i, val in enumerate(left_data[:3]):
                self.cell(col_width - 2, 8, str(val), 1, 0, 'C')
            for i, val in enumerate(left_data[3:]):
                self.cell(col_width - 2, 8, str(val), 1, 0, 'C')
            self.ln()
        
        self.ln(5)


def generate_pdf_report(
    meal: MealAnalysis,
    user: UserProfile,
    food_items: List[Dict],
    evaluation: Dict,
    recommendations: List[str],
    diet_category: str,
    image_path: Optional[str] = None,
    detection_image_path: Optional[str] = None
) -> bytes:
    """Generate complete PDF report.
    
    Args:
        meal: Meal analysis
        user: User profile
        food_items: Detected food items
        evaluation: Health evaluation
        recommendations: List of recommendations
        diet_category: Diet category string
        image_path: Path to original image
        detection_image_path: Path to detection image
        
    Returns:
        PDF as bytes
    """
    pdf = NutritionReportPDF()
    pdf.add_page()
    
    # User Information
    pdf.section_title('👤 User Profile')
    pdf.add_key_value('Name', 'Test User')
    pdf.add_key_value('Weight', f'{user.weight} kg')
    pdf.add_key_value('Height', f'{user.height} cm')
    pdf.add_key_value('Age', f'{user.age} years')
    pdf.add_key_value('Gender', user.gender)
    pdf.add_key_value('BMI', f'{user.calculate_bmi()} ({user.get_bmi_category()})')
    pdf.add_key_value('Daily Calorie Needs', f'{user.get_daily_calorie_needs():.0f} kcal')
    
    # Meal Summary
    pdf.section_title('🍽 Meal Analysis')
    pdf.add_text(f'Total Calories: {meal.total_calories:.0f} kcal', bold=True)
    
    # Detected Foods
    if food_items:
        pdf.section_title('🥘 Detected Food Items')
        for item in food_items:
            pdf.add_key_value(
                item['food'].title(),
                f"{item['calories']} kcal (Confidence: {item['confidence']}%)"
            )
    
    # Nutrition Details
    pdf.section_title('📊 Detailed Nutrition Information')
    pdf.add_nutrition_table(meal)
    
    # Health Analysis
    pdf.section_title('❤️ Health Analysis')
    pdf.add_key_value('Calorie Status', evaluation.get('calorie_status', 'N/A'))
    pdf.add_key_value('Fat Status', evaluation.get('fat_status', 'N/A'))
    pdf.add_key_value('Protein Status', evaluation.get('protein_status', 'N/A'))
    pdf.add_key_value('Sodium Status', evaluation.get('sodium_status', 'N/A'))
    pdf.add_key_value('Sugar Status', evaluation.get('sugar_status', 'N/A'))
    pdf.add_key_value('Fiber Status', evaluation.get('fiber_status', 'N/A'))
    pdf.add_key_value('Diet Category', diet_category)
    
    # Recommendations
    pdf.section_title('💡 AI Recommendations')
    for i, rec in enumerate(recommendations, 1):
        pdf.add_text(f'{i}. {rec}', size=9)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, f'Report generated: {timestamp}', 0, 1)
    
    # Add images if available
    if image_path or detection_image_path:
        pdf.add_page()
        pdf.section_title('📸 Analysis Images')
        
        try:
            if image_path:
                pdf.add_text('Original Image', bold=True, size=11)
                pdf.image(image_path, x=10, y=pdf.get_y(), w=90)
                pdf.ln(55)
            
            if detection_image_path:
                pdf.add_text('Detection Results', bold=True, size=11)
                pdf.image(detection_image_path, x=10, y=pdf.get_y(), w=90)
        except Exception as e:
            pdf.add_text(f'Note: Images could not be embedded ({str(e)})')
    
    # Return PDF as bytes
    pdf_out = pdf.output(dest='S')
    if isinstance(pdf_out, (bytes, bytearray)):
        return bytes(pdf_out)
    return pdf_out.encode('latin-1')


def save_pdf_report(pdf_bytes: bytes, filename: str) -> str:
    """Save PDF report to file and return path.
    
    Args:
        pdf_bytes: PDF content as bytes
        filename: Output filename
        
    Returns:
        Path to saved PDF file
    """
    import os
    
    # Create reports directory if it doesn't exist
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filepath = os.path.join(reports_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(pdf_bytes)
    
    return filepath
