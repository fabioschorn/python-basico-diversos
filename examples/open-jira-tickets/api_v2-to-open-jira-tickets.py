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
    assignee_username=None,
    custom_fields=None
):
    """
    Creates an issue in JIRA Server/Data Center 9.12.x via REST API (/rest/api/2/issue).

    :param jira_base_url: The base URL of your on-premise Jira (e.g. 'https://jira.mycompany.com').
    :param auth_user: Username for Jira authentication (or 'email@company.com' if so configured).
    :param auth_pass: Password or personal access token, depending on your Jira's configuration.
    :param project_key: The key of the project in which to create the issue (e.g., 'ABC').
    :param summary: The summary (title) of the new issue.
    :param description: The body/description of the issue (in plain text or Jira wiki format).
    :param issue_type: The type of the issue (e.g. 'Story', 'Task', 'Bug'). Defaults to 'Story'.
    :param assignee_username: (Optional) If you want to assign the issue to a specific user. 
                              Must be a valid username (Jira Server 9.12 may still allow usernames).
    :param custom_fields: (Optional) A dict of custom fields. Example:
                          { "customfield_10000": "Some value", "customfield_10001": 42 }
    :return: The JSON response from Jira, including the new issue key (e.g. KEY-123).
    """

    # Construct the endpoint for creating an issue
    create_issue_url = f"{jira_base_url}/rest/api/2/issue"

    # Build the main 'fields' payload
    fields_data = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    # If an assignee is provided, specify in the payload
    if assignee_username:
        fields_data["assignee"] = {"name": assignee_username}

    # Merge any custom fields
    if custom_fields:
        fields_data.update(custom_fields)

    # Construct the overall request payload
    payload = {
        "fields": fields_data
    }

    # For Jira Server 9.12.15, you typically can use Basic Auth with a username + password (or token).
    auth_str = f"{auth_user}:{auth_pass}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {b64_auth}"
    }

    # Perform the POST request
    response = requests.post(
        url=create_issue_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create issue: {response.status_code}\n{response.text}")

    return response.json()


if __name__ == "__main__":
    # Example usage:
    JIRA_BASE_URL = "https://jira.mycompany.com"   # On-prem or Data Center URL
    USERNAME = "my_jira_username"
    PASSWORD_OR_TOKEN = "my_jira_password"  # or a personal access token if supported
    PROJECT_KEY = "ABC"
    
    SUMMARY = "Demo Story creation in Jira Server 9.12.15"
    DESCRIPTION = (
        "This issue was created via the Jira REST API (Server 9.12.x). "
        "It's a demo to show how to set summary, description, etc."
    )

    try:
        result = create_jira_issue(
            jira_base_url=JIRA_BASE_URL,
            auth_user=USERNAME,
            auth_pass=PASSWORD_OR_TOKEN,
            project_key=PROJECT_KEY,
            summary=SUMMARY,
            description=DESCRIPTION,
            issue_type="Story",
            assignee_username=None,  # or "someUser"
            custom_fields=None       # Example: {"customfield_10000": "Some value"}
        )
        print("Issue created successfully:", result)
    except Exception as e:
        print("Error creating issue:", e)