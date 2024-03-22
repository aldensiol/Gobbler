from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
from ctransformers import AutoModelForCausalLM
from MapGenerator import plotAllHTML

data_extractor = "./DataExtractorLLM"

finetuned_model = T5ForConditionalGeneration.from_pretrained(data_extractor)
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")

# List of field identifiers to split the text correctly
fields = ["Location of the incident:", "Prominent landmarks:", "Expressway:", "Nearby lamp post numbers:", "Casualties:", "Nature of traffic accident:", "Hazards or obstructions:", "Vehicles involved:", "Actions taken by bystanders:", "State of casualties involved in the accident:"]

# Function to split and format the initial string
def parse_report(report, fields):
    for field in fields:
        report = report.replace(field, "\n" + field)
    # Remove the first newline character added before the first field
    report = report.lstrip('\n')
    return report

def prompt_llm(modified_string, llm):
    format_prompt = f"<s>[INST] {recommend_prompt.format(modified_string)} [/INST]"

    print("************************************************")
    print(llm(format_prompt))
    print("************************************************")
    print("\nGenerating shortest path from nearest hospital, police station and fire station to incident site...\n")
    plotAllHTML(location_value(parsed_report_correct))

def location_value(parsed_report_correct):
    return parsed_report_correct.split('\n')[0].split(':')[1]


recommend_prompt = """
As an AI Emergency Response Dispatcher in Singapore, your task is to assess and coordinate emergency services for the following incident:

incident report: {}

Recommend the appropriate response for:

Police Deployment: Specify the minimum number of police units required.
Ambulance Services: Identify the number of ambulances needed based on potential injuries.
Firefighter Engagement: Assess the necessity for firefighter presence.
Provide concise instructions prioritizing public safety, emergency care, and traffic management."
"""
while True:
    user_prompt = input("\n\nPlease describe the traffic accident or type 'exit' to quit the application:\n\n")

    if user_prompt == "exit":
        exit()

    inputs = tokenizer(user_prompt, return_tensors="pt")
    outputs = finetuned_model.generate(**inputs, max_length=200, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)


    # Parsing the initial string to correctly format it
    parsed_report_correct = parse_report(answer, fields)
    
    print("\n\n")
    print(parsed_report_correct)

    print("\nGenerating suggested responses for the situation...\n")

    modified_string = parsed_report_correct.replace('\n', ' ')

    # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
    llm = AutoModelForCausalLM.from_pretrained("./mistral-7b-instruct-v0.2.Q4_K_M.gguf",
                                            context_length = 1000,
                                            max_new_tokens = 350)

    prompt_llm(modified_string, llm)
