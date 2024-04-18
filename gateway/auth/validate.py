import os, requests, logging


def token(request):
    # Check header present in request
    if "Authorization" not in request.headers:
        logging.error(f"An Error occurred while retrieving Authorization header, headers: {request.headers}")
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    # Checks now if header is present but no token passed
    if not token:
        logging.error(f"An Error occurred while retrieving Authorization header content, headers: {request.headers}")
        return None, ("missing credentials", 401)

    # Conditions met, call the authentication service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    # Returns Tuple with the decoded token that includes 'Admin' claim, and no error; or None and error from auth service
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
