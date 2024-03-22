# NCS-Team Gobblers

# As part of NUS-NCS Innovation Hackathon, 2024

# Contributors

Anastasia Goh, Alden Sio, Lo Jingjie (Dylan), Li Shuyao, Xu Ziqi, Zhu Yi Cheng

# Introduction to Noah
<p align = "center">
<img width="476" alt="Screenshot 2024-03-21 at 22 51 48" src="https://github.com/aldensiol/NCS-Winner-Club/assets/124263084/febe9359-d0c6-4ae0-91ed-0e3ac94514ff">
</p>
Noah is an AI-powered call-operator assistant designed to monitor and analyze conversations between call operators and callers. It specializes in extracting crucial accident information such as location, casualties, and accident details from these calls. Noah organizes this information into a structured format for call operators, highlighting any missing details and prompting relevant questions. 
<br></br>
Additionally, Noah utilizes natural language processing (NLP) and machine learning to assess accident severity and provide recommendations for incident response, facilitating quicker and more informed emergency responses. Furthermore, Noah can extract location data from calls to provide information about the nearest hospitals and police stations, including estimated travel times, enabling swift and appropriate action during emergencies.




## How to Use Noah?

For **Windows Users** only:
Simply click on this <a href="https://huggingface.co/Zqbot1/Noah">link</a>
 to download Noah from HuggingFace! Here are the steps to use Noah after you have successfully installed it:

1. Unzip Noah.zip.
2. Run the final.exe. (If there are any warnings, select "Run anyway".)
3. Enter your prompt.
4. Once you are done, type "exit" to quit the application.

An example of a prompt is: 
A severe explosion has occurred at the junction of Kent Ridge Road, near National University of Singapore. A gas tanker, after colliding with a sedan, has exploded, resulting in a massive fireball and subsequent fires spreading to nearby buildings and vehicles. There are five people seriously injured and lying on the ground.

## How to download and use the Model **locally**/as a **Mac** User

Leveraging the fine-tuned model for your applications is straightforward. Follow the steps below to integrate and utilize the model effectively:

### Step 1: Cloning Code from Git, and Installing Dependencies
Ensure you have Python and the necessary libraries installed. You will need all the libraries within the requirements.txt file, which can be installed via pip:

```bash
git clone https://github.com/aldensiol/Gobbler.git

## cd into the folder

pip install requirements.txt
```

### Step 1.5: Installing Fine-Tuned model
Ensure you download the Checkpoint (updated model) into the directory you want to code. You can find this checkpoint <a href="https://drive.google.com/drive/folders/13JDms4Q_2WaaCqvk36ySFbu7KssH3F4X?usp=drive_link">here.</a>

### Step 2: Loading the Model
By editing the final.py script, you can load the fine-tuned model directly using the Transformers library. Replace `your_model_path` with the actual path where the checkpoint:

```python
last_checkpoint = "your_last_checkpoint_path" # Replace this with the path to the fine-tuned model
finetuned_model = T5ForConditionalGeneration.from_pretrained(last_checkpoint)
tokenizer = T5Tokenizer.from_pretrained(last_checkpoint)
```

### Step 3: Running Noah.py
Run the script, using
```bash
python Noah.py
```

When prompted via "Please describe the traffic accident:", input your incident report. For an example, you can use this: A severe explosion has occurred at the junction of Kent Ridge Road, near National University of Singapore. A gas tanker, after colliding with a sedan, has exploded, resulting in a massive fireball and subsequent fires spreading to nearby buildings and vehicles. There are five people seriously injured and lying on the ground.

### Step 4: Interpreting the Results
The output will be your model's interpretation or response based on its fine-tuning. Analyze the results as needed for your application.

# Fine-Tuning Guide for Emergency Incident Extracting Model (how we trained our model)

This is our guide on how we fine-tuned the "google/flan-t5-base" model for emergency incident reporting. Below is a generic sequence of events that outlines our fine-tuning process:

## 1. Installation and Importing Libraries
Firstly, we begin by installing and importing necessary libraries and models. For this project, we utilized "google/flan-t5-base" from HuggingFace.

## 2. Instantiating the Model
We then instantiate the base Google FLAN model for further processing.

## 3. Dataset Loading and Preprocessing
The dataset is loaded and preprocessed through tokenization. We specifically allow contextual words like "no", "don't", etc., to handle prompts such as "no one is injured" or "don't need to send ambulance".

