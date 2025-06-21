# Copyright CloudSoftonic Pty Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
import logging


# Note that 
# 1. The checks API is in private beta currently v1alpha at the time of writing this code.
#    Until it becomes stable, it may be wise to not tie your code with it. Just stay aware
#    of the API changes and test at limited scale.
# 2. This is only part of the guardrails that have currently implemented. There are more in
#    agent prompts.
# 3. Code credit is to https://developers.google.com/checks/guide/ai-safety/guardrails


USE_CHECKS = False
# USE_CHECKS = os.environ.get("USE_CHECKS") == "True"


def input_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    if not USE_CHECKS:
        logging.warning("Bypassing Check guardrails on input validation.")
        return None

    SECRET_FILE_PATH = os.environ.get("SECRET_FILE_PATH = 'path/to/your/secret.json'") 
    checks_scope = 'https://www.googleapis.com/auth/checks'
    credentials = service_account.Credentials.from_service_account_file(
        SECRET_FILE_PATH, scopes=[checks_scope]
    )
 
    service = build('checks', 'v1alpha', credentials=credentials)
    request = service.aisafety().classifyContent(
        body={
            'input': {
                'textInput': {
                    'content': llm_request.contents,
                    'languageCode': 'en',
                }
            },
            'policies': [
                # Not that MEDICAL_INFO might be needed to be allowed and
                # PII_SOLICITING_RECITING requies deidentification of data
                {'policyType': 'DANGEROUS_CONTENT'},
                {'policyType': 'SEXUALLY_EXPLICIT'},
                {'policyType': 'OBSCENITY_AND_PROFANITY'},
            ],
        }
    )

    response = request.execute()
    for policy_result in response['policyResults']:
        if policy_result["violationResult"] == "VIOLATIVE":
            return f"We cannot proceed with this request as the request content is in violation of our {policy_result['policyType']} policy."
    return None


def output_guardrail(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> LlmResponse | None:
    if not USE_CHECKS:
        logging.warning("Bypassing Check guardrails on output validation.")
        return None

    SECRET_FILE_PATH = os.environ.get("SECRET_FILE_PATH = 'path/to/your/secret.json'") 
    checks_scope = 'https://www.googleapis.com/auth/checks'
    credentials = service_account.Credentials.from_service_account_file(
        SECRET_FILE_PATH, scopes=[checks_scope]
    )
 
    service = build('checks', 'v1alpha', credentials=credentials)
    request = service.aisafety().classifyContent(
        body={
            'input': {
                'textInput': {
                    'content': llm_response.contents,
                    'languageCode': 'en',
                }
            },
            'policies': [
                # Not that MEDICAL_INFO might be needed to be allowed and
                # PII_SOLICITING_RECITING requies deidentification of data
                {'policyType': 'DANGEROUS_CONTENT'},
                {'policyType': 'SEXUALLY_EXPLICIT'},
                {'policyType': 'OBSCENITY_AND_PROFANITY'},
            ],
        }
    )

    response = request.execute()
    for policy_result in response['policyResults']:
        if policy_result["violationResult"] == "VIOLATIVE":
            return f"We cannot proceed with this request as the request content is in violation of our {policy_result['policyType']} policy."
    return None
