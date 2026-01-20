import streamlit as st
import plotly.express as px
import base64
import pandas as pd

# --- IMPORT LOCAL MODULES ---
from etl_engine import load_and_process_data
from ai_engine import run_intelligence_engine, run_forecast
from genai_tools import generate_pdf_notice, vernacular_chat

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Aadhaar Drishti | Gov-Tech Intel",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. TRANSLATION DICTIONARY (THEME: SANSKRIT-TECH)
# ==========================================
translations = {
    "English": {
        "sidebar_title": "Aadhaar Drishti",
        "nav_live": "Satark Monitor (Live)",
        "nav_plan": "Bhavishya (Predict)",
        "nav_auto": "Karyawahi (Actions)",
        "nav_chat": "Samvad AI (Chat)",
        "main_title": "🇮🇳 Real-time Governance Hub",
        "metric_trans": "Total Transactions",
        "metric_crit": "Active Alerts",
        "metric_mig": "Migration Velocity",
        "metric_mon": "Districts Tracked",
        "chat_welcome": "Aadhaar Samvad Assistant",
        "chat_placeholder": "Ask about anomalies, trends, or policies..."
    },
    "Hindi": {
        "sidebar_title": "आधार दृष्टि",
        "nav_live": "सतर्क मॉनिटर (लाइव)",
        "nav_plan": "भविष्य (अनुमान)",
        "nav_auto": "कार्यवाही (एक्शन)",
        "nav_chat": "संवाद एआई (चैट)",
        "main_title": "🇮🇳 वास्तविक समय निगरानी केंद्र",
        "metric_trans": "कुल लेनदेन",
        "metric_crit": "सक्रिय अलर्ट",
        "metric_mig": "पलायन गति",
        "metric_mon": "ट्रैक किए गए जिले",
        "chat_welcome": "आधार संवाद सहायक",
        "chat_placeholder": "विसंगतियों या रुझानों के बारे में पूछें..."
    },
    "Marathi": {
        "sidebar_title": "आधार दृष्टी",
        "nav_live": "सतर्क मॉनिटर (थेट)",
        "nav_plan": "भविष्य (अंदाज)",
        "nav_auto": "कार्यवाही (कृती)",
        "nav_chat": "संवाद AI (चर्चा)",
        "main_title": "🇮🇳 रिअल-टाइम गव्हर्नन्स हब",
        "metric_trans": "एकूण व्यवहार",
        "metric_crit": "सक्रिय अलर्ट",
        "metric_mig": "स्थलांतर वेग",
        "metric_mon": "ट्रॅक केलेले जिल्हे",
        "chat_welcome": "आधार संवाद सहाय्यक",
        "chat_placeholder": "विसंगती किंवा ट्रेंडबद्दल विचारा..."
    },
    "Tamil": {
        "sidebar_title": "ஆதார் த்ரிஷ்டி",
        "nav_live": "சதர்க் மானிட்டர் (லைவ்)",
        "nav_plan": "பவிஷ்யா (கணிப்பு)",
        "nav_auto": "காரியவாஹி (செயல்)",
        "nav_chat": "சம்வாத் AI (உரையாடல்)",
        "main_title": "🇮🇳 நிகழ்நேர ஆளுமை மையம்",
        "metric_trans": "மொத்த பரிவர்த்தனைகள்",
        "metric_crit": "செயலில் உள்ள எச்சரிக்கைகள்",
        "metric_mig": "இடம்பெயர்வு வேகம்",
        "metric_mon": "கண்காணிக்கப்படும் மாவட்டங்கள்",
        "chat_welcome": "ஆதார் சம்வாத் உதவியாளர்",
        "chat_placeholder": "முரண்பாடுகள் பற்றி கேட்கவும்..."
    }
}

# ==========================================
# 3. MAIN APPLICATION LOGIC
# ==========================================

# --- DATA LOADING ---
try:
    with st.spinner("Initializing Aadhaar Drishti Protocol..."):
        ts_data = load_and_process_data()
    
    if ts_data.empty:
        st.warning("System Offline: No data streams detected in 'data/' folder.")
        st.stop()
        
    profile_data = run_intelligence_engine(ts_data)

