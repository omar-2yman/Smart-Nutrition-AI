#!/usr/bin/env python3
# =========================
# 🍔 SMART NUTRITION AI ASSISTANT
# =========================
# Professional AI-powered food detection and nutrition analysis system
# Features: YOLOv8 Detection, Nutrition Analysis, PDF Reports, BMI Analysis

import streamlit as st
from streamlit_option_menu import option_menu
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from datetime import datetime
from ultralytics import YOLO

# Import utility modules
from utils.nutrition import NUTRITION_DATABASE, get_nutrition_info
from utils.recommendations import UserProfile, MealAnalysis, HealthAnalyzer, RecommendationEngine
from utils.charts import (
    create_macro_distribution_pie,
    create_nutrition_bars,
    create_calorie_gauge,
    create_health_indicators,
    create_food_items_bar
)
from utils.pdf_export import generate_pdf_report, save_pdf_report


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Nutrition AI",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Apple-Style Dark Mode
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Premium Dark Mode Theme */
    :root {
        --bg-color: #0b0f19;
        --card-bg: rgba(20, 25, 40, 0.6);
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --accent-gradient: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        --accent-purple: linear-gradient(135deg, #c471ed 0%, #f64f59 100%);
        --border-color: rgba(255, 255, 255, 0.08);
    }
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0b0f19, #131a2f, #0d1326, #090c15);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: var(--text-primary);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Hide Streamlit components to look like a web app */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Cards */
    .premium-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .premium-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 40px -8px rgba(79, 172, 254, 0.3);
        border-color: rgba(79, 172, 254, 0.5);
    }
    
    /* Hero Section */
    @keyframes gradientPulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-title {
        font-size: 5rem;
        background: var(--accent-gradient);
        background-size: 200% auto;
        animation: gradientPulse 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.04em;
    }
    .hero-subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.3rem;
        margin-bottom: 4rem;
        font-weight: 400;
    }
    
    /* Feature Cards */
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 16px;
        transition: transform 0.3s ease;
    }
    .premium-card:hover .feature-icon {
        transform: scale(1.1);
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 10px;
    }
    .feature-desc {
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Metrics */
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
        letter-spacing: -0.03em;
    }
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }
    
    /* Streamlit UI Overrides */
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--border-color);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.5) !important;
    }
    .stDownloadButton > button {
        background: var(--accent-purple) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(196, 113, 237, 0.3) !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(196, 113, 237, 0.5) !important;
    }
    
    /* Inputs */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 1px #4facfe !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(79, 172, 254, 0.3) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        background-color: rgba(79, 172, 254, 0.08) !important;
        border-color: #4facfe !important;
        transform: scale(1.02);
    }
    
    /* Clean up expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--text-primary);
        background-color: transparent !important;
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# CACHE FUNCTIONS
# =========================
@st.cache_resource
def load_yolo_model():
    """Load YOLOv8 model with caching."""
    return YOLO("best.pt")


# =========================
# INITIALIZATION
# =========================
def initialize_session_state():
    """Initialize session state variables."""
    if 'detection_results' not in st.session_state:
        st.session_state.detection_results = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

initialize_session_state()

# Load model
try:
    model = load_yolo_model()
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.stop()


# =========================
# SIDEBAR NAVIGATION & USER PROFILE
# =========================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 1rem; color: #fff;'>🍔 Nutrition AI</h2>", unsafe_allow_html=True)
    
    # Navigation
    page = option_menu(
        None,
        ["Dashboard", "Analysis", "Reports", "About"],
        icons=["house", "camera", "file-earmark-pdf", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4facfe", "font-size": "1.1rem"}, 
            "nav-link": {"font-size": "0.95rem", "text-align": "left", "margin":"0px", "--hover-color": "rgba(79, 172, 254, 0.1)"},
            "nav-link-selected": {"background-color": "rgba(79, 172, 254, 0.2)", "color": "white", "font-weight": "600"},
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Compact Profile Settings
    with st.expander("👤 Health Profile", expanded=False):
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175, step=1)
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=25, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
    user = UserProfile(weight=weight, height=height, age=age, gender=gender)
    
    with st.expander("⚙️ Advanced Settings", expanded=False):
        confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
        show_charts = st.toggle("Enable Deep Analytics", value=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Minimal metrics in sidebar
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 16px; margin-top: 10px; border: 1px solid rgba(255,255,255,0.05);">
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 4px;">BMI Status</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: #fff;">{user.calculate_bmi()} <span style="font-size:0.9rem; font-weight:normal; color:#4facfe;">({user.get_bmi_category()})</span></div>
    </div>
    <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 16px; margin-top: 12px; border: 1px solid rgba(255,255,255,0.05);">
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 4px;">Daily Target</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: #fff;">{user.get_daily_calorie_needs():.0f} <span style="font-size:0.9rem; font-weight:normal; color:#4facfe;">kcal</span></div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# PAGE: HOME (Dashboard)
# =========================
if page == "Dashboard":
    # Hero Section
    st.markdown('<div class="hero-title">Smart Nutrition AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">AI-powered food detection, nutrition analysis, and personalized health insights.</div>', unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="premium-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Food Detection</div>
            <div class="feature-desc">Real-time identification of complex meals.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="premium-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Nutrition Analysis</div>
            <div class="feature-desc">Instant macro and micronutrient breakdown.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="premium-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">AI Recommendations</div>
            <div class="feature-desc">Personalized health advice based on your profile.</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="premium-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">PDF Reports</div>
            <div class="feature-desc">Export professional nutrition reports instantly.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    

    # Quick Stats
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 1.5rem;">System Capabilities</h3>', unsafe_allow_html=True)
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.markdown("""<div class="premium-card" style="text-align:center; padding:2rem 1rem;">
            <div class="metric-value">12+</div><div class="metric-label">Supported Foods</div></div>""", unsafe_allow_html=True)
    with stat2:
        st.markdown("""<div class="premium-card" style="text-align:center; padding:2rem 1rem;">
            <div class="metric-value">95%</div><div class="metric-label">AI Accuracy</div></div>""", unsafe_allow_html=True)
    with stat3:
        st.markdown("""<div class="premium-card" style="text-align:center; padding:2rem 1rem;">
            <div class="metric-value">7</div><div class="metric-label">Nutrition Metrics</div></div>""", unsafe_allow_html=True)
    with stat4:
        st.markdown("""<div class="premium-card" style="text-align:center; padding:2rem 1rem;">
            <div class="metric-value">PDF</div><div class="metric-label">Reports</div></div>""", unsafe_allow_html=True)


# =========================
# PAGE: ANALYSIS
# =========================
elif page == "Analysis":
    st.markdown('<h2 style="margin-bottom: 2rem;">Analysis Dashboard</h2>', unsafe_allow_html=True)
    
    if "webcam_images" not in st.session_state:
        st.session_state.webcam_images = []

    # Input Methods
    upload_col1, upload_col2 = st.columns(2)
    with upload_col1:
        st.markdown('<h4 style="margin-bottom: 1rem;">Upload Images</h4>', unsafe_allow_html=True)
        st.caption("You can select multiple images at once.")
        uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], key="analysis_upload",
                                          label_visibility="collapsed", accept_multiple_files=True)
        
        uploaded_images = [Image.open(f).convert("RGB") for f in uploaded_files] if uploaded_files else []

    with upload_col2:
        st.markdown('<h4 style="margin-bottom: 1rem;">Use Webcam</h4>', unsafe_allow_html=True)
        st.caption("Capture and add multiple images to a batch.")
        with st.expander("📷 Click here to open camera"):
            camera_image = st.camera_input("Capture food", key="analysis_cam", label_visibility="collapsed")
            
            if camera_image:
                if st.button("➕ Add Photo to Batch", type="primary", use_container_width=True):
                    st.session_state.webcam_images.append(Image.open(camera_image).convert("RGB"))
                    st.rerun()
                    
            if len(st.session_state.webcam_images) > 0:
                st.success(f"📸 {len(st.session_state.webcam_images)} images in webcam batch.")
                if st.button("🗑️ Clear Webcam Batch", use_container_width=True):
                    st.session_state.webcam_images = []
                    st.rerun()

    images_to_process = uploaded_images + st.session_state.webcam_images
    
    if not images_to_process:
        st.info("📸 Please upload images or capture photos above to start the analysis.")
    else:
        st.session_state.uploaded_images = images_to_process
        num_images = len(images_to_process)
        if num_images > 1:
            st.markdown(f'<h4 style="margin-bottom:1rem;">Processing {num_images} Images as a Single Meal</h4>', unsafe_allow_html=True)

        detected_items = []
        total_calories = total_protein = total_fat = total_carbs = total_sugar = total_fiber = total_sodium = 0
        processed_images = []
        temp_files = []

        with st.spinner(f"Analyzing {num_images} image{'s' if num_images > 1 else ''}..."):
            for img_idx, image_to_process in enumerate(images_to_process):
                image_np = np.array(image_to_process)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                Image.fromarray(image_np).save(temp_file.name)
                temp_files.append(temp_file.name)
                temp_file.close()

                results = model.predict(source=temp_file.name, conf=confidence, save=False, verbose=False)
                result = results[0]
                plotted = result.plot()
                
                processed_images.append({
                    "original": image_np,
                    "plotted": plotted
                })

                if len(result.boxes) > 0:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        conf_score = float(box.conf[0])
                        class_name = result.names[cls_id]
                        nutrition = get_nutrition_info(class_name)
                        calories = nutrition["calories"]
                        
                        item_label = f"{class_name} (Img {img_idx+1})" if num_images > 1 else class_name
                        detected_items.append({"food": item_label, "confidence": round(conf_score * 100, 2), "calories": calories})
                        
                        total_calories += calories
                        total_protein += nutrition["protein"]
                        total_fat += nutrition["fat"]
                        total_carbs += nutrition["carbs"]
                        total_sugar += nutrition["sugar"]
                        total_fiber += nutrition["fiber"]
                        total_sodium += nutrition["sodium"]

        if len(detected_items) > 0:
            meal = MealAnalysis(total_calories, total_protein, total_fat, total_carbs, total_sugar, total_fiber, total_sodium)
            st.session_state.detection_results = {
                "meal": meal, "detected_items": detected_items,
                "plotted_image": processed_images[0]["plotted"], 
                "original_image": processed_images[0]["original"], 
                "temp_file": temp_files[0] if temp_files else None
            }
            st.session_state.analysis_complete = True

            evaluation = HealthAnalyzer.evaluate_meal_health(meal, user)
            recommendations = RecommendationEngine.generate_meal_recommendations(meal, user)
            diet_category = RecommendationEngine.get_diet_category(meal)

            # Images
            st.markdown('<h4 style="margin-bottom:1rem;">AI Detection Results</h4>', unsafe_allow_html=True)
            cols = st.columns(min(num_images, 3))
            for i, p_img in enumerate(processed_images):
                with cols[i % min(num_images, 3)]:
                    st.image(p_img["plotted"], channels="BGR", use_column_width=True, caption=f"Image {i+1}" if num_images > 1 else None)

            # Nutrition Summary
            st.markdown(f"""<div class="premium-card" style="margin-top:2rem;">
                <h4 style="color:white;margin-bottom:1.5rem;">Total Nutrition Summary</h4>
                <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                    <div style="flex:1;background:rgba(255,255,255,0.02);padding:1.5rem;border-radius:12px;border-left:4px solid #f64f59;">
                        <div style="color:#94a3b8;font-size:0.9rem;text-transform:uppercase;">Total Calories</div>
                        <div style="font-size:2.2rem;font-weight:bold;color:#fff;">{total_calories:.0f} <span style="font-size:1rem;color:#94a3b8;">kcal</span></div>
                    </div>
                    <div style="flex:1;background:rgba(255,255,255,0.02);padding:1.5rem;border-radius:12px;border-left:4px solid #4facfe;">
                        <div style="color:#94a3b8;font-size:0.9rem;text-transform:uppercase;">Total Protein</div>
                        <div style="font-size:2.2rem;font-weight:bold;color:#fff;">{total_protein:.1f} <span style="font-size:1rem;color:#94a3b8;">g</span></div>
                    </div>
                </div>
                <div style="display:flex;gap:1rem;">
                    <div style="flex:1;background:rgba(255,255,255,0.02);padding:1.5rem;border-radius:12px;border-left:4px solid #f7b733;">
                        <div style="color:#94a3b8;font-size:0.9rem;text-transform:uppercase;">Total Carbs</div>
                        <div style="font-size:2.2rem;font-weight:bold;color:#fff;">{total_carbs:.1f} <span style="font-size:1rem;color:#94a3b8;">g</span></div>
                    </div>
                    <div style="flex:1;background:rgba(255,255,255,0.02);padding:1.5rem;border-radius:12px;border-left:4px solid #c471ed;">
                        <div style="color:#94a3b8;font-size:0.9rem;text-transform:uppercase;">Total Fat</div>
                        <div style="font-size:2.2rem;font-weight:bold;color:#fff;">{total_fat:.1f} <span style="font-size:1rem;color:#94a3b8;">g</span></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Detection table
            st.markdown(f'<h4 style="margin-top:1.5rem;">🥘 Combined Items ({len(detected_items)} found)</h4>', unsafe_allow_html=True)
            detection_data = []
            for item in detected_items:
                raw_food_name = item["food"].split(" (Img")[0] # remove image suffix for lookup
                n = get_nutrition_info(raw_food_name)
                detection_data.append({
                    "🍽️ Food": item["food"].title(),
                    "📊 Calories": f"{item['calories']} kcal",
                    "💪 Protein": f"{n['protein']}g",
                    "🧈 Fat": f"{n['fat']}g",
                    "🌾 Carbs": f"{n['carbs']}g",
                    "🎯 Confidence": f"{item['confidence']}%"
                })
            st.dataframe(detection_data, use_container_width=True)

            # Health analysis
            st.markdown('<h4 style="margin-top:2rem;">❤️ Health Analysis</h4>', unsafe_allow_html=True)
            cal_status = evaluation["calorie_status"]
            cal_color = "#4CAF50" if "Light" in cal_status else "#FFC107" if "Moderate" in cal_status else "#F44336"
            ratios = meal.get_macro_ratios()
            ha1, ha2, ha3 = st.columns(3)
            with ha1:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);padding:1.2rem;border-radius:12px;border-left:4px solid {cal_color};margin-bottom:1rem;">
                    <div style="color:#94a3b8;font-size:0.85rem;">Calorie Level</div>
                    <div style="font-size:1.2rem;font-weight:bold;color:{cal_color};">{cal_status}</div>
                    <div style="font-size:0.8rem;color:#94a3b8;">{evaluation['calorie_percentage']:.1f}% of daily needs</div>
                </div>""", unsafe_allow_html=True)
            with ha2:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);padding:1.2rem;border-radius:12px;border-left:4px solid #4facfe;margin-bottom:1rem;">
                    <div style="color:#94a3b8;font-size:0.85rem;">Macro Balance</div>
                    <div style="font-size:0.9rem;color:white;margin-top:4px;">🥩 Protein: {ratios['protein']:.1f}%</div>
                    <div style="font-size:0.9rem;color:white;">🧈 Fat: {ratios['fat']:.1f}%</div>
                    <div style="font-size:0.9rem;color:white;">🌾 Carbs: {ratios['carbs']:.1f}%</div>
                </div>""", unsafe_allow_html=True)
            with ha3:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);padding:1.2rem;border-radius:12px;border-left:4px solid #4ECDC4;margin-bottom:1rem;">
                    <div style="color:#94a3b8;font-size:0.85rem;">Diet Category</div>
                    <div style="font-size:1.2rem;font-weight:bold;color:#4ECDC4;">{diet_category}</div>
                </div>""", unsafe_allow_html=True)

            # Nutritional status
            st.markdown('<h4 style="margin-top:1rem;">📋 Nutritional Status</h4>', unsafe_allow_html=True)
            def _badge(label, status, good_kw, bad_kw):
                s = status.lower()
                c = "#4CAF50" if any(k in s for k in good_kw) else "#F44336" if any(k in s for k in bad_kw) else "#FFC107"
                return f'<div style="background:rgba(255,255,255,0.03);padding:1rem;border-radius:12px;border-left:4px solid {c};margin-bottom:0.8rem;"><strong style="color:{c};">{label}</strong><br><span style="color:white;font-size:0.9rem;">{status}</span></div>'
            ns1, ns2, ns3 = st.columns(3)
            with ns1:
                st.markdown(_badge("🧈 Fat", evaluation["fat_status"], ["low","good"], ["high","excess"]), unsafe_allow_html=True)
                st.markdown(_badge("🍬 Sugar", evaluation["sugar_status"], ["low","good"], ["high","excess"]), unsafe_allow_html=True)
            with ns2:
                st.markdown(_badge("💪 Protein", evaluation["protein_status"], ["high","good","adequate"], ["low"]), unsafe_allow_html=True)
                st.markdown(_badge("🌾 Fiber", evaluation["fiber_status"], ["good","high"], ["low"]), unsafe_allow_html=True)
            with ns3:
                st.markdown(_badge("🧂 Sodium", evaluation["sodium_status"], ["low","good"], ["high","excess"]), unsafe_allow_html=True)

            # Charts (5 tabs)
            if show_charts:
                st.markdown('<h4 style="margin-top:2rem;">📈 Visualizations</h4>', unsafe_allow_html=True)
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["🥧 Macros", "📊 Nutrition", "🎯 Gauge", "❤️ Health", "🍽️ Items"])
                with tab1:
                    fig = create_macro_distribution_pie(meal)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)
                with tab2:
                    fig = create_nutrition_bars(meal)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)
                with tab3:
                    fig = create_calorie_gauge(total_calories, user.get_daily_calorie_needs())
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)
                with tab4:
                    fig = create_health_indicators(evaluation)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)
                with tab5:
                    fig = create_food_items_bar(detected_items)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)

            # All AI Recommendations
            st.markdown('<h4 style="margin-top:2rem;">💡 AI Recommendations</h4>', unsafe_allow_html=True)
            for rec in recommendations:
                st.info(rec)

            # PDF Export
            st.markdown('<h4 style="margin-top:2rem;">📄 Export Report</h4>', unsafe_allow_html=True)
            btn_label = "📥 Generate & Download PDF Report"
            if st.button(btn_label, use_container_width=True, key="pdf_combined"):
                with st.spinner("Compiling PDF..."):
                    try:
                        pdf_bytes = generate_pdf_report(meal=meal, user=user, food_items=detected_items, evaluation=evaluation, recommendations=recommendations, diet_category=diet_category)
                        filename = f"nutrition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.download_button(label="⬇️ Download PDF Report", data=pdf_bytes, file_name=filename, mime="application/pdf", use_container_width=True, key="dl_combined")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
        else:
            st.warning("❌ No food items detected in any of the uploaded images.")
            st.info("💡 Try different images or adjust the confidence threshold in Advanced Settings.")

        for tf in temp_files:
            try:
                os.unlink(tf)
            except:
                pass




# =========================
# PAGE: REPORTS
# =========================
elif page == "Reports":
    st.markdown('<h2 style="margin-bottom: 2rem;">Analysis Reports</h2>', unsafe_allow_html=True)
    
    if st.session_state.analysis_complete and st.session_state.detection_results:
        results = st.session_state.detection_results
        meal = results["meal"]
        detected_items = results["detected_items"]
        evaluation = HealthAnalyzer.evaluate_meal_health(meal, user)
        recommendations = RecommendationEngine.generate_meal_recommendations(meal, user)
        diet_category = RecommendationEngine.get_diet_category(meal)
        
        st.success("✅ Previous analysis available — ready to export!")
        if st.button("📥 Generate PDF Report", use_container_width=True):
            with st.spinner("Compiling document..."):
                try:
                    pdf_bytes = generate_pdf_report(meal=meal, user=user, food_items=detected_items, evaluation=evaluation, recommendations=recommendations, diet_category=diet_category)
                    filename = f"nutrition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    st.download_button(label="⬇️ Download Report", data=pdf_bytes, file_name=filename, mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("📸 Please analyze a food image first on the Dashboard before generating reports.")


# =========================
# PAGE: ABOUT
# =========================
elif page == "About":
    st.markdown('<h2 style="margin-bottom: 2rem;">System Overview</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4>Technology Stack</h4>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 1rem;">
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Computer Vision:</strong> YOLOv8, PyTorch, OpenCV</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Frontend interface:</strong> Streamlit</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Data Analytics:</strong> NumPy, Plotly</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Document Gen:</strong> FPDF2</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4>Performance Metrics</h4>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 1rem;">
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Speed:</strong> ~50-100ms per image</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Accuracy:</strong> 95%+ precision on trained dataset</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Classes:</strong> 12 core food categories</div>
            <div style="margin-bottom: 0.5rem;"><strong style="color: #4facfe;">Status:</strong> Production Ready</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)