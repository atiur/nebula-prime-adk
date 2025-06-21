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

from google.adk.agents import (
    LlmAgent,
    ParallelAgent,
)
from google.adk.tools import google_search
from dotenv import load_dotenv
import os

from . import prompt, description

load_dotenv()
MODEL = "gemini-2.0-flash"

breast_cancer = LlmAgent(
    name="breast_cancer",
    model=MODEL,
    description=description.breast_cancer,
    instruction=prompt.breast_cancer,
    tools=[google_search],
    output_key="breast_cancer",
)

colon_cancer = LlmAgent(
    name="colon_cancer",
    model=MODEL,
    description=description.colon_cancer,
    instruction=prompt.colon_cancer,
    tools=[google_search],
    output_key="colon_cancer",
)


brain_cancer = LlmAgent(
    name="brain_cancer",
    model=MODEL,
    description=description.brain_cancer,
    instruction=prompt.brain_cancer,
    tools=[google_search],
    output_key="brain_cancer",
)

oncology_coordinator = ParallelAgent(
    name="oncology_coordinator",
    sub_agents=[breast_cancer, colon_cancer, brain_cancer],
    description=description.oncology_coordinator,
)
