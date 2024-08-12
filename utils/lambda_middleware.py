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
        trace_id = event.get('headers', {}).get("X-Trace-ID", str(uuid.uuid4()))
        trace_id_var.set(trace_id)

        start_time = time.time()
        client_ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'Unknown')

        # Sanitize and prepare the request payload
        sanitized_event = sanitize_payload(deepcopy(event)) or {}
        request_payload = sanitized_event.get('body')
        if request_payload:
            try:
                request_payload = json.loads(request_payload)
            except json.JSONDecodeError:
                pass  # Keep it as a string if it's not JSON

        try:
            # Call the actual handler
            response = handler(event, context)
            process_time = time.time() - start_time

            # Prepare and sanitize the response payload
            response_payload = response.get('body')
            if response_payload:
                try:
                    response_payload = json.loads(response_payload)
                except json.JSONDecodeError:
                    pass  # Keep it as a string if it's not JSON
            sanitized_response_payload = sanitize_payload(response_payload)

            log_dict = {
                "url": event.get('path'),
                "method": event.get('httpMethod'),
                "process_time": f"{process_time:.4f}",
                "status_code": response.get('statusCode'),
                "trace_id": trace_id,
                "client_ip": client_ip,
                "request_payload": request_payload,
                "response_payload": sanitized_response_payload
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
                "trace_id": trace_id,
                "client_ip": client_ip,
                "request_payload": request_payload,
            })
            raise

        return response

    return wrapper
