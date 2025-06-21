# nebula-prime-adk


## The problem
This project is a demonstration of using Agent Developmment Toolkit (ADK) to bulid and run MultiAgentic AI to solve clinical problem at scale.
Today's clinicians are over burdened with cognitive load as they have to go through decades worth of patient data for every patient and come up with optimal care plans.
MultiAgentic AI can help reduce this burden by having high level agents break down the problem that low level agents can solve accurately.

## User experience
In this example scenario, clinicians open a patient in the app with a clinical conext.
We have implemented only oncology and nephrology as example contexts but this AgentciAI system can be extended to any number of clinical specialties.
The app then uses the Agentic system to automatically go through patient's health data and assess aganist a set of complex diseases.
To establish trust, the Agentic system produces a disease assessment and, along with it, provides the confidence of the decision, the relevance and completeness of the data avaialable to it.
It additionally produces a gist of key data that reflects why the Agents came to this conclusion.
The clinician can take a glance at this app and see critical comorbidities.
They can decide whether the agent Analysis is correct or needs correction based on the gist summary and decide which disease area to probe further.


## Target impact
The eventual impact of the system is to reduce cognitive stress of the clinician.
Clinicians spend X min to go through all relevant health data before a patient consulation.
The Agentic system can reduce this prep time to less than one min by offering this pre-assessment.

## Implementation details

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

## MultiAgentic AI
The interaction among above components are shown in the below diagram.

![](nebula_prime.png)

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


## Setup and Installation

1.  **Prerequisites**
    *   Python 3.12
    *   Poetry  ```pip install poetry```

    * A project on Google Cloud Platform
    * Google Cloud CLI

2.  **Installation**

```bash
# Clone this repository.
git clone https://github.com/atiur/nebula-prime-adk
# Install the package and dependencies.
poetry install
```

3.  **Configuration**
Set up Google Cloud credentials.

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=<your-project-id>
export GOOGLE_CLOUD_LOCATION=<your-cloud-location>
export GOOGLE_CLOUD_STORAGE_BUCKET=<your-storage-bucket>
```

Authenticate your GCloud account.

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```

## Running the Agent Locally

Add configuration to .env file.

```bash
DEFAULT_MODEL="gemini-2.0-flash"
GOOGLE_API_KEY="Use your GCP API key"
OPENAI_API_KEY="Use your OpenAI API key"
```

Make sure to install dependencies.

```bash
poetry install
```

Run as API server.

```
adk api_server
```

Create session.
```
curl -X POST http://localhost:8000/apps/nebula_prime_adk/users/u_1/sessions/s_1 \
  -H "Content-Type: application/json" \
  -d '{
    "clninical_contenxt": "nephrology",
    "clinical_reports": " Patient Name: John Doe Date of Birth: June 4, 1995 Age: 30 years Study Date: June 5, 2025 Referring Physician: Dr. Jane Smith Procedure: Non-Contrast CT Scan of the Abdomen and Pelvis Indication: Acute right flank pain with suspected nephrolithiasis. Findings: Kidneys: The right kidney exhibits mild hydronephrosis with perinephric fat stranding. A 6 mm hyperdense calculus is identified at the right ureteropelvic junction (UPJ), consistent with a nephrolithiasis. The left kidney appears normal with no evidence of calculi or hydronephrosis. Ureters: The right proximal ureter is dilated up to the level of the obstructing calculus. No additional stones are visualized along the course of the ureters. Bladder: Normal in appearance with no intraluminal calculi. Other Findings: No evidence of appendicitis, diverticulitis, or other intra-abdominal pathology.\nImpression:6 mm obstructing calculus at the right ureteropelvic junction causing mild hydronephrosis and perinephric fat stranding, indicative of acute nephrolithiasis. No additional urinary tract calculi identified. Recommendations: Urological consultation for management of obstructing ureteral stone. Consideration of pain management and hydration therapy. Follow-up imaging to monitor for stone passage or need for intervention. Radiologist: Dr. Emily Johnson, MD."
}' | jq .
```

