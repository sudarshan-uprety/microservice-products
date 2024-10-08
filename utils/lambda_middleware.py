import json
import time
import uuid
from functools import wraps
from copy import deepcopy

from utils.log import logger, trace_id_var

# List of sensitive fields to redact
SENSITIVE_FIELDS = [
    "password", "confirm_password", "new_password", "current_password",
    "access_token", "refresh_token", "id_token"
]


def sanitize_payload(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, dict):
        sanitized = {}
        for key, value in payload.items():
            if key in SENSITIVE_FIELDS:
                sanitized[key] = "******"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_payload(value)
            else:
                sanitized[key] = value
        return sanitized
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    else:
        return payload


def lambda_middleware(handler):
    @wraps(handler)
    def wrapper(event, context):
        body = event.get('body', {})

        # If body is a string, try to parse it as JSON
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                logger.debug("Failed to parse body as JSON")
                body = {}

        if body is None:
            body = {}

        trace_id = body.get('trace_id')

        # If trace_id is not found in the body, generate a new one
        if not trace_id:
            trace_id = str(uuid.uuid4())

        start_time = time.time()
        client_ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'Unknown')

        # Sanitize and prepare the request payload
        sanitized_event = sanitize_payload(deepcopy(event)) or {}
        request_payload = sanitized_event.get('body')
        if request_payload:
            try:
                request_payload = json.loads(request_payload)
            except json.JSONDecodeError:
                pass

        try:
            response = handler(event, context)
            process_time = time.time() - start_time

            log_dict = {
                "url": event.get('path'),
                "method": event.get('httpMethod'),
                "process_time": f"{process_time:.4f}",
                "status_code": response.get('statusCode'),
                "trace_id": trace_id,
                "client_ip": client_ip,
                "request_payload": sanitize_payload(request_payload)
            }

            log_message = json.dumps(log_dict)

            if response.get('statusCode', 200) >= 500:
                logger.error(f"Request failed: {log_message}")
            elif response.get('statusCode', 200) >= 400:
                logger.warning(f"Request resulted in client error: {log_message}")
            else:
                logger.info(f"Request completed successfully: {log_message}")

        except Exception as e:
            process_time = time.time() - start_time
            logger.exception(f"Request failed with exception: {str(e)}", extra={
                "url": event.get('path'),
                "method": event.get('httpMethod'),
                "process_time": f"{process_time:.4f}",
                "client_ip": client_ip,
                "request_payload": request_payload,
            })
            raise

        return response

    return wrapper
