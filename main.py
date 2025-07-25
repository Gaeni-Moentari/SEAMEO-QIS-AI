from AI_Component.Crew import *
from AI_Component.validator.validator import *
from AI_Component.qis_agent_chain import is_seaqis_question, QisAgentChain
import Component.Logo as Img
import streamlit as st
import time

# Set page config (must be at the top)
Img.set_page_config(
    page_title="SEAMEO QIS - SciMentor",
    page_icon="./Image/seaqis.png",
    layout="wide"
)

Img.image(["./Image/gema.png", "./Image/seameo.png", "./Image/seaqis.png"])
st.title("SEAMEO QIS")
st.write("SciMentor is your friend when you're curious about science experiments, STEM concepts, or fun ways to teach science. Like a science teacher who never gets tired of explaining, but digital version and can be talked to anytime.")
st.write("Koordinator Gatot HP - www.gaeni.org ")
input = st.text_input("Enter your question")
lang = "english"
submit = st.button("Start Search")

if submit:
    # Enhanced question validation with SEAQIS context detection
    is_science_related = qis_validator(input)
    is_seaqis_related = is_seaqis_question(input)
    
    if is_science_related or is_seaqis_related:
        # If valid, proceed to main process
        with st.spinner('🤖 SciMentor is thinking... Please wait'):
            # Show progress bar with realistic timing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate processing steps
            status_text.text('🔍 Analyzing your question...')
            progress_bar.progress(25)
            time.sleep(0.5)
            
            status_text.text('🧠 Processing science knowledge...')
            progress_bar.progress(50)
            time.sleep(0.5)
            
            status_text.text('📚 Generating response...')
            progress_bar.progress(75)
            
            # Use the appropriate agent chain based on context
            if is_seaqis_related:
                # Use the specialized SEAQIS agent chain
                result = QisAgentChain(input, lang).process_question()
            else:
                # Use the general science education agent chain
                result = QisCrew(input, lang).generalCrew().kickoff()
            
            status_text.text('✅ Complete!')
            progress_bar.progress(100)
            time.sleep(0.3)
            
            # Clean up progress indicators
            progress_bar.empty()
            status_text.empty()
        st.markdown(result)
    else:
        # If not valid, show error message
        st.error("Your question is not related to science education or SEAMEO QIS topics. Please ask a relevant question.")