except Exception as e:
    st.error(f"System Failure: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    # Language Selector
    language = st.selectbox("Language / भाषा", ["English", "Hindi", "Marathi", "Tamil"])
    t = translations[language]  # Load Dictionary
    
    st.title(t["sidebar_title"])
    st.caption("AI-Powered Governance Suite")
    st.markdown("---")
    
    # Navigation Map (Display Name -> Logic Key)
    nav_map = {
        t["nav_live"]: "Live",
        t["nav_plan"]: "Predict",
        t["nav_auto"]: "Action",
        t["nav_chat"]: "Chat"
    }
    
    nav_selection = st.radio("Module Selection", list(nav_map.keys()))
    nav = nav_map[nav_selection] # Get Internal Key
    
    st.markdown("---")
    st.info(f"System Status: Online ")

# ==========================================
# 4. MODULE VIEWS
# ==========================================

# --- MODULE 1: SATARK MONITOR (Live) ---
if nav == "Live":
    st.title(t["main_title"])
    
    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    vol_million = profile_data['total_vol'].sum() / 1000000
    k1.metric(t["metric_trans"], f"{vol_million:.2f}M")
    k2.metric(t["metric_crit"], len(profile_data[profile_data['status']=='Critical']), delta="High Priority", delta_color="inverse")
    k3.metric(t["metric_mig"], f"{profile_data['migration_score'].mean():.2f}")
    k4.metric(t["metric_mon"], len(profile_data))
    
    # Visuals
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Anomaly Radar (Isolation Forest)")
        fig_scatter = px.scatter(
            profile_data, x='total_vol', y='migration_score', 
            color='status', color_discrete_map={'Critical':'#ef4444', 'Normal':'#3b82f6'},
            hover_name='district', hover_data=['ai_reasoning', 'state'],
            size='total_vol', size_max=40,
            title="Operational Load vs. Migration Intensity"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c2:
        st.subheader("Migration Heatmap")
        top_mig = profile_data.sort_values('migration_score', ascending=False).head(10)
        fig_bar = px.bar(top_mig, x='migration_score', y='district', color='migration_score', 
                        title="Top Influx Districts", color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Critical Feed
    st.subheader(f"{t['metric_crit']} Feed")
    st.dataframe(
        profile_data[profile_data['status']=='Critical'][['district', 'state', 'total_vol', 'migration_score', 'ai_reasoning']],
        use_container_width=True
    )

# --- MODULE 2: BHAVISHYA (Predict) ---
elif nav == "Predict":
    st.title(f"{t['nav_plan']}")
    st.markdown("Powered by **Facebook Prophet** (Time-Series Forecasting)")
    
    sel_dist = st.selectbox("Select District for Projection", ts_data['district'].unique())
    
    if st.button("Initialize Forecast Model"):
        with st.spinner(f"Simulating future trends for {sel_dist}..."):
            forecast = run_forecast(ts_data, sel_dist)
            
            if forecast is not None:
                curr_avg = ts_data[ts_data['district']==sel_dist]['total_vol'].mean()
                pred_avg = forecast.tail(30)['yhat'].mean()
                growth = ((pred_avg - curr_avg)/curr_avg)*100
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Current Daily Load", f"{curr_avg:.0f}")
                m2.metric("Projected Load (30 Days)", f"{pred_avg:.0f}")
                m3.metric("Growth Velocity", f"{growth:.1f}%", delta_color="inverse" if growth > 15 else "normal")
                
                fig = px.line(forecast, x='ds', y='yhat', title=f"Demand Projection: {sel_dist}")
                fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', line=dict(width=0), showlegend=False)
                fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                if growth > 20:
                    st.error(f"STRATEGIC ALERT: {sel_dist} requires immediate resource augmentation.")
            else:
                st.warning("Insufficient data points for reliable projection.")

# --- MODULE 3: KARYAWAHI (Action) ---
elif nav == "Action":
    st.title(f"{t['nav_auto']}")
    st.markdown("Automated **Legal Notice Generation** for flagged anomalies.")
    
    anomalies = profile_data[profile_data['status']=='Critical']
    
    if anomalies.empty:
        st.success("No critical anomalies requiring action.")
    else:
        # Show ALL anomalies, not just head(5)
        for i, row in anomalies.iterrows():
            with st.expander(f"{row['district']} | {row['ai_reasoning']}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**State:** {row['state']}")
                    st.write(f"**Transaction Volume:** {row['total_vol']:,.0f}")
                    st.write(f"**Migration Index:** {row['migration_score']:.3f}")
                with c2:
                    if st.button("Draft Notice", key=f"btn_{i}"):
                        pdf_bytes = generate_pdf_notice(
                            row['district'], 
                            row['ai_reasoning'], 
                            f"Vol: {row['total_vol']}", 
                            language
                        )
                        b64 = base64.b64encode(pdf_bytes).decode()
                        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Notice_{row["district"]}.pdf"> Download PDF</a>'
                        st.markdown(href, unsafe_allow_html=True)

# --- MODULE 4: SAMVAD AI (Chat) ---
elif nav == "Chat":
    st.title(t["chat_welcome"])
    st.markdown("Ask complex policy queries in your local language.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(t["chat_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # RAG Context Retrieval
        context = profile_data.sort_values('migration_score', ascending=False).head(5).to_markdown()
        
        with st.spinner("Processing Logic..."):
            response = vernacular_chat(prompt, context, language)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)