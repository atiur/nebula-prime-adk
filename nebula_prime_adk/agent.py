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

from google.adk.agents import LlmAgent
from dotenv import load_dotenv
import os

from . import prompt, description
from .nephrology import nephrology_coordinator
from .oncology import oncology_coordinator
from .guardrails import input_guardrail, output_guardrail

load_dotenv()

MODEL = "gemini-2.0-flash"


nebula_prime_coordinator = LlmAgent(
    name="nebula_prime_coordinator",
    description=description.nebula_prime_coordinator,
    instruction=prompt.nebula_prime_coordinator,
    model=MODEL,
    global_instruction=prompt.nebula_prime_adk_global_instruction,
    sub_agents=[nephrology_coordinator, oncology_coordinator],
    before_model_callback=input_guardrail,
    after_model_callback=output_guardrail,
    disallow_transfer_to_peers=True,
)

root_agent = nebula_prime_coordinator