Invoke the coordinator.
```
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
    "app_name": "nebula_prime_adk",
    "user_id": "u_1",
    "session_id": "s_1",
    "new_message": {
        "role": "user",
        "parts": [
            {
                "text": "What is the diagnosis for this patient?"
            }
        ]
    },
    "streaming": false
}' 2>/dev/null | jq .
```

## Running the Agents in AgentEngine
Install glcoud CLI tool.

Initialize gcloud config.
```
gcloud init
```

Login using gcloud.
```
gcloud auth login
```


Deploy to AgentEngine.

```
python deployment/deploy.py --create
```

List agents to see if deploy.py is configured correctly.

```
python deployment/deploy.py --list
```

Update agents. Note that GCP API and SDK version is broken on one requiring gcs_uri and another not. So, update code needs a fix when GCP fixes their SDK.

```
python deployment/deploy.py --update --resource_id 2871159111657979904
```


Delete, if desired.

```
python deployment/deploy.py --delete --resource_id 2871159111657979904
```

Create session with state.

```
curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904:query -d '{
    "class_method": "create_session",
    "input": {
        "user_id": "u_1",
        "state": {
            "clinical_context": "nephrology",
            "clinical_reports": "Patient Name: John Doe\n Date of Birth: June 4, 1995\n Age: 30 years\n Study Date: June 5, 2025\n Referring Physician: Dr. Jane Smith \nProcedure: Non-Contrast CT Scan of the Abdomen and Pelvis  \n Indication: Acute right flank pain with suspected nephrolithiasis.  \nFindings: Kidneys: The right kidney exhibits mild hydronephrosis with perinephric fat stranding. A 6 mm hyperdense calculus is identified at the right ureteropelvic junction (UPJ), consistent with a nephrolithiasis. The left kidney appears normal with no evidence of calculi or hydronephrosis.\n Ureters: The right proximal ureter is dilated up to the level of the obs \ntructing calculus. No additional stones are visualized along the course of the ureters.\n Bladder: Normal in appearance with no intraluminal calculi. Other Findings: No evidence of appendicitis, diverticulitis, or other intra-abdominal pathology.\n Impression:6 mm obstructing calculus at the right ureteropelvic junction causing mild hydronephrosis and perinephric fat stranding, indicative of acute nephrolithiasis. No additional urinary tract calculi identified. Recommendations: Urological consultation for management of obstructing ureteral stone. Consideration of pain management and hydration therapy. Follow-up imaging to monitor for stone passage or need for intervention.\n Radiologist: Dr. Emily Johnson, MD."
        }
    }
}'
```

Delete session.

```
curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904:query -d '{"class_method": "delete_session", "input": {"user_id": "_u1", "session_id": "7952473484343377920"}}'
```

List sessions. While this is documented [here](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-sessions-api), this api always returns error.

```
curl -X GET \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://us-central1-aiplatform.googleapis.com/v1/projects/nebula-prime-13736/locations/us-central1/reasoningEngines/2871159111657979904/sessions"
```

Query Agentic system.

```
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

## Disclaimer

- This project is not meant to be product offering clinical guidance or prescription at professional capacity. We entrust that to our clinicians. This is merely a demo project using AgenticAI
- This package contains code using ADK for AgentEngine part only. The frontend code and API layer code are not included
- This code does not come with any guarantee of correctness, use it at your own discretion
- The agent prompts are written using a multitude of GenAI models including gpt4o and gemini flash. Do not use these in a live system for clinical use
- There are multiple layers of guard rails. The one using GCP checks API in diagram is currently in private beta versioned as v1alpha1. Do not use alpha or beta anything in a production system
- This project has not bee rigorously tested, please do test and provide us feedback

## License

```
Copyright CloudSoftonic Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```