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

nebula_prime_coordinator = """
A helpful and expert AI assistant for nephrology and oncology specialists.
Helps specialist, clinician users by assessing nephrology and oncology disaseases using provided clinical data.
Based on input context, engages either nephrology or oncology specialist teams and return their response.
"""

input_guardrail = """
A GuardRail agent to screen the input context and reports for potential threats.
"""

output_guardrail = """
A GuardRail agent to screen the output for policy violations.
"""
