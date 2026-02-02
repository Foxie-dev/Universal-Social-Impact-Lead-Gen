import streamlit as st
from crew import run_swedish_scout # Make sure this matches your function name in crew.py

st.set_page_config(page_title="BLING Sponsor Scout", layout="wide", page_icon="🇸🇪")

st.title("🇸🇪 Sponsorship Scout & Audit Engine")
st.info("Automating due diligence and strategic outreach for the Swedish impact ecosystem.")
st.info("🔍 AI is performing a deep-search on Allabolag. This usually takes 60-90 seconds to ensure accuracy.")


# 1. SIDEBAR FOR INPUTS
with st.sidebar:
    st.header("Search Parameters")
    niche_input = st.text_input("Industry Niche", value="Tjänsteföretag")
    city_input = st.text_input("Swedish City", value="Stockholm")
    run_button = st.button("🚀 Start AI Research")
    
st.divider()
st.markdown("Developed by **[Tina, Ai Strategy Lead]**") # Aligned correctly!
# 2. THE EXECUTION
if run_button:
    with st.status("🤖 Agents are working...", expanded=True) as status:
        st.write("🕵️‍♂️ Scout: Finding relevant organizations...")
        st.write("📊 Analyst: Verifying financials on Allabolag...")
        
        # This calls your logic from crew.py
        result = run_swedish_scout(niche_input, city_input) 
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # 3. DISPLAY RESULTS
    st.subheader("Final M&A / Sponsorship Report")
    st.markdown(result)