## 4. Tokenization into Dictionary Format
Our dataset is further tokenized into a dictionary format, which is a requirement for this model. For our case, keys such as 'input_ids', 'attention_mask', 'labels' are essential for training.

## 5. System Prompt and Labeling
We add a system prompt, "extract structured details:", and attach labels to the respective columns. This data is then split into training and testing samples.

## 6. Converting Texts into Embeddings
Text data is converted into embeddings to be processed by the model.

## 7. Global Training Parameters
Next, we decide on global parameters for training, which mostly depend on computational power. Here are some key parameters:

- **L_RATE (Learning Rate):** Determines the adjustment rate of network weights with respect to the loss gradient. A smaller value indicates slower adjustments.
- **BATCH_SIZE:** Specifies the number of samples processed before updating the model's internal parameters.
- **PER_DEVICE_EVAL_BATCH:** Defines the number of samples processed at once during model evaluation. Usually equal to BATCH_SIZE.
- **WEIGHT_DECAY:** A regularization technique to prevent overfitting by penalizing larger weights.
- **SAVE_TOTAL_LIMIT:** Specifies the maximum number of model checkpoints to save.
- **NUM_EPOCHS:** The number of times the entire dataset passes through the model.

## 8. Training
With the parameters set, we proceed to train the model using `.train()` method.

## 9. Model Checkpointing
After training, we obtain the desired checkpoint (the one with the least loss) and store it. This model can then be loaded using:

```python
last_checkpoint = "./results/checkpoint-500"
finetuned_model = T5ForConditionalGeneration.from_pretrained(last_checkpoint)
tokenizer = T5Tokenizer.from_pretrained(last_checkpoint)
```

## 10. Testing the Model
Finally, we test the fine-tuned model with prompts to evaluate its performance. For example:

```python
incident_report = "Hello police, there is an accident near me at Information Technology NUS, Street 2. A bus collided with a Taxi, 3 people are severely injured, there is a fire. Students are calling for help, Lamp post nearby: 88"

inputs = tokenizer(incident_report, return_tensors="pt")
outputs = finetuned_model.generate(**inputs, max_length=200, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
```
Once we have obtained our extracted entities, we use these to prompt for specific instructions to be distributed to relevant authorities -- helping in effectively managing this given incident.

# Guide to Generating Recommendations from Mistral-7B-Instruct-v0.2-GGUF
For the generation of recommendations and instructions to call operators, we made use of the open sourced model Mistral-7B-Instruct-v0.2-GGUF, which is a open source LLM Model trained to respond to Instructions (hence the Instruct in its name).

## 1. Downloading of Mistral-7B-Instruct-v0.2-GGUF
We first download the entire model from Hugging Face. https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

## 2. Initialising of Model
Ensuring that the downloaded GGUF model is in the same directory as the script.py file, we initialise the model using a external library - ctransformers.

```python
from ctransformers import AutoModelForCausalLM

# Initialise LLM Model
llm = AutoModelForCausalLM.from_pretrained("mistral-7b-instruct-v0.2.Q4_K_M.gguf", max_new_tokens = 350)
```

A detailed list of parameters can be found here: https://github.com/marella/ctransformers

## 3. Generating responses from prompts
We first construct our prompt and ensure that it is in a particular format. After that, we call the prompt as a input to the LLM. And, wow, you will see your responses according to the prompt!

```python
example_prompt = """
As an emergency dispatcher, you are tasked with classifying traffic incident reports into four severity levels to ensure appropriate emergency responses are dispatched. 

Incident report: {}

Here's the classification criteria:

Life-Threatening Emergencies: Includes situations like cardiac arrest, unconsciousness, severe breathing difficulties, active seizures, major trauma, and stroke.
Emergencies: Encompasses conditions such as head injuries, labor, bone fractures, and asthma attacks.
Minor Emergencies: Covers incidents like cuts with bleeding, accidents resulting in bruising or swelling, and mild injuries.
Non-Emergencies: Includes minor issues such as constipation and mild rashes.

Given the details of a traffic incident report, determine its classification based on the above criteria.
"""

formatted_prompt = f"<s>[INST] {your_prompt} [/INST]"

# Call LLM with prompt
print(llm(format_prompt))
```
