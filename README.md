# 🌌 nebula-prime-adk

> **MultiAgentic AI for Clinical Disease Assessment**  
> _Reduce clinician burnout with scalable, trustworthy AI agents._

---

## 🚀 Overview

**nebula-prime-adk** is a demonstration of using Agent Developmment Toolkit (ADK) to bulid and run MultiAgentic AI to solve clinical problem at scale.
Clinicians face cognitive overload reviewing decades of patient data. and come up with optimal care plans.
MultiAgentic AI can help by breaking down problems into manageable tasks for specialist agents.

---

## 🩺 Use Case

- Clinicians select a patient and clinical context (currently: **oncology** or **nephrology**).
- The system analyzes patient data and assesses for complex diseases.
- Results include:
  - Disease assessment
  - Confidence, relevance, and completeness scores
  - Key data summaries for transparency

> **Impact:**  
> ⏱️ Reduce clinician prep time from _X minutes_ to _less than 1 minute_.
> 😥 Reduce cognitive stress of the clinician.

---

## 🏭 Implementation details

<details>
<summary>Example setup</summary>

In this example setup, we have a clinical app that fetches a selected patient's clinical and health imaging data.
Ideally, the clinical data would come from HL7 or FHIR servers like Epic or Cerner.
Similarly, the imaging data would come from a PACS archive.
In this example, however, the frontend fetches these data from our custom source that is not shown.
The app then send radiology report and clinical data to our backend system running on GCP.
The first API layer handles identity and authorization and traffic shaping mechanisms. It then orchestrates multiple calls with the Agentic AI running on Google Agent Engine.

These Agents work at 3 layers. At the top layer, a coordinating agent (Nebula Prime coodinator) receives uses GCP Checks API to filter out offending requests that include dangerous, sexually explicit, or obscene coontent.
It then uses a prompt that helps it to decide whether the request is in the context of oncology or nephrology and forwards the request to an oncology coordinator agent or a nephrology coordinator agents.
These agents runs a preconfigured set of specialist agents in parallel.
The oncology coordinator runs agents to detect breast cancer, colon cancer, and brain cancer.
The nephrology coordinator runs agents to detect kidney stone, kidney failure, and renal cell carcinoma, the most common type of kidney cancer.

Each of these agents use their prompts in conjunction of the patient's data to determin the presence of the target disease, confidence score, relevance and confidence scores of the data etc. and returns it to their coordinator.
The coordinator then returns to main coordinator who returns the complete response with context to the API.
This response data then goes via GCP Checks API before the frontend app can show this data on the app.

Each agent uses one of the industry standard large language model and Google search as a tool.
We used Gemini flash 2.0 and OpenAI GPT4o. The agents use the GenAI models to process the clinical data with the
help of the thought process baked in their prompts.
If the agents need to understand anything about the disease or the clinical data, they can use the Google search
tool to find more details from most relevant documents on the Internet.

Note that:

1. This project does not offer a clinical solution. This is merely a demo project using AgenticAI
2. This package contains code using ADK for AgentEngine part only. The frontend code is not included
3. This code does not come with any guarantee of correctness, use it at your own discretion
4. The agent prompts are written using a multitude of GenAI models including gpt4o and gemini flash. Do not use these in a live system without proper analysis
5. There are multiple layers of guard rails. The one using GCP checks API in diagram is currently in private beta. Its code is written in guardrails.py but is disabled in the agent config by default. Use it at your own discretion

</details>

## 🧠 MultiAgentic AI Architecture

<details>
<summary>🖼️ <b>Click to expand: Agent Hierarchy Diagram</b></summary>

![MultiAgentic AI Diagram](nebula_prime.png)

The diagram outlines below agents:

1. Nephrology
    1. Nephrology coordinator agent
    1. Nephrolithiasis agent
    1. Renal failure agent
    1. renal cell carcinoma
1. Oncology
    1. Oncology coordinator agent
    1. Breast cancer agent
    1. Colon cancer agent
    1. Brain cancer agent

</details>

| Layer         | Agents                                                                 |
|---------------|-----------------------------------------------------------------------|
| **Top**       | Nebula Prime Coordinator                                              |
| **Nephrology**| Nephrology Coordinator → Nephrolithiasis, Renal Failure, RCC          |
| **Oncology**  | Oncology Coordinator → Breast Cancer, Colon Cancer, Brain Cancer       |

---


## ⚙️ Features

