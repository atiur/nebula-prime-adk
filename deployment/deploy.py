# Copyright 2025 Cloud
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

# This script is based on example code in adk-samples repo from Google.

import os

import vertexai
from absl import app, flags
from dotenv import load_dotenv
from nebula_prime_adk.agent import root_agent
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

load_dotenv()

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"), "GOOGLE_CLOUD_PROJECT")
flags.DEFINE_string("location", os.environ.get("GOOGLE_CLOUD_LOCATION"), "GOOGLE_CLOUD_LOCATION")
flags.DEFINE_string("bucket", os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET"), "GOOGLE_CLOUD_STORAGE_BUCKET")
flags.DEFINE_string("resource_id", None, "RESOURCE_ID"  )

flags.DEFINE_bool("list", False, "List all agents.")
flags.DEFINE_bool("create", False, "Creates a new agent.")
flags.DEFINE_bool("update", False, "Updates an existing agent.")
flags.DEFINE_bool("delete", False, "Deletes an existing agent.")
flags.mark_bool_flags_as_mutual_exclusive(["create", "update", "delete"])

requirements=[
    "google-adk(==1.3.0)",
    "google-api-core(==2.25.0)",
    "google-api-python-client(==2.171.0)",
    "google-auth(==2.40.3)",
    "google-auth-httplib2(==0.2.0)",
    "google-cloud-aiplatform(==1.97.0)",
    "google-cloud-appengine-logging(==1.6.1)",
    "google-cloud-audit-log(==0.3.2)",
    "google-cloud-bigquery(==3.34.0)",
    "google-cloud-core(==2.4.3)",
    "google-cloud-logging(==3.12.1)",
    "google-cloud-resource-manager(==1.14.2)",
    "google-cloud-secret-manager(==2.24.0)",
    "google-cloud-speech(==2.32.0)",
    "google-cloud-storage(==2.19.0)",
    "google-cloud-trace(==1.16.1)",
    "google-crc32c(==1.7.1)",
    "google-genai(==1.19.0)",
    "google-resumable-media(==2.7.2)",
    "googleapis-common-protos(==1.70.0)",
    "grpc-google-iam-v1(==0.14.2)",
    "pydantic (>=2.10.6,<3.0.0)",
    "python-dotenv (==1.1.0)",
    "pydantic(==2.11.5)",
    "pydantic-settings(==2.9.1)",
    "pydantic_core(==2.33.2)",
    "litellm (==1.72.4)",
    "absl-py (==2.3.0)",
    "cloudpickle (==3.1.1)",
]
extra_packages = [
    "nebula_prime_adk",
]
display_name="nebulla_prime_adk"
description="nebulla_prime_adk"

def create() -> None:
    """Creates an agent engine for Marketing Agency."""
    adk_app = AdkApp(agent=root_agent, enable_tracing=True)

    remote_app = agent_engines.create(
        adk_app,
        display_name=display_name,
        description=description,
        requirements=requirements,
        extra_packages = extra_packages,
    )

    print(f"Created remote agent: {remote_app.resource_name}")

def update(resource_id: str) -> None:
    remote_agent = agent_engines.get(resource_id)
    remote_agent.update(
        display_name=display_name,
        description=description,
        requirements=requirements,
        extra_packages = extra_packages,
        )
    print(f"Updated remote agent: {resource_id}")


def delete(resource_id: str) -> None:
    remote_agent = agent_engines.get(resource_id)
    remote_agent.delete(force=True)
    print(f"Deleted remote agent: {resource_id}")


def list_agents() -> None:
    remote_agents = agent_engines.list()
    template = """
{agent.name} ("{agent.display_name}")
- Create time: {agent.create_time}
- Update time: {agent.update_time}
"""
    remote_agents_string = "\n".join(
        template.format(agent=agent) for agent in remote_agents
    )
    print(f"All remote agents:\n{remote_agents_string}")


def main(argv:list[str]=None) -> None:
    del argv  # unused
    project_id = (
        FLAGS.project_id
        if FLAGS.project_id
        else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = (
        FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    )
    bucket = (
        FLAGS.bucket
        if FLAGS.bucket
        else os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    )

    print(f"PROJECT: {project_id}")
    print(f"LOCATION: {location}")
    print(f"BUCKET: {bucket}")

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket:
        print(
            "Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET"
        )
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )

    if FLAGS.list:
        list_agents()
    elif FLAGS.create:
        create()
    elif FLAGS.update:
        if not FLAGS.resource_id:
            print("resource_id is required for delete")
            return
        update(FLAGS.resource_id)
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("resource_id is required for delete")
            return
        delete(FLAGS.resource_id)
    else:
        print("Unknown command")


if __name__ == "__main__":
    app.run(main)
