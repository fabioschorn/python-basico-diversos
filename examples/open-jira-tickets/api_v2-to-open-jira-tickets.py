#!/usr/bin/env python3

import requests
import json

def create_jira_issue_with_pat(
    jira_base_url: str,
    personal_access_token: str,
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Story",
    assignee_username: str = None,
    custom_fields: dict = None
):
    """
    Creates an issue in a Jira Server (9.12.x) or Data Center instance using a Personal Access Token
    and the REST API endpoint /rest/api/2/issue.

    :param jira_base_url: The base URL of your Jira server (e.g. "https://jira.service.test.com").
    :param personal_access_token: The personal access token (PAT) string. 
                                  This is placed in the Authorization: Bearer header.
    :param project_key: The Jira project key where the issue should be created (e.g. "ABC").
    :param summary: The summary (title) of the new issue.
    :param description: The description/body of the issue (plain text or Jira wiki formatting).
    :param issue_type: Issue type name (e.g. "Story", "Task", "Bug"). Defaults to "Story".
    :param assignee_username: (Optional) Username to assign the issue to (if Jira still supports usernames).
    :param custom_fields: (Optional) A dict of custom fields (e.g. {"customfield_10000": "Value"}).
    :return: A dict representing the JSON response from Jira, typically containing the new issue key.
    """

    # Endpoint for creating issues in Jira Server 9.x
    create_issue_url = f"{jira_base_url}/rest/api/2/issue"

    # Construct the fields payload
    fields_data = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    # If specifying an assignee
    if assignee_username:
        # In many Jira Server setups (pre-GDPR or no accountId usage), you can set:
        fields_data["assignee"] = {"name": assignee_username}
        # If your instance has switched to accountId (like Cloud or GDPR updates), 
        # you'd need "accountId": <value> instead of "name".

    # If there are custom fields, merge them in
    if custom_fields:
        fields_data.update(custom_fields)

    # Final JSON payload
    payload = {"fields": fields_data}

    # Use the personal access token in a Bearer auth header
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(
        url=create_issue_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    # Check for successful creation
    if response.status_code not in (200, 201):
        raise Exception(
            f"Failed to create Jira issue. "
            f"Status Code: {response.status_code} | Response: {response.text}"
        )

    return response.json()


if __name__ == "__main__":
    # Example usage:

    # IMPORTANT: Be sure to include 'https://' in the base URL
    JIRA_BASE_URL = "https://jira.service.test.com"

    # Replace this with your actual personal access token 
    # (which you've generated from your on-prem Jira 9.x Data Center/Server instance).
    PERSONAL_ACCESS_TOKEN = "YOUR_JIRA_PERSONAL_ACCESS_TOKEN"

    PROJECT_KEY = "TEST"
    SUMMARY = "Sample Story with a Personal Access Token"
    DESCRIPTION = (
        "This story was created in Jira Server 9.12.x using a Bearer token (PAT) "
        "instead of a username/password."
    )

    try:
        result = create_jira_issue_with_pat(
            jira_base_url=JIRA_BASE_URL,
            personal_access_token=PERSONAL_ACCESS_TOKEN,
            project_key=PROJECT_KEY,
            summary=SUMMARY,
            description=DESCRIPTION,
            issue_type="Story",
            assignee_username=None,  # or "someuser"
            custom_fields=None       # e.g. {"customfield_10001": "some value"}
        )
        print("Issue created successfully!")
        print("Response:", result)
        # Typically includes {'id': '10000', 'key': 'TEST-42', 'self': 'https://...'}
    except Exception as e:
        print("Error creating issue:", e)