- 🤖 **Specialist Agents** for nephrology & oncology
- 🧩 **Parallel & Coordinating Agents** for modularity
- 🔒 **Guardrails** (GCP Checks API, prompt-level)
- 🌐 **Google Search Tool** for real-time medical knowledge
- 📊 **Transparent Outputs**: JSON with confidence & data quality

---

## 📦 Installation

> **Requirements:**  
> - Python 3.12  
> - Poetry `pip install poetry`
> - Google Cloud Project & CLI

```sh
git clone https://github.com/atiur/nebula-prime-adk
cd nebula-prime-adk
poetry install
```

---


## 🛠️ Configuration

<details>
<summary>🔑 <b>Environment Variables (.env)</b></summary>

```env
DEFAULT_MODEL="gemini-2.5-pro-preview-06-05"
GOOGLE_API_KEY="<GOOGLE_API_KEY>"
OPENAI_API_KEY="<OPENAI_API_KEY>"
USE_CHECKS=False
SECRET_FILE_PATH='path/to/your/secret.json'
```
</details>

<details>
<summary>☁️ <b>Google Cloud Setup</b></summary>

```sh
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=<your-project-id>
export GOOGLE_CLOUD_LOCATION=<your-cloud-location>
export GOOGLE_CLOUD_STORAGE_BUCKET=<your-storage-bucket>

gcloud auth application-default login
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```
</details>

---


## 🧪 Running Locally

<details>
<summary>▶️ <b>Start API Server</b></summary>

Add configuration to .env file.

```bash
DEFAULT_MODEL="gemini-2.0-flash"
GOOGLE_API_KEY="Use your GCP API key"
OPENAI_API_KEY="Use your OpenAI API key"
```

```sh
# Make sure to install dependencies.
poetry install
# Run as API server.
adk api_server
```
</details>

<details>
<summary>💬 <b>Example: Create Session & Query</b></summary>

```sh
curl -X POST http://localhost:8000/apps/nebula_prime_adk/users/u_1/sessions/s_1 \
  -H "Content-Type: application/json" \
  -d '{
    "clinical_context": "nephrology",
    "clinical_reports": "Patient Name: John Doe ... (your report here)"
  }' | jq .
```

```sh
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
    "app_name": "nebula_prime_adk",
    "user_id": "u_1",
    "session_id": "s_1",
    "new_message": {
        "role": "user",
        "parts": [
            { "text": "What is the diagnosis for this patient?" }
        ]
    },
    "streaming": false
}' | jq .
```
</details>

---

## ☁️ Deploying to AgentEngine

<details>
<summary>🛫 <b>Deploy, List, Update, Delete Agents</b></summary>

```sh
# Install glcoud CLI tool.
# Initialize gcloud config.
gcloud init
# Login using gcloud.
gcloud auth login
# Deploy to AgentEngine.
python deployment/deploy.py --create
# List agents to see if deploy.py is configured correctly.
python deployment/deploy.py --list
# Update agents. Note that GCP API and SDK version is broken on one requiring gcs_uri and another not. So, update code needs a fix when GCP fixes their SDK.
python deployment/deploy.py --update --resource_id <RESOURCE_ID>
# Delete, if desired.
python deployment/deploy.py --delete --resource_id <RESOURCE_ID>
```
</details>

---

## 📝 API Example

<details>
<summary>🌐 <b>Sample API Request</b></summary>

Create session with state.
```sh
# Create session with state.
curl -XPOST <Your API endpoint> -H "Content-Type: application/json" -d '{
    "user_id": "u_1",
    "state": {
        "clinical_context": "nephrology",
        "clinical_reports": "Patient Name: John Doe ... (your report here)"
    }
}'
```

Delete session.
```sh
# Delete session.
curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904:query -d '{"class_method": "delete_session", "input": {"user_id": "_u1", "session_id": "7952473484343377920"}}'
```

List sessions. While this is documented [here](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-sessions-api), this api always returns error.

```sh
curl -X GET \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904/sessions"
```

Query Agentic system.

```sh
curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904:streamQuery?alt=sse -d '{
  "class_method": "stream_query",
  "input": {
    "user_id": "u_1",
    "session_id": "7952473484343377920",
    "message": "What is the diagnosis for this patient?",
  }
}'
```
</details>

---
## ⚠️ Disclaimer

> **Warning**  
> - This is a demo project, **not for clinical use**.
> - No guarantee of correctness; use at your own risk.
> - Prompts and outputs are for demonstration only.
> - GCP Checks API is in private beta; use with caution.

---

## 📄 License

```
Copyright CloudSoftonic Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE file for details.
```
