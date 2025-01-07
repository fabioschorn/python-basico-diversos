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
                                  Placed in the Authorization: Bearer header.
    :param project_key: The Jira project key where the issue should be created (e.g. "ABC").
    :param summary: The summary (title) of the new issue.
    :param description: The description/body of the issue (plain text or Jira wiki formatting).
    :param issue_type: Issue type name (e.g. "Story", "Task", "Bug"). Defaults to "Story".
    :param assignee_username: (Optional) Username to assign the issue (if Jira still supports usernames).
    :param custom_fields: (Optional) A dict of custom fields (e.g. {"customfield_10001": "Value"}).
                         If your Jira requires "Team values" or anything else, put them here.
    :return: A dict representing the JSON response from Jira, typically containing the new issue key.
    """

    # Endpoint for creating issues in Jira Server 9.x
    create_issue_url = f"{jira_base_url}/rest/api/2/issue"

    # Base fields for the issue
    fields_data = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    # If specifying an assignee (depends on your Jira config if "name" or "accountId" is needed)
    if assignee_username:
        fields_data["assignee"] = {"name": assignee_username}

    # Merge custom fields if provided (e.g., customfield_10001, customfield_10501, etc.)
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

    # 1) Make sure you have the full HTTPS URL
    JIRA_BASE_URL = "https://jira.service.test.com"

    # 2) Replace with your actual personal access token
    PERSONAL_ACCESS_TOKEN = "YOUR_JIRA_PERSONAL_ACCESS_TOKEN"

    # 3) Basic fields
    PROJECT_KEY = "TEST"
    SUMMARY = "Sample Story with a Personal Access Token"
    DESCRIPTION = (
        "This story was created in Jira Server 9.12.x using a Bearer token (PAT). "
        "We also added the custom fields to satisfy the required Team fields."
    )

    # 4) If your Jira requires "Team value" for customfield_10001 or customfield_10501,
    #    define them here. For example, if the field is a simple text field:
    #    "customfield_10001": "Team for Feature Link",
    #    "customfield_10501": "Team for Corp-Test Team"
    #
    #    If they are single select fields, you might need e.g.:
    #    {"customfield_10001": {"value": "MyTeamName"}}
    #    or even {"id": "1234"} depending on your field config.
    custom_fields_required = {
        "customfield_10001": "Team for Feature Link",
        "customfield_10501": "Team for Corp-Test Team"
    }

    try:
        result = create_jira_issue_with_pat(
            jira_base_url=JIRA_BASE_URL,
            personal_access_token=PERSONAL_ACCESS_TOKEN,
            project_key=PROJECT_KEY,
            summary=SUMMARY,
            description=DESCRIPTION,
            issue_type="Story",
            assignee_username=None,  # or "someuser" if needed
            custom_fields=custom_fields_required
        )
        print("Issue created successfully!")
        print("Response:", result)
        # Typically includes {'id': '10000', 'key': 'TEST-42', 'self': 'https://...'}
    except Exception as e:
        print("Error creating issue:", e)