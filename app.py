import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import random
from streamlit_option_menu import option_menu

# --- 1. ENHANCED CONFIGURATION & PROFESSIONAL STYLE ---
st.set_page_config(
    page_title="EcoTrack Pro",
    layout="wide",
    page_icon="🍃",
    initial_sidebar_state="expanded"
)

# MODERN CSS WITH GRADIENTS AND ANIMATIONS
st.markdown("""
<style>
    /* MAIN BACKGROUND WITH SUBTLE GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        background-attachment: fixed;
    }
    
    /* GRADIENT HEADER */
    .gradient-header {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.15);
        color: white;
        text-align: center;
    }
    
    /* GLASSMORPHISM CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.1);
    }
    
    /* METRIC CARDS WITH ICONS */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-left: 5px solid;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 10px 0;
    }
    
    .metric-card.red { border-left-color: #ff6b6b; }
    .metric-card.green { border-left-color: #51cf66; }
    .metric-card.blue { border-left-color: #339af0; }
    
    /* FACT CARDS */
    .fact-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* QUIZ STYLING */
    .quiz-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
    }
    
    .quiz-option {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quiz-option:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.02);
    }
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 139, 87, 0.3);
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
    }
    
    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* DATA TABLE STYLING */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
        color: white !important;
    }
    
    /* BADGE STYLING */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(90deg, #ffd166 0%, #ffb142 100%);
        color: #333;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. KNOWLEDGE DATABASE ---
ECO_FACTS = [
    "A single tree can absorb up to 48 pounds of CO2 per year",
    "Plant-based diets can reduce food-related emissions by up to 73%",
    "If everyone in India used LED bulbs, we could save 50 million tons of CO2 annually",
    "A vegetarian meal saves about 1.5kg of CO2 compared to a meat-based meal",
    "Unplugging electronics can save up to 10% on electricity bills",
    "One flight from Mumbai to Delhi emits about 175kg of CO2 per passenger",
    "Public transport emits 95% less CO2 per passenger than private cars",
    "India aims to achieve 50% renewable energy capacity by 2030",
    "A laptop uses 80% less energy than a desktop computer",
    "Recycling one aluminum can saves enough energy to run a TV for 3 hours"
]

QUIZ_QUESTIONS = [
    {
        "question": "What percentage of global emissions comes from the food sector?",
        "options": ["15%", "26%", "35%", "42%"],
        "correct": 1,
        "explanation": "The food sector contributes about 26% of global greenhouse gas emissions."
    },
    {
        "question": "How much CO2 does 1km of driving a petrol car produce?",
        "options": ["100g", "170g", "250g", "320g"],
        "correct": 1,
        "explanation": "A typical petrol car emits about 170g of CO2 per kilometer."
    },
    {
        "question": "Which activity has the highest carbon footprint?",
        "options": ["1 hour of AC use", "10km drive in car", "1kg of beef", "Charging phone for a year"],
        "correct": 2,
        "explanation": "1kg of beef produces about 27kg of CO2, equivalent to driving 160km!"
    },
    {
        "question": "What's the CO2 saving of switching to LED bulbs?",
        "options": ["20%", "50%", "75%", "90%"],
        "correct": 2,
        "explanation": "LED bulbs use 75% less energy and last 25 times longer than incandescent bulbs."
    },
    {
        "question": "How many trees needed to offset 1 ton of CO2 annually?",
        "options": ["1-2 trees", "5-10 trees", "15-20 trees", "50+ trees"],
        "correct": 3,
        "explanation": "It takes about 50 mature trees to absorb 1 ton of CO2 each year."
    }
]

# --- 3. SESSION STATE SETUP ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"
if 'data' not in st.session_state:
    st.session_state.data = [
        {"Date": datetime.date.today(), "Item": "Uber Ride", "Category": "Taxi/Cab", "Amount": 450, "CO2": 54.0},
        {"Date": datetime.date.today(), "Item": "Starbucks", "Category": "Food & Dining", "Amount": 350, "CO2": 14.0},
        {"Date": datetime.date.today(), "Item": "Flight to Delhi", "Category": "Flight", "Amount": 5000, "CO2": 1750.0},
    ]
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = random.choice(QUIZ_QUESTIONS)
if 'fact_shown' not in st.session_state:
    st.session_state.fact_shown = random.choice(ECO_FACTS)

# --- 4. WELCOME SCREEN WITH ENHANCED DESIGN ---
if st.session_state.user_name == "Guest":
    # Hero Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='font-size: 3.5rem; color: #2E8B57; margin-bottom: 1rem;'>🍃 EcoTrack Pro</h1>
            <h3 style='color: #666; font-weight: 300;'>Intelligent Carbon Footprint Analytics</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("---")
    st.subheader("🌱 Features That Make a Difference")
    
    features = st.columns(3)
    with features[0]:
        st.markdown("""
        <div class='glass-card'>
            <h3>📊 Smart Analytics</h3>
            <p>Real-time carbon footprint tracking with advanced visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features[1]:
        st.markdown("""
        <div class='glass-card'>
            <h3>🎯 Personalized Goals</h3>
            <p>Set and track sustainability targets tailored to your lifestyle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features[2]:
        st.markdown("""
        <div class='glass-card'>
            <h3>🌍 Impact Insights</h3>
            <p>Learn how small changes create big environmental impacts</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Did You Know Section
    st.markdown("---")
    st.markdown(f"""
    <div class='fact-card'>
        <h3>🌍 DID YOU KNOW?</h3>
        <p style='font-size: 1.2rem;'>{st.session_state.fact_shown}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Section
    st.markdown("---")
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Ready to Track Your Impact?")
            name_input = st.text_input("Enter your name to begin:", placeholder="Enter your name...")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🚀 Launch Dashboard", use_container_width=True):
                    if name_input:
                        st.session_state.user_name = name_input
                        st.rerun()
                    else:
                        st.warning("Please enter your name")
    
    st.stop()

# --- 5. EMISSION FACTORS ---
EMISSION_FACTORS = {
    "Flight": 0.35,
    "Car Fuel": 0.22,
    "Taxi/Cab": 0.12,
    "Electricity": 0.82, 
    "Food & Dining": 0.04,
    "Groceries": 0.03,
    "Shopping": 0.06,
    "Public Transport": 0.02,
    "Hotel Stay": 0.15
}

# --- 6. SIDEBAR WITH ENHANCED DESIGN ---
with st.sidebar:
    # User Profile Card
    st.markdown(f"""
    <div class='glass-card' style='text-align: center; margin-bottom: 2rem;'>
        <h3>👤 {st.session_state.user_name}</h3>
        <div class='badge'>🌱 Eco Warrior Level 3</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Did You Know in Sidebar
    with st.expander("💡 Daily Eco Tip", expanded=True):
        new_fact = random.choice([f for f in ECO_FACTS if f != st.session_state.fact_shown])
        st.session_state.fact_shown = new_fact
        st.info(f"**Did you know?** {new_fact}")
    
    # Quiz Section
    with st.expander("🧠 Sustainability Quiz", expanded=True):
        quiz = st.session_state.current_quiz
        st.markdown(f"**{quiz['question']}**")
        
        selected_option = st.radio(
            "Choose your answer:",
            quiz['options'],
            key=f"quiz_{hash(quiz['question'])}",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Check Answer", use_container_width=True):
                if quiz['options'].index(selected_option) == quiz['correct']:
                    st.session_state.quiz_score += 10
                    st.success(f"Correct! 🎉 +10 points\n\n{quiz['explanation']}")
                else:
                    st.error(f"Incorrect. The right answer is: {quiz['options'][quiz['correct']]}\n\n{quiz['explanation']}")
        
        with col2:
            if st.button("🔄 New Question", use_container_width=True):
                st.session_state.current_quiz = random.choice(QUIZ_QUESTIONS)
                st.rerun()
        
        st.markdown(f"**Your Score:** {st.session_state.quiz_score} points")
    
    st.markdown("---")
    
    # Transaction Input Form
    st.subheader("➕ Add New Transaction")
    with st.form("entry_form", clear_on_submit=True):
        date_input = st.date_input("📅 Date", datetime.date.today())
        item_input = st.text_input("📝 Description", placeholder="e.g., Monthly groceries")
        cat_input = st.selectbox("🏷️ Category", list(EMISSION_FACTORS.keys()))
        amt_input = st.number_input("💰 Amount (₹)", min_value=0.0, value=0.0, step=100.0)
        
        submitted = st.form_submit_button("📥 Add Transaction", type="primary", use_container_width=True)
        if submitted and amt_input > 0:
            if cat_input == "Electricity":
                co2 = round((amt_input / 8.0) * 0.82, 2)
            else:
                co2 = round(amt_input * EMISSION_FACTORS[cat_input], 2)
                
            new_entry = {
                "Date": date_input,
                "Item": item_input,
                "Category": cat_input,
                "Amount": amt_input,
                "CO2": co2
            }
            st.session_state.data.append(new_entry)
            st.success("✅ Transaction recorded successfully!")
            st.balloons()

# --- 7. MAIN DASHBOARD ---
# Header with Gradient
st.markdown(f"""
<div class='gradient-header'>
    <h1 style='margin: 0;'>🍃 EcoTrack Pro Dashboard</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Welcome back, {st.session_state.user_name}! Track your carbon footprint journey.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.data:
    st.info("🌱 Start by adding your first transaction from the sidebar!")
else:
    df = pd.DataFrame(st.session_state.data)
    
    # --- ENHANCED METRICS CARDS ---
    total_co2 = df['CO2'].sum()
    total_spent = df['Amount'].sum()
    avg_daily_co2 = total_co2 / max(len(df['Date'].unique()), 1)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card red'>
            <h4 style='color: #666; margin: 0;'>🌍 Total Emissions</h4>
            <h2 style='color: #d9534f; margin: 10px 0;'>{total_co2:.1f} kg</h2>
            <p style='color: #999; font-size: 0.9rem;'>CO₂ Equivalent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card green'>
            <h4 style='color: #666; margin: 0;'>💰 Total Spend</h4>
            <h2 style='color: #2E8B57; margin: 10px 0;'>₹{total_spent:,.0f}</h2>
            <p style='color: #999; font-size: 0.9rem;'>Indian Rupees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        offset_trees = int(total_co2 / 20)
        offset_cost = offset_trees * 50
        st.markdown(f"""
        <div class='metric-card blue'>
            <h4 style='color: #666; margin: 0;'>🌳 Offset Needed</h4>
            <h2 style='color: #339af0; margin: 10px 0;'>{offset_trees} trees</h2>
            <p style='color: #999; font-size: 0.9rem;'>₹{offset_cost} to plant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h4 style='color: #666; margin: 0;'>📊 Daily Average</h4>
            <h2 style='color: #f76707; margin: 10px 0;'>{avg_daily_co2:.1f} kg/day</h2>
            <p style='color: #999; font-size: 0.9rem;'>Per day emissions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # --- TABS FOR DIFFERENT VIEWS ---
    tab1, tab2, tab3 = st.tabs(["📈 Analytics", "🏆 Achievements", "📋 Transactions"])
    
    with tab1:
        # Charts in Glass Cards
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📅 Monthly Trend")
            
            # Create monthly aggregation
            df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
            monthly_data = df.groupby('Month').agg({'CO2': 'sum', 'Amount': 'sum'}).reset_index()
            monthly_data['Month'] = monthly_data['Month'].astype(str)
            
            fig_line = px.line(monthly_data, x='Month', y='CO2',
                               markers=True, line_shape='spline',
                               color_discrete_sequence=['#2E8B57'])
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title=None,
                yaxis_title='CO₂ (kg)',
                hovermode='x unified'
            )
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📊 Category Distribution")
            
            fig_pie = px.pie(df, values='CO2', names='Category', hole=0.4,
                            color_discrete_sequence=px.colors.sequential.Greens_r)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        # Achievement System
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏆 Your Eco Milestones")
        
        achievements = [
            {"icon": "🌱", "title": "First Step", "desc": "Logged first transaction", "achieved": len(df) >= 1},
            {"icon": "📊", "title": "Analyst", "desc": "Tracked 5+ transactions", "achieved": len(df) >= 5},
            {"icon": "💰", "title": "Smart Spender", "desc": "Saved ₹1000+ on emissions", "achieved": total_co2 > 100},
            {"icon": "🌳", "title": "Tree Champion", "desc": "Offset equivalent of 5 trees", "achieved": total_co2 >= 100},
            {"icon": "📈", "title": "Trend Setter", "desc": "Reduced emissions by 10%", "achieved": False},
        ]
        
        cols = st.columns(3)
        for idx, achievement in enumerate(achievements):
            with cols[idx % 3]:
                status = "✅" if achievement["achieved"] else "⏳"
                color = "#2E8B57" if achievement["achieved"] else "#CCCCCC"
                st.markdown(f"""
                <div style='text-align: center; padding: 15px; border: 2px solid {color}; border-radius: 10px; margin: 10px 0;'>
                    <h2 style='margin: 0;'>{achievement['icon']}</h2>
                    <h4 style='margin: 10px 0;'>{achievement['title']} {status}</h4>
                    <p style='color: #666; font-size: 0.9rem;'>{achievement['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Progress towards goals
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Monthly Goal Progress")
        
        goal = 100  # kg CO2 goal
        progress = min(total_co2 / goal * 100, 100)
        
        st.metric("Target", f"{total_co2:.1f} / {goal} kg")
        st.progress(progress / 100)
        
        if total_co2 > goal:
            st.error(f"⚠️ You're {total_co2 - goal:.1f} kg over your monthly target")
        else:
            st.success(f"✅ {goal - total_co2:.1f} kg remaining to reach your target")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        # Enhanced Transactions Table
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📋 Transaction History")
        
        # Sort and display
        display_df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
        display_df['CO2'] = display_df['CO2'].round(1)
        
        # Add color coding for high emissions
        def color_high_emissions(val):
            if val > 100:
                return 'background-color: #ffcccc'
            elif val > 50:
                return 'background-color: #ffe6cc'
            return ''
        
        styled_df = display_df.style.applymap(color_high_emissions, subset=['CO2'])
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn("Date"),
                "Item": "Description",
                "Category": "Category",
                "Amount": st.column_config.NumberColumn("Amount (₹)", format="₹%d"),
                "CO2": st.column_config.NumberColumn("CO₂ (kg)", format="%.1f kg")
            }
        )
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", len(df))
        with col2:
            st.metric("Highest Emission", f"{df['CO2'].max():.1f} kg")
        with col3:
            st.metric("Average per Transaction", f"{df['CO2'].mean():.1f} kg")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🍃 <strong>EcoTrack Pro</strong> | Making Sustainability Measurable</p>
        <p style='font-size: 0.9rem;'>Every small action counts towards a greener planet</p>
    </div>
    """, unsafe_allow_html=True)