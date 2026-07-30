import json
from models.process_explanation import ProcessExplanation
from ai.prompt_builder import build_process_prompt

def generate_process_explanations(interface, llm):

    prompt = build_process_prompt(interface)

    print("\nCalling Gemini for Process Steps...\n")

    response = llm.generate(prompt)

    print("\nGemini Response:\n")
    print(response)  
    
    if not response.strip():
        print("No response received from Gemini.")
        return []
    
    try:
        steps = json.loads(response)
    except json.JSONDecodeError:
        print("Gemini returned invalid or empty JSON.")
        return []
    
    steps = json.loads(response)
     
    process_steps = []

    for step in steps:
        process_steps.append(
            ProcessExplanation(
                step_number=step["step"],
                component_type=step["component_type"],
                component_name=step["component_name"],
                title=step["title"],
                description=step["description"],
                icon=step["icon"]
            )
        ) 
    
    return process_steps