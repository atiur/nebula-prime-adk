from vertexai import agent_engines
import logging
import json
from flask import jsonify
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
}

ADK_RESOURCE = "<Your Agent Engnie Resource Name>"

def create_session_and_query_diagnosis(user_id:str, state:dict) -> None:
    """
    Create a session and query the agentic system for the diagnosis.
    """
    adk_app = agent_engines.get(ADK_RESOURCE)
    session = adk_app.create_session(user_id=user_id, state=state)
    response = []
    for event in adk_app.stream_query(
        user_id=user_id,
        session_id=session['id'],
        message="What is the diagnosis for this patient?",
    ):
        response.append(event)
    final_result = []
    for r in response:
        content = r["content"]
        if "parts" in content:
            for p in content["parts"]:
                if "text" in p:
                    t = p["text"]
                    if t.startswith('```json'):
                        json_result = json.loads(t[7:-3])
                        final_result.append(json_result)
    adk_app.delete_session(user_id=user_id, session_id=session['id'])
    return final_result

def handler(request):
    """
    Handler for the API.
    """
    client = google.cloud.logging.Client()
    handler = CloudLoggingHandler(client, name="my-cloud-function-log")
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    if request.method == "OPTIONS":
        logging.info(f"Received OPTIONS request, potentially for CORS preflight")
        # Handle CORS preflight
        return ("", 204, headers)
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Query parameters: {request.args}")
    if request.method != 'POST':
        logging.info(f"Received non POST request, ignoring, will send a 405")
        return jsonify({'error': 'Only POST requests are accepted'}), 405
    logging.info(f"Received a POST request")
    content_type = request.headers["content-type"]
    request_json = {}
    if content_type == "application/json":
        request_json = request.get_json(silent=True)
    logging.info(f"Request body: {request.get_json()}")
    if "user_id" not in request_json or "state" not in request_json:
        return "Blank request"
    response = create_session_and_query_diagnosis(request_json["user_id"], request_json["state"])
    return (response, 200, headers)
