#!/usr/bin/env python3

import requests
import json
import base64

def create_jira_issue(
    jira_base_url,
    auth_user,
    auth_pass,
    project_key,
    summary,
    description,
    issue_type="Story",
    customfield_10001_value=None,  # e.g. "TeamValueForFeatureLink"
    customfield_10501_value=None,  # e.g. "TeamValueForCorpTestTeam"
    assignee_username=None
):
    """
    Creates a Jira issue using the REST API v2, filling required custom fields.

    :param jira_base_url: Full URL of Jira (e.g. "https://jira.service.test.com")
    :param auth_user: Username for Basic Auth (or the username part if using token as password)
    :param auth_pass: Password or personal access token
    :param project_key: The key of the project where the issue will be created
    :param summary: Summary (title) of the issue
    :param description: Description of the issue
    :param issue_type: The type/name of the Jira issue (default "Story")
    :param customfield_10001_value: The "Team" value or object for customfield_10001
    :param customfield_10501_value: The "Team" value or object for customfield_10501
    :param assignee_username: (Optional) The username to assign the issue to
    :return: The JSON response from Jira if successful
    """

    # Construct the endpoint for creating an issue
    create_issue_url = f"{jira_base_url}/rest/api/2/issue"

    # Base fields
    fields_data = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    # If these custom fields are required, fill them in here:
    # The exact syntax depends on how your Jira field is configured (text vs single-select).
    if customfield_10001_value is not None:
        fields_data["customfield_10001"] = customfield_10001_value

    if customfield_10501_value is not None:
        fields_data["customfield_10501"] = customfield_10501_value

    # If you'd like to assign the issue
    if assignee_username:
        fields_data["assignee"] = {"name": assignee_username}

    payload = {"fields": fields_data}

    # Basic Auth: username + password/token
    auth_str = f"{auth_user}:{auth_pass}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {b64_auth}"
    }

    # Make the POST request
    response = requests.post(create_issue_url, headers=headers, data=json.dumps(payload))

    if response.status_code not in (200, 201):
        raise Exception(
            f"Failed to create Jira issue. "
            f"Status Code: {response.status_code} | Response: {response.text}"
        )

    return response.json()


if __name__ == "__main__":
    # Example usage
    JIRA_BASE_URL = "https://jira.service.test.com"
    USERNAME = "myuser"
    PASSWORD = "mypassword"  # or personal access token, if Jira is set up that way

    # The "Team" values that must be filled
    # Some fields need a string, others a dictionary { "value": "X" } or { "id": "Y" }
    CF_10001_VALUE = "TeamValueForFeatureLink"
    CF_10501_VALUE = "TeamValueForCorpTestTeam"

    # Or, if it's a single-select field, you might try:
    # CF_10001_VALUE = {"value": "Feature Link Team A"}
    # CF_10501_VALUE = {"value": "Corp Test Team A"}

    try:
        created_issue = create_jira_issue(
            jira_base_url=JIRA_BASE_URL,
            auth_user=USERNAME,
            auth_pass=PASSWORD,
            project_key="TEST",
            summary="New Issue with Required Fields",
            description="Filling the required custom fields for teams...",
            issue_type="Story",
            customfield_10001_value=CF_10001_VALUE,
            customfield_10501_value=CF_10501_VALUE
        )
        print("Issue created successfully!")
        print(created_issue)
    except Exception as e:
        print("Error creating issue:", e)