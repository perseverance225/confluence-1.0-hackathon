import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import random
import time
from datetime import timedelta
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EcoTrack Pro",
    layout="wide",
    page_icon="🍃",
    initial_sidebar_state="expanded"
)

# --- ENHANCED STYLES ---
st.markdown("""
<style>
    /* MAIN BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    /* GAME CARDS */
    .game-card {
        background: linear-gradient(135deg, var(--color1) 0%, var(--color2) 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .game-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* BADGES */
    .badge {
        display: inline-block;
        padding: 6px 15px;
        background: linear-gradient(45deg, #ffd166 0%, #ffb142 100%);
        color: #333;
        border-radius: 20px;
        font-weight: 600;
        margin: 2px;
        box-shadow: 0 3px 10px rgba(255, 209, 102, 0.3);
    }
    
    /* ECO FACTORY GAME STYLES */
    .factory-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .factory-item {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #2E8B57;
        transition: all 0.3s ease;
    }
    
    .factory-item:hover {
        transform: translateX(10px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .factory-button {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .factory-button:hover {
        transform: scale(1.05);
    }
    
    /* WORD HUNT GAME */
    .word-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 5px;
        margin: 20px 0;
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .word-cell {
        aspect-ratio: 1;
        background: #e9ecef;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .word-cell:hover {
        background: #2E8B57;
        color: white;
    }
    
    .word-cell.selected {
        background: #ff6b6b;
        color: white;
        transform: scale(0.95);
    }
    
    /* ECO CALCULATOR */
    .calculator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 20px 0;
    }
    
    .calculator-input {
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 8px;
        padding: 10px;
        color: white;
        margin: 5px;
        width: 100%;
    }
    
    .calculator-input::placeholder {
        color: rgba(255,255,255,0.7);
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 139, 87, 0.3);
    }
    
    /* PROGRESS BARS */
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* ANIMATIONS */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .bounce {
        animation: bounce 0.5s ease;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 0.5s ease-in-out;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: white;
        padding: 5px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- KNOWLEDGE DATABASE ---
ECO_FACTS = [
    "🌳 A single tree can absorb 48 pounds of CO2 per year",
    "🌱 Plant-based diets reduce food emissions by up to 73%",
    "💡 LED bulbs use 75% less energy than incandescent bulbs",
    "🚗 Electric cars produce 60% fewer emissions than petrol cars",
    "💧 A 5-minute shower saves 50 liters of water",
    "🚲 Cycling 10km instead of driving saves 1.6kg of CO2",
    "📱 Recycling 1 million phones saves 35,000 lbs of copper",
    "☀️ Solar panels can pay back their carbon cost in just 2 years",
    "🍃 India's forest cover increased by 5,188 sq km in 5 years",
    "🚌 Public transport emits 95% less CO2 than private cars"
]

QUIZ_DATABASE = [
    {
        "question": "What saves more water: shorter showers or fixing leaks?",
        "options": ["Shorter showers", "Fixing leaks", "Both are equal", "Neither"],
        "answer": 1,
        "explanation": "A leaky faucet can waste 10,000+ liters per year - more than shower savings!"
    },
    {
        "question": "Which mode of transport has the lowest carbon footprint?",
        "options": ["Electric Car", "Bus", "Bicycle", "Train"],
        "answer": 2,
        "explanation": "Bicycles produce zero emissions during use - the greenest option!"
    },
    {
        "question": "How many trees needed to offset 1 ton of CO2 annually?",
        "options": ["5 trees", "15 trees", "25 trees", "50 trees"],
        "answer": 3,
        "explanation": "It takes about 50 mature trees to absorb 1 ton of CO2 each year"
    },
    {
        "question": "What percentage of global electricity could come from solar by 2050?",
        "options": ["10%", "25%", "45%", "60%"],
        "answer": 2,
        "explanation": "Solar could provide 45% of global electricity by 2050 with proper investment"
    },
    {
        "question": "Which household appliance uses the most energy?",
        "options": ["Refrigerator", "Air Conditioner", "Water Heater", "Washing Machine"],
        "answer": 1,
        "explanation": "AC units account for about 40% of household electricity in India"
    },
    {
        "question": "How much plastic ends up in oceans each year?",
        "options": ["1 million tons", "8 million tons", "15 million tons", "25 million tons"],
        "answer": 1,
        "explanation": "About 8 million tons of plastic enter oceans annually - equivalent to a garbage truck per minute"
    },
    {
        "question": "What's the CO2 saving of switching to LED bulbs?",
        "options": ["20%", "50%", "75%", "90%"],
        "answer": 2,
        "explanation": "LED bulbs use 75% less energy and last 25 times longer than incandescent bulbs"
    },
    {
        "question": "How much water is used to produce 1kg of rice?",
        "options": ["500L", "1,500L", "3,500L", "5,000L"],
        "answer": 2,
        "explanation": "Rice requires about 3,500 liters of water per kg - choose local grains!"
    }
]

# --- NEW GAME DATABASES ---

# ECO FACTORY GAME - Build sustainable products
ECO_FACTORY_ITEMS = {
    "Solar Panel": {
        "components": ["Silicon", "Glass", "Metal Frame", "Wiring"],
        "energy_saved": 400,  # kWh per year
        "co2_reduced": 200,   # kg per year
        "description": "Converts sunlight into electricity",
        "icon": "☀️"
    },
    "LED Bulb": {
        "components": ["LED Chip", "Heat Sink", "Plastic Case", "Circuit Board"],
        "energy_saved": 50,
        "co2_reduced": 25,
        "description": "Energy efficient lighting",
        "icon": "💡"
    },
    "Water Filter": {
        "components": ["Filter Cartridge", "Plastic Housing", "Activated Carbon", "Membrane"],
        "water_saved": 1000,  # liters per year
        "description": "Purifies tap water, reduces plastic bottles",
        "icon": "💧"
    },
    "Compost Bin": {
        "components": ["Plastic Bin", "Aeration Holes", "Lid", "Base Plate"],
        "waste_reduced": 100,  # kg per year
        "description": "Turns food waste into fertilizer",
        "icon": "🌱"
    }
}

# ECO WORD HUNT GAME
WORD_HUNT_WORDS = {
    "grid": [
        ['S', 'O', 'L', 'A', 'R', 'P', 'A', 'N'],
        ['E', 'L', 'E', 'C', 'T', 'R', 'I', 'C'],
        ['R', 'E', 'C', 'Y', 'C', 'L', 'E', 'S'],
        ['C', 'O', 'M', 'P', 'O', 'S', 'T', 'P'],
        ['A', 'U', 'T', 'O', 'M', 'O', 'B', 'I'],
        ['B', 'I', 'K', 'E', 'L', 'A', 'N', 'E'],
        ['P', 'L', 'A', 'S', 'T', 'I', 'C', 'S'],
        ['W', 'A', 'T', 'E', 'R', 'S', 'A', 'V']
    ],
    "words": ["SOLAR", "ELECTRIC", "RECYCLE", "COMPOST", "BIKE", "PLASTIC", "WATER", "PLANET", "GREEN", "ECO"]
}

# ECO CALCULATOR GAME - Calculate environmental impacts
ECO_CALCULATIONS = [
    {
        "question": "If you replace 10 incandescent bulbs with LEDs, how much CO2 do you save per year?",
        "hint": "Each LED saves 25kg CO2/year",
        "answer": 250,
        "unit": "kg CO₂",
        "explanation": "10 bulbs × 25kg each = 250kg CO₂ saved annually!"
    },
    {
        "question": "Cycling 20km instead of driving saves how much CO2?",
        "hint": "Car emits 170g CO2 per km",
        "answer": 3.4,
        "unit": "kg CO₂",
        "explanation": "20km × 0.17kg/km = 3.4kg CO₂ saved!"
    },
    {
        "question": "A 5-minute shorter shower saves how much water?",
        "hint": "Shower uses 10L per minute",
        "answer": 50,
        "unit": "liters",
        "explanation": "5 minutes × 10L/min = 50 liters saved!"
    },
    {
        "question": "Planting 5 trees offsets how much CO2 per year?",
        "hint": "Each tree absorbs 22kg CO2/year",
        "answer": 110,
        "unit": "kg CO₂",
        "explanation": "5 trees × 22kg = 110kg CO₂ absorbed annually!"
    }
]

# MEMORY GAME CARDS
MEMORY_GAME_CARDS = [
    {"front": "🚲", "back": "Bike: 0g CO2/km", "matched": False},
    {"front": "🚗", "back": "Car: 170g CO2/km", "matched": False},
    {"front": "🚌", "back": "Bus: 105g CO2/km", "matched": False},
    {"front": "✈️", "back": "Plane: 285g CO2/km", "matched": False},
    {"front": "💡", "back": "LED: 75% less energy", "matched": False},
    {"front": "💧", "back": "Shower: 50L saved/5min", "matched": False},
    {"front": "🌳", "back": "Tree: 22kg CO2/year", "matched": False},
    {"front": "☀️", "back": "Solar: 0 emissions", "matched": False}
]

# SORTING CHALLENGE
SORTING_CHALLENGE = {
    "title": "📊 Carbon Footprint Sorting",
    "items": [
        {"name": "Flight (1 hour)", "co2": 90, "icon": "✈️"},
        {"name": "Car (50km)", "co2": 8.5, "icon": "🚗"},
        {"name": "AC (8 hours)", "co2": 6.4, "icon": "❄️"},
        {"name": "Bus (50km)", "co2": 6, "icon": "🚌"},
        {"name": "Train (50km)", "co2": 2.5, "icon": "🚆"},
        {"name": "Bicycle (50km)", "co2": 0, "icon": "🚲"}
    ]
}

# --- EMISSION FACTORS ---
EMISSION_FACTORS = {
    "Flight": {"factor": 0.35, "unit": "per ₹100"},
    "Car Fuel": {"factor": 0.22, "unit": "per ₹100"},
    "Taxi/Cab": {"factor": 0.12, "unit": "per ₹100"},
    "Electricity": {"factor": 0.82, "unit": "per unit (kWh)"},
    "Food & Dining": {"factor": 0.04, "unit": "per ₹100"},
    "Groceries": {"factor": 0.03, "unit": "per ₹100"},
    "Shopping": {"factor": 0.06, "unit": "per ₹100"},
    "Public Transport": {"factor": 0.02, "unit": "per ₹100"},
    "Hotel Stay": {"factor": 0.15, "unit": "per ₹100"}
}

# --- SESSION STATE SETUP ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
    
if 'data' not in st.session_state:
    st.session_state.data = []
    
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {
        'current_question': random.choice(QUIZ_DATABASE),
        'score': 0,
        'questions_answered': 0,
        'last_answer': None,
        'streak': 0
    }
    
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'memory': {'cards': [], 'flipped': [], 'matches': 0, 'moves': 0},
        'sorting': {'score': 0, 'current_order': [], 'attempts': 0},
        'factory': {'built_items': [], 'points': 0, 'components': {}},
        'word_hunt': {'found_words': [], 'score': 0, 'selected_cells': []},
        'calculator': {'current_q': 0, 'score': 0, 'attempts': []},
        'total_score': 0,
        'badges': []
    }
    
if 'current_fact' not in st.session_state:
    st.session_state.current_fact = random.choice(ECO_FACTS)
    
if 'selected_indices' not in st.session_state:
    st.session_state.selected_indices = []
    
if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None

# --- HELPER FUNCTIONS ---
def calculate_co2(category, amount):
    """Calculate CO2 emissions based on category and amount"""
    if category == "Electricity":
        return round((amount / 8.0) * 0.82, 2)
    else:
        return round(amount * EMISSION_FACTORS[category]["factor"], 2)

def get_new_badges(score):
    """Award badges based on score"""
    badges = []
    if score >= 50 and "Beginner" not in st.session_state.game_state['badges']:
        badges.append("Beginner")
    if score >= 100 and "Eco Warrior" not in st.session_state.game_state['badges']:
        badges.append("Eco Warrior")
    if score >= 200 and "Climate Hero" not in st.session_state.game_state['badges']:
        badges.append("Climate Hero")
    if score >= 300 and "Planet Saver" not in st.session_state.game_state['badges']:
        badges.append("Planet Saver")
    
    return badges

def initialize_memory_game():
    """Initialize memory game cards"""
    cards = MEMORY_GAME_CARDS.copy()
    random.shuffle(cards)
    cards = cards[:8]
    game_cards = []
    for card in cards:
        game_cards.append({**card, 'id': len(game_cards), 'matched': False})
        game_cards.append({**card, 'id': len(game_cards), 'matched': False})
    
    random.shuffle(game_cards)
    return game_cards

def initialize_word_hunt():
    """Initialize word hunt game state"""
    return {
        'found_words': [],
        'score': 0,
        'selected_cells': []
    }

def initialize_eco_factory():
    """Initialize eco factory game state"""
    return {
        'built_items': [],
        'points': 0,
        'components': {
            'Silicon': 0, 'Glass': 0, 'Metal Frame': 0, 'Wiring': 0,
            'LED Chip': 0, 'Heat Sink': 0, 'Plastic Case': 0, 'Circuit Board': 0,
            'Filter Cartridge': 0, 'Plastic Housing': 0, 'Activated Carbon': 0, 'Membrane': 0,
            'Plastic Bin': 0, 'Aeration Holes': 0, 'Lid': 0, 'Base Plate': 0
        }
    }

# --- WELCOME SCREEN ---
if st.session_state.user_name is None:
    # Hero Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='
            text-align: center;
            padding: 3rem;
            background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
            border-radius: 25px;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(46, 139, 87, 0.3);
        '>
            <h1 style='font-size: 4rem; margin: 0;'>🍃 EcoTrack Pro</h1>
            <h3 style='font-weight: 300; margin: 1rem 0;'>Interactive Carbon Footprint Platform</h3>
            <p>Track, Learn, Play & Reduce Your Environmental Impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    # New Games Showcase
    st.subheader("🎮 Exciting New Games!")
    games = st.columns(3)
    
    with games[0]:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: white; border-radius: 15px;'>
            <div style='font-size: 3rem;'>🏭</div>
            <h4>Eco Factory</h4>
            <p>Build sustainable products</p>
        </div>
        """, unsafe_allow_html=True)
    
    with games[1]:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: white; border-radius: 15px;'>
            <div style='font-size: 3rem;'>🔍</div>
            <h4>Word Hunt</h4>
            <p>Find eco-words in grid</p>
        </div>
        """, unsafe_allow_html=True)
    
    with games[2]:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: white; border-radius: 15px;'>
            <div style='font-size: 3rem;'>🧮</div>
            <h4>Eco Calculator</h4>
            <p>Solve environmental math</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Login Section
    st.markdown("---")
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🚀 Start Your Eco Journey")
            
            name_input = st.text_input(
                "Enter your name:",
                placeholder="Type your name here...",
                key="login_name"
            )
            
            option = st.radio("Choose starting option:", 
                            ["Start with Sample Data", "Start Empty"])
            
            if st.button("🚀 Launch Dashboard", use_container_width=True, type="primary"):
                if name_input:
                    st.session_state.user_name = name_input
                    if option == "Start with Sample Data":
                        st.session_state.data = [
                            {"Date": datetime.date.today(), "Item": "Uber Ride", "Category": "Taxi/Cab", "Amount": 450, "CO2": 54.0},
                            {"Date": datetime.date.today() - timedelta(days=1), "Item": "Vegetarian Lunch", "Category": "Food & Dining", "Amount": 250, "CO2": 10.0},
                            {"Date": datetime.date.today() - timedelta(days=3), "Item": "Flight to Mumbai", "Category": "Flight", "Amount": 6000, "CO2": 2100.0},
                        ]
                    st.rerun()
                else:
                    st.warning("Please enter your name first!")
    
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    # User Profile
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    '>
        <h3 style='margin: 0;'>👤 {st.session_state.user_name}</h3>
        <div class='badge'>Level {min(10, len(st.session_state.data)//2 + 1)}</div>
        <p style='margin: 10px 0 0 0; opacity: 0.9;'>
            Game Score: {st.session_state.game_state['total_score']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    with st.expander("📊 Quick Stats", expanded=True):
        if st.session_state.data:
            df = pd.DataFrame(st.session_state.data)
            total_co2 = df['CO2'].sum()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("CO₂ Saved", f"{total_co2:.0f} kg")
            with col2:
                st.metric("Games Played", st.session_state.quiz_state['questions_answered'])
    
    # Did You Know
    with st.expander("💡 Eco Fact", expanded=True):
        st.info(st.session_state.current_fact)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()
    
    if st.button("🏆 View Badges", use_container_width=True):
        st.session_state.show_badges = True

# --- MAIN APP WITH TABS ---
st.markdown(f"# 🍃 Welcome back, {st.session_state.user_name}!")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📝 Data Manager", "🧠 Eco Quiz", "🎮 Interactive Games"])

# --- TAB 1: DASHBOARD ---
with tab1:
    if not st.session_state.data:
        st.info("🌱 Start by adding your first transaction in the Data Manager tab!")
    else:
        df = pd.DataFrame(st.session_state.data)
        
        # Top Metrics
        total_co2 = df['CO2'].sum()
        total_spent = df['Amount'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem;'>🌍</div>
                <h3 style='color: #d9534f;'>{total_co2:.1f} kg</h3>
                <p>Total CO₂</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem;'>💰</div>
                <h3 style='color: #2E8B57;'>₹{total_spent:,.0f}</h3>
                <p>Total Spent</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            trees_needed = int(total_co2 / 20)
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem;'>🌳</div>
                <h3 style='color: #339af0;'>{trees_needed}</h3>
                <p>Trees to Offset</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem;'>🎮</div>
                <h3 style='color: #f76707;'>{st.session_state.game_state['total_score']}</h3>
                <p>Game Score</p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: DATA MANAGER ---
with tab2:
    st.header("📝 Manage Your Carbon Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Add New Transaction
        with st.form("add_form"):
            st.subheader("➕ Add New Activity")
            
            col_date, col_item = st.columns(2)
            with col_date:
                date = st.date_input("Date", datetime.date.today())
            with col_item:
                item = st.text_input("Description", placeholder="e.g., Uber ride, Groceries")
            
            col_cat, col_amt = st.columns(2)
            with col_cat:
                category = st.selectbox("Category", list(EMISSION_FACTORS.keys()))
            with col_amt:
                amount = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=100.0)
            
            if amount > 0:
                co2 = calculate_co2(category, amount)
                st.info(f"Estimated CO₂: **{co2:.1f} kg**")
            
            if st.form_submit_button("Add Activity", type="primary"):
                if item and amount > 0:
                    st.session_state.data.append({
                        "Date": date,
                        "Item": item,
                        "Category": category,
                        "Amount": amount,
                        "CO2": co2
                    })
                    st.success(f"✅ Added {item} ({co2:.1f} kg CO₂)")
                    st.rerun()

# --- TAB 3: ECO QUIZ ---
with tab3:
    st.header("🧠 Sustainability Quiz")
    
    quiz = st.session_state.quiz_state['current_question']
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    '>
        <h3 style='margin: 0 0 1rem 0;'>Question:</h3>
        <p style='font-size: 1.2rem; font-weight: 500;'>{quiz['question']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = st.radio("Choose your answer:", quiz['options'], key="quiz_answer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if quiz['options'].index(selected) == quiz['answer']:
                st.session_state.quiz_state['score'] += 10
                st.session_state.quiz_state['streak'] += 1
                st.success(f"🎉 Correct! +10 points (Streak: {st.session_state.quiz_state['streak']})")
            else:
                st.session_state.quiz_state['streak'] = 0
                st.error(f"❌ Wrong! Correct answer: {quiz['options'][quiz['answer']]}")
            st.session_state.quiz_state['last_answer'] = quiz['explanation']
    
    with col2:
        if st.button("🔄 New Question", use_container_width=True):
            st.session_state.quiz_state['current_question'] = random.choice(
                [q for q in QUIZ_DATABASE if q != quiz]
            )
            st.session_state.quiz_state['questions_answered'] += 1
            st.rerun()

# --- TAB 4: INTERACTIVE GAMES ---
with tab4:
    st.header("🎮 Interactive Eco Games")
    
    # Game selector
    game_choice = st.selectbox(
        "Choose a game to play:",
        ["🧠 Eco Memory Challenge", "📊 Carbon Sorting Game", "🏭 Eco Factory", "🔍 Eco Word Hunt", "🧮 Eco Calculator"]
    )
    
    st.markdown("---")
    
    # GAME 1: MEMORY GAME
    if game_choice == "🧠 Eco Memory Challenge":
        st.subheader("🧠 Eco-Facts Memory Game")
        st.write("Find matching pairs of eco-icons and their facts")
        
        # Initialize game if needed
        if not st.session_state.game_state['memory']['cards']:
            st.session_state.game_state['memory']['cards'] = initialize_memory_game()
        
        # Display game stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Matches", st.session_state.game_state['memory']['matches'])
        with col2:
            st.metric("Moves", st.session_state.game_state['memory']['moves'])
        with col3:
            st.metric("Score", st.session_state.game_state['total_score'])
        
        # Game grid
        st.write("Click on cards to reveal them and find matching pairs:")
        cols = st.columns(4)
        
        for i in range(0, 16, 4):
            for j in range(4):
                card_idx = i + j
                if card_idx < len(st.session_state.game_state['memory']['cards']):
                    card = st.session_state.game_state['memory']['cards'][card_idx]
                    col = cols[j]
                    
                    with col:
                        is_flipped = card_idx in st.session_state.game_state['memory']['flipped'] or card['matched']
                        
                        if is_flipped:
                            btn_text = card['back']
                            btn_type = "primary"
                        else:
                            btn_text = "❓"
                            btn_type = "secondary"
                        
                        if st.button(
                            btn_text,
                            key=f"mem_{card_idx}",
                            use_container_width=True,
                            type=btn_type,
                            disabled=card['matched']
                        ) and not card['matched']:
                            if len(st.session_state.game_state['memory']['flipped']) < 2:
                                st.session_state.game_state['memory']['flipped'].append(card_idx)
                                st.session_state.game_state['memory']['moves'] += 1
                                
                                # Check for match if two cards are flipped
                                if len(st.session_state.game_state['memory']['flipped']) == 2:
                                    idx1, idx2 = st.session_state.game_state['memory']['flipped']
                                    card1 = st.session_state.game_state['memory']['cards'][idx1]
                                    card2 = st.session_state.game_state['memory']['cards'][idx2]
                                    
                                    if card1['back'] == card2['back']:
                                        # Match found
                                        st.session_state.game_state['memory']['cards'][idx1]['matched'] = True
                                        st.session_state.game_state['memory']['cards'][idx2]['matched'] = True
                                        st.session_state.game_state['memory']['matches'] += 1
                                        st.session_state.game_state['memory']['flipped'] = []
                                        
                                        # Add score
                                        st.session_state.game_state['total_score'] += 20
                                        st.success("🎉 Match found! +20 points")
                                    else:
                                        # No match
                                        st.warning("No match! Try again.")
                                        time.sleep(1)
                                        st.session_state.game_state['memory']['flipped'] = []
                                
                                st.rerun()
        
        # Game controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Game", type="secondary", use_container_width=True):
                st.session_state.game_state['memory'] = {
                    'cards': initialize_memory_game(),
                    'flipped': [],
                    'matches': 0,
                    'moves': 0
                }
                st.rerun()
        
        with col2:
            if st.button("🏆 Earn Points", type="primary", use_container_width=True):
                points = st.session_state.game_state['memory']['matches'] * 10
                st.session_state.game_state['total_score'] += points
                st.success(f"🎉 +{points} points earned!")
                st.rerun()
    
    # GAME 2: SORTING GAME
    elif game_choice == "📊 Carbon Sorting Game":
        st.subheader("📊 Carbon Footprint Sorting Challenge")
        st.write("Sort these activities from HIGHEST to LOWEST carbon footprint")
        
        # Initialize sorting order
        if not st.session_state.game_state['sorting']['current_order']:
            items = list(range(len(SORTING_CHALLENGE['items'])))
            random.shuffle(items)
            st.session_state.game_state['sorting']['current_order'] = items
        
        # Display items in current order
        st.write("**Current Order:**")
        for pos, idx in enumerate(st.session_state.game_state['sorting']['current_order']):
            item = SORTING_CHALLENGE['items'][idx]
            cols = st.columns([1, 4, 2, 2])
            with cols[0]:
                st.write(f"**{pos + 1}.**")
            with cols[1]:
                st.write(f"{item['icon']} {item['name']}")
            with cols[2]:
                st.write(f"**{item['co2']} kg** CO₂")
            with cols[3]:
                col_up, col_down = st.columns(2)
                with col_up:
                    if st.button("↑", key=f"up_{idx}"):
                        if pos > 0:
                            st.session_state.game_state['sorting']['current_order'][pos], \
                            st.session_state.game_state['sorting']['current_order'][pos-1] = \
                            st.session_state.game_state['sorting']['current_order'][pos-1], \
                            st.session_state.game_state['sorting']['current_order'][pos]
                            st.rerun()
                with col_down:
                    if st.button("↓", key=f"down_{idx}"):
                        if pos < len(SORTING_CHALLENGE['items']) - 1:
                            st.session_state.game_state['sorting']['current_order'][pos], \
                            st.session_state.game_state['sorting']['current_order'][pos+1] = \
                            st.session_state.game_state['sorting']['current_order'][pos+1], \
                            st.session_state.game_state['sorting']['current_order'][pos]
                            st.rerun()
        
        # Check order button
        if st.button("✅ Check Order", type="primary", use_container_width=True):
            # Calculate correct order (sorted by CO2 descending)
            correct_order = sorted(
                range(len(SORTING_CHALLENGE['items'])), 
                key=lambda i: SORTING_CHALLENGE['items'][i]['co2'], 
                reverse=True
            )
            
            # Check how many are in correct position
            correct_positions = sum(
                1 for i, idx in enumerate(st.session_state.game_state['sorting']['current_order'])
                if idx == correct_order[i]
            )
            
            score = correct_positions * 15
            st.session_state.game_state['total_score'] += score
            st.session_state.game_state['sorting']['attempts'] += 1
            
            # Display results
            if correct_positions == len(SORTING_CHALLENGE['items']):
                st.balloons()
                st.success(f"🎉 Perfect! All items in correct order! +{score} points")
            else:
                st.info(f"📊 {correct_positions}/{len(SORTING_CHALLENGE['items'])} correct. +{score} points")
                
                # Show correct order
                st.write("**Correct Order:**")
                for i, idx in enumerate(correct_order):
                    item = SORTING_CHALLENGE['items'][idx]
                    st.write(f"{i + 1}. {item['icon']} {item['name']} ({item['co2']} kg CO₂)")
    
    # GAME 3: ECO FACTORY
    elif game_choice == "🏭 Eco Factory":
        st.subheader("🏭 Eco Factory - Build Sustainable Products")
        st.write("Collect components and build eco-friendly products to earn points!")
        
        # Initialize factory if needed
        if not st.session_state.game_state['factory']['components']:
            st.session_state.game_state['factory'] = initialize_eco_factory()
        
        # Game stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Built Items", len(st.session_state.game_state['factory']['built_items']))
        with col2:
            st.metric("Factory Points", st.session_state.game_state['factory']['points'])
        with col3:
            st.metric("Total Score", st.session_state.game_state['total_score'])
        
        # Collect Components Section
        st.markdown("### 🔧 Collect Components")
        st.write("Click to collect random components:")
        
        if st.button("🔄 Collect Components", type="primary", use_container_width=True):
            # Add 3 random components
            all_components = list(st.session_state.game_state['factory']['components'].keys())
            collected = random.sample(all_components, 3)
            for component in collected:
                st.session_state.game_state['factory']['components'][component] += 1
            
            st.success(f"Collected: {', '.join(collected)}!")
            st.rerun()
        
        # Show current inventory
        st.markdown("### 📦 Your Inventory")
        inventory_cols = st.columns(4)
        components_list = list(st.session_state.game_state['factory']['components'].items())
        
        for i, (component, count) in enumerate(components_list):
            with inventory_cols[i % 4]:
                if count > 0:
                    st.info(f"**{component}**: {count}")
                else:
                    st.text(f"{component}: 0")
        
        # Build Products Section
        st.markdown("### 🛠️ Build Eco Products")
        st.write("Use your components to build sustainable products:")
        
        product_cols = st.columns(2)
        
        for i, (product_name, product_info) in enumerate(ECO_FACTORY_ITEMS.items()):
            with product_cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class='factory-item'>
                        <h4>{product_info['icon']} {product_name}</h4>
                        <p>{product_info['description']}</p>
                        <p><strong>Components needed:</strong></p>
                        <p>{', '.join(product_info['components'])}</p>
                        <p><strong>Impact:</strong> {product_info.get('co2_reduced', product_info.get('water_saved', product_info.get('waste_reduced', 0)))} {
                            'kg CO₂/year' if 'co2_reduced' in product_info else 
                            'liters/year' if 'water_saved' in product_info else 
                            'kg waste/year'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Check if player has all components
                    can_build = all(
                        st.session_state.game_state['factory']['components'][comp] > 0
                        for comp in product_info['components']
                    )
                    
                    if st.button(f"Build {product_name}", key=f"build_{i}", 
                               disabled=not can_build, use_container_width=True):
                        if can_build:
                            # Deduct components
                            for comp in product_info['components']:
                                st.session_state.game_state['factory']['components'][comp] -= 1
                            
                            # Add to built items
                            st.session_state.game_state['factory']['built_items'].append(product_name)
                            
                            # Add points
                            points = len(product_info['components']) * 10
                            st.session_state.game_state['factory']['points'] += points
                            st.session_state.game_state['total_score'] += points
                            
                            st.balloons()
                            st.success(f"🎉 Built {product_name}! +{points} points")
                            st.rerun()
        
        # Built Items Display
        if st.session_state.game_state['factory']['built_items']:
            st.markdown("### 🏗️ Your Built Products")
            built_cols = st.columns(4)
            for i, item in enumerate(st.session_state.game_state['factory']['built_items'][-8:]):
                with built_cols[i % 4]:
                    info = ECO_FACTORY_ITEMS[item]
                    st.success(f"{info['icon']} {item}")
    
    # GAME 4: ECO WORD HUNT
    elif game_choice == "🔍 Eco Word Hunt":
        st.subheader("🔍 Eco Word Hunt")
        st.write("Find hidden eco-words in the grid (horizontal, vertical, or diagonal)")
        
        # Initialize word hunt if needed
        if not st.session_state.game_state['word_hunt']['found_words']:
            st.session_state.game_state['word_hunt'] = initialize_word_hunt()
        
        # Game stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Found Words", len(st.session_state.game_state['word_hunt']['found_words']))
        with col2:
            st.metric("Word Hunt Score", st.session_state.game_state['word_hunt']['score'])
        with col3:
            st.metric("Total Score", st.session_state.game_state['total_score'])
        
        # Word list
        st.write("**Words to find:**")
        words_cols = st.columns(4)
        for i, word in enumerate(WORD_HUNT_WORDS['words']):
            with words_cols[i % 4]:
                if word in st.session_state.game_state['word_hunt']['found_words']:
                    st.success(f"✅ {word}")
                else:
                    st.info(f"❓ {word}")
        
        # Word grid
        st.write("**Click letters to select them, then click 'Check Word' to see if you found a word:**")
        
        # Create grid display with selection
        grid_html = "<div class='word-grid'>"
        for i, row in enumerate(WORD_HUNT_WORDS['grid']):
            for j, letter in enumerate(row):
                cell_id = f"{i}_{j}"
                is_selected = cell_id in st.session_state.game_state['word_hunt']['selected_cells']
                cell_class = "word-cell selected" if is_selected else "word-cell"
                grid_html += f"<div class='{cell_class}' onclick='selectCell(\"{cell_id}\")'>{letter}</div>"
        grid_html += "</div>"
        
        st.markdown(grid_html, unsafe_allow_html=True)
        
        # Selection interface (simulated)
        st.write("**Selected Letters:**")
        selected_letters = ""
        for cell_id in st.session_state.game_state['word_hunt']['selected_cells']:
            i, j = map(int, cell_id.split('_'))
            selected_letters += WORD_HUNT_WORDS['grid'][i][j] + " "
        
        st.write(f"`{selected_letters}`")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Simple word input since we can't do real click selection
            user_word = st.text_input("Type the word you found:", "").upper()
            
        with col2:
            if st.button("🔍 Check Word", type="primary", use_container_width=True):
                if user_word:
                    if user_word in WORD_HUNT_WORDS['words']:
                        if user_word not in st.session_state.game_state['word_hunt']['found_words']:
                            st.session_state.game_state['word_hunt']['found_words'].append(user_word)
                            points = len(user_word) * 5
                            st.session_state.game_state['word_hunt']['score'] += points
                            st.session_state.game_state['total_score'] += points
                            st.balloons()
                            st.success(f"🎉 Found '{user_word}'! +{points} points")
                        else:
                            st.warning(f"'{user_word}' already found!")
                    else:
                        st.error(f"'{user_word}' is not in the word list!")
                    st.rerun()
        
        with col3:
            if st.button("🔄 Clear Selection", type="secondary", use_container_width=True):
                st.session_state.game_state['word_hunt']['selected_cells'] = []
                st.rerun()
        
        # Game controls
        if st.button("🔄 New Game", type="secondary", use_container_width=True):
            st.session_state.game_state['word_hunt'] = initialize_word_hunt()
            st.rerun()
    
    # GAME 5: ECO CALCULATOR
    else:
        st.subheader("🧮 Eco Calculator Challenge")
        st.write("Solve these environmental math problems to earn points!")
        
        # Initialize calculator if needed
        if st.session_state.game_state['calculator']['current_q'] >= len(ECO_CALCULATIONS):
            st.session_state.game_state['calculator']['current_q'] = 0
        
        current_q = st.session_state.game_state['calculator']['current_q']
        problem = ECO_CALCULATIONS[current_q]
        
        # Display problem
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin: 1rem 0;
        '>
            <h3 style='margin: 0 0 1rem 0;'>Problem {current_q + 1}/{len(ECO_CALCULATIONS)}</h3>
            <p style='font-size: 1.2rem; font-weight: 500;'>{problem['question']}</p>
            <p><strong>Hint:</strong> {problem['hint']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Game stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Calculator Score", st.session_state.game_state['calculator']['score'])
        with col2:
            st.metric("Total Score", st.session_state.game_state['total_score'])
        
        # Answer input
        col1, col2 = st.columns([2, 1])
        with col1:
            user_answer = st.number_input(
                f"Your answer ({problem['unit']}):",
                min_value=0.0,
                value=0.0,
                step=0.1,
                key=f"calc_{current_q}"
            )
        
        with col2:
            st.write("")  # Spacer
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                # Check if answer is correct (allow some tolerance)
                tolerance = 0.1
                is_correct = abs(user_answer - problem['answer']) <= tolerance
                
                if is_correct:
                    points = 25
                    st.session_state.game_state['calculator']['score'] += points
                    st.session_state.game_state['total_score'] += points
                    st.session_state.game_state['calculator']['attempts'].append({
                        'problem': current_q,
                        'correct': True,
                        'points': points
                    })
                    
                    st.balloons()
                    st.success(f"🎉 Correct! +{points} points")
                    st.info(f"**Explanation:** {problem['explanation']}")
                    
                    # Move to next question
                    st.session_state.game_state['calculator']['current_q'] += 1
                    if st.session_state.game_state['calculator']['current_q'] >= len(ECO_CALCULATIONS):
                        st.session_state.game_state['calculator']['current_q'] = 0
                        st.balloons()
                        st.success("🎊 You completed all problems! Starting over...")
                else:
                    st.session_state.game_state['calculator']['attempts'].append({
                        'problem': current_q,
                        'correct': False,
                        'user_answer': user_answer
                    })
                    st.error(f"❌ Incorrect. Try again!")
                
                st.rerun()
        
        # Skip button
        if st.button("⏭️ Skip Problem", type="secondary", use_container_width=True):
            st.session_state.game_state['calculator']['current_q'] += 1
            if st.session_state.game_state['calculator']['current_q'] >= len(ECO_CALCULATIONS):
                st.session_state.game_state['calculator']['current_q'] = 0
            st.rerun()

# --- BADGES DISPLAY ---
if 'show_badges' in st.session_state and st.session_state.show_badges:
    st.markdown("---")
    st.header("🏆 Your Eco Badges")
    
    badges = st.session_state.game_state['badges']
    if badges:
        cols = st.columns(4)
        for i, badge in enumerate(badges):
            with cols[i % 4]:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ffd166 0%, #ffb142 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    margin: 0.5rem 0;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                '>
                    <div style='font-size: 2.5rem;'>🏅</div>
                    <h4>{badge}</h4>
                    <p style='font-size: 0.9rem;'>Eco Achievement</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🎯 Play games to earn badges! Complete challenges to unlock achievements.")
    
    if st.button("Close Badges", use_container_width=True):
        st.session_state.show_badges = False
        st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🍃 <strong>EcoTrack Pro</strong> | Track • Learn • Play • Reduce</p>
    <p style='font-size: 0.9rem;'>Making sustainability fun and interactive! 🌍🎮</p>
</div>
""", unsafe_allow_html=True)
