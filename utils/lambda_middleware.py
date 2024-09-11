import json
import time
import uuid
from functools import wraps
from typing import Dict, Any

from utils.log import logger

SENSITIVE_FIELDS = frozenset([
    "password", "confirm_password", "new_password", "current_password",
    "access_token", "refresh_token", "id_token"
])


def sanitize_payload(payload: Any) -> Any:
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
    def wrapper(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        start_time = time.time()

        # Extract and sanitize relevant information
        body = event.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {}

        trace_id = body.get('trace_id') or str(uuid.uuid4())
        client_ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'Unknown')

        sanitized_payload = sanitize_payload(body)

        log_dict = {
            "url": event.get('path'),
            "method": event.get('httpMethod'),
            "trace_id": trace_id,
            "client_ip": client_ip,
            "request_payload": sanitized_payload
        }

        try:
            response = handler(event, context)
            process_time = time.time() - start_time
            status_code = response.get('statusCode', 200)

            log_dict.update({
                "process_time": f"{process_time:.4f}",
                "status_code": status_code
            })

            log_message = json.dumps(log_dict)

            if status_code >= 500:
                logger.error(f"Request failed: {log_message}")
            elif status_code >= 400:
                logger.warning(f"Request resulted in client error: {log_message}")
            else:
                logger.info(f"Request completed successfully: {log_message}")

            return response

        except Exception as e:
            process_time = time.time() - start_time
            log_dict["process_time"] = f"{process_time:.4f}"
            logger.exception(f"Request failed with exception: {str(e)}", extra=log_dict)
            raise

    return wrapper
