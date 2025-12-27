import json
import requests
from logger import setup_logger
from db import get_connection

OLLAMA_URL = "http://localhost:11434/api/generate"

# Used phi3:mini as it is an efficient model
# It is instruction based and can run in CPU-only hardware.
# To know more about model visit https://ollama.com/library/phi3:mini
MODEL = "phi3:mini" 
MODEL_VERSION = "4k-instruct-q4" # 4-bit quantized version.
TEMPERATURE = 0.1 # I have set this to lower value to get more deterministic output.
TOP_P = 0.9 # Balancing so that there will be less hallucination.
NUM_PREDICT = 80 # Maximum tokens the model is allowed to generate. Should be enough for even complex bash commands.


# Will enhance the prompt template in future 
# based on user feedback.
SYSTEM_PROMPT = """
You are a Linux command translator.

STRICT RULES (must follow):
- Output ONLY ONE valid bash command.
- Do NOT include explanations.
- Do NOT include markdown, backticks, or code fences.
- Do NOT add comments.
- Do NOT add extra text before or after the command.
- If unsure, output the closest safe command.

Breaking any rule is a FAILURE. UTTER FAILURE!!!
"""

def save_interaction(
    input_text: str,
    model_output: str,
    model_name: str = MODEL,
    model_version: str = MODEL_VERSION,
    metadata: dict | None = None,
):

    """
        Whenever user inputs an instruction, 
        this funcion will save the input and generated output command to DB.
        This can be used for future fine-tuning of model.
    """
    logger = setup_logger("save_interaction")
    logger.debug("Opening DB connection.")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            logger.debug("Saving interaction to DB.")
            cur.execute(
                """
                INSERT INTO command_feedback (
                    input_text,
                    model_output,
                    model_name,
                    model_version,
                    metadata
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    input_text,
                    model_output,
                    model_name,
                    model_version,
                    json.dumps(metadata) if metadata else None,
                ),
            )
        conn.commit()
    finally:
        conn.close()
        logger.debug("DB connection closed.")

def translate_to_shell(plain_english: str) -> str:
    """ 
    This function takes a plain English instruction
    Calls Ollama API to generate a bash command
    Saves the interaction to the DB
    Returns the bash command.
    """
    logger = setup_logger("translate_to_shell")
    logger.info("Received instruction: %s", plain_english)

    prompt = f"{SYSTEM_PROMPT}\n\nTask: {plain_english}\nCommand:"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P, 
            "num_predict": NUM_PREDICT 
        }
    }

    logger.debug("Sending request to Ollama API.")
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    result = response.json()["response"].strip()
    logger.info("Command generated: %s", result)

    # Saving the interaction to the DB.
    save_interaction(
        input_text=plain_english,
        model_output=result,
        metadata={
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": NUM_PREDICT
        }
    )
    
    return result

if __name__ == "__main__":
    logger = setup_logger("main")
    while True:
        user_input = input("\n Describe task (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        logger.info(translate_to_shell(user_input))
