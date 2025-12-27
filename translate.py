import json
import requests
from logger import setup_logger
from db import get_connection

# Loading the configs
from configs.model_registry import EXPERIMENTS
from configs.prompts import PROMPTS

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_ID = "phi3-mini:exp"

def build_payload(model_id: str, user_input: str) -> dict:
    params = EXPERIMENTS[model_id]
    prompt = PROMPTS[params.prompt_template].replace(
        "{{input}}", user_input
    )

    return {
        "model": params.model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": params.temperature,
            "top_p": params.top_p,
            "num_predict": params.num_predict,
        }
    }


def save_interaction(input_text: str, model_output: str, model_id: str):
    """
        Whenever user inputs an instruction, 
        this funcion will save the input and generated output command to DB.
        This can be used for future fine-tuning of model.
    """
    logger = setup_logger("save_interaction")
    
    # Fetching params from model registry based on model_id
    params = EXPERIMENTS[model_id]
    model_name = params.model_name
    model_version = params.model_version
    metadata = {
        "temperature": params.temperature,
        "top_p": params.top_p,
        "num_predict": params.num_predict,
    }

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

    payload = build_payload(
        model_id=MODEL_ID,
        user_input=plain_english
    )

    logger.debug("Sending request to Ollama API.")
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    result = response.json()["response"].strip()
    logger.info("Command generated: %s", result)

    # Saving the interaction to the DB.
    save_interaction(
        input_text=plain_english,
        model_output=result,
        model_id=MODEL_ID
    )
    
    return result

if __name__ == "__main__":
    logger = setup_logger("main")
    while True:
        user_input = input("\n Describe task (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        logger.info(translate_to_shell(user_input))
