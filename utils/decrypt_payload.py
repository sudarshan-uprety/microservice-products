import base64
import json


def decrypt_payload(event):
    """
    Decrypt payload using base64 encoded string
    """
    if not event.get('body'):
        raise ValueError("Request body is missing")

    if event['isBase64Encoded']:
        body = base64.b64decode(event['body'])
    else:
        body = event['body'].encode('utf-8') if isinstance(event['body'], str) else event['body']

    content_type = event['headers'].get('Content-Type', '')
    if not content_type.startswith('multipart/form-data'):
        raise ValueError('Content-Type must be multipart/form-data')

    # Extract the boundary from the content type
    boundary = content_type.split("boundary=")[1]
    boundary = f'--{boundary}'

    # Split the body by boundary
    parts = body.split(boundary.encode())

    json_data = None
    image_data = None

    for part in parts:
        if part:
            part = part.strip()
            if not part or part == b'--':
                continue

            headers, content = part.split(b'\r\n\r\n', 1)
            headers = headers.decode('utf-8')
            content = content.rstrip(b'--').strip()

            if 'name="image"' in headers:
                image_data = content
            elif 'name="data"' in headers:
                try:
                    json_data = json.loads(content.decode('utf-8'))
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON in 'data' field")

    if json_data is None:
        raise ValueError('data field is missing in form data.')
    if image_data is None:
        raise ValueError('image field is missing in form data.')
    return json_data, image_data
