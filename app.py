import streamlit as st
import requests
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="Oxalis AI", page_icon="☘️", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0078d4;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .status-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. Header & Introduction ---
st.title("☘️ Oxalis AI")
st.subheader(" Multi-Agent Strategy Swarm")
st.info("Input your goal and let the Planner, Retriever, and Executor orchestrate your success.")

# --- 3. Input Section ---
with st.container():
    col_a, col_b = st.columns([2, 1])
    with col_a:
        topic = st.text_input("Project Topic / Goal", placeholder="e.g., Designing a portable water filtration system")
    with col_b:
        timeframe = st.selectbox("Timeframe", ["Short Analysis", "1 Week Phase", "1 Month Phase", "1 Year Phase", "Longer than a year"])

    context = st.text_area("Constraints or Context", placeholder="Identify specific hardware, budget limits, or technical preferences here...")

    generate_btn = st.button(" Run Oxalis ai", use_container_width=True)

# --- 4. Logic Execution ---
if generate_btn:
    if not topic:
        st.error("Please enter a topic to begin.")
    else:
        payload = {
            "project_topic": topic,
            "timeframe": timeframe,
            "additional_context": context
        }

        with st.spinner("Wait while the agents collaborate... check the Uvicorn terminal for live progress."):
            try:
                # Call the backend
                response = requests.post("http://127.0.0.1:8000/plan", json=payload, timeout=180)
                
                if response.status_code == 200:
                    response_json = response.json()
                    st.session_state['output'] = response_json.get("data", "No blueprint was generated.")
                    
                    # Store logs if available
                    if os.path.exists("swarm.log"):
                        with open("swarm.log", "r", encoding="utf-8") as f:
                            st.session_state['logs'] = f.read()
                else:
                    st.error(f"Backend Offline or Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: Ensure your FastAPI server is running in the other terminal. {e}")

# --- 5. Output Display ---
if 'output' in st.session_state:
    st.markdown("---")
    
    # Check if the output is empty or an error string
    output_text = st.session_state['output']
    
    if output_text and len(output_text) > 50:
        st.success(" Execution Strategy Generated Successfully!")
        
        st.markdown(output_text, unsafe_allow_html=True)
        
        st.divider()
        st.download_button(
            label="💾 Download Blueprint (.md)", 
            data=output_text, 
            file_name="oxalis_plan.md",
            mime="text/markdown"
        )
    else:
        st.warning("The swarm is still processing or returned an incomplete response. Check the terminal for details.")

    # Keep Technical Logs in a separate area
    if 'logs' in st.session_state:
        with st.expander(" View Technical Reasoning (Agent Logs)"):
            st.code(st.session_state['logs'], language="text")

# --- 6. Footer ---
st.markdown("---")
footer_html = """
<div style="text-align: center; color: #808495; padding: 10px;">
    <p style="margin-bottom: 5px;"><strong>Oxalis AI</strong> | Agentic Intelligence</p>
    <p style="font-size: 0.85rem;">Built with ❤️ by <b>Team 2Bytes</b> | AI Unlocked 2026</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)