import streamlit as st
from translate import translate_to_shell
import time

# Set page configuration
st.set_page_config(
    page_title="Linux Command Generator",
    page_icon="🐧",
    layout="centered"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stCode {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Linux Command Generator")
    st.markdown("Translate plain English instructions into Linux commands instantly.")

    # Input section
    user_instruction = st.text_input("Enter your instruction:", placeholder="e.g., list all files sorted by size")

    if st.button("Generate Command"):
        if user_instruction:
            try:
                # Show loading spinner while generating
                with st.spinner('Generating command...'):
                    # Call the Ollama SLM API to generate the command
                    command = translate_to_shell(user_instruction)
                    
                # Display result
                st.success("Command Generated!")
                st.code(command, language='bash')
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure Ollama is running safely locally!")
        else:
            st.warning("Please enter an instruction first.")

if __name__ == "__main__":
    main()
