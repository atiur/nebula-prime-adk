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

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.tools import google_search
from dotenv import load_dotenv
import os

from . import prompt, description

load_dotenv()
MODEL = "gemini-2.0-flash"


nephrolithiasis = LlmAgent(
    name="nephrolithiasis",
    model=MODEL,
    description=description.nephrolithiasis,
    instruction=prompt.nephrolithiasis,
    output_key="nephrolithiasis",
    tools=[google_search],
)

renal_failure = LlmAgent(
    name="renal_failure",
    model=MODEL,
    description=description.renal_failure,
    instruction=prompt.renal_failure,
    output_key="renal_failure",
    tools=[google_search],
)

renal_cell_carcinoma = LlmAgent(
    name="renal_cell_carcinoma",
    model=MODEL,
    description=description.renal_cell_carcinoma,
    instruction=prompt.renal_cell_carcinoma,
    output_key="renal_cell_carcinoma",
    tools=[google_search],
)

nephrology_coordinator = ParallelAgent(
    name="nephrology_coordinator",
    sub_agents=[nephrolithiasis, renal_failure, renal_cell_carcinoma],
    description=description.nephrology_coordinator,
)
