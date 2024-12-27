#!/usr/bin/env python3

import requests
import json

def create_jira_story(
    jira_domain: str,
    api_token: str,
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Story",
    assignee_account_id: str = None,
    custom_fields: dict = None
):
    """
    Creates a new issue (Story) in JIRA using the REST API (v3).

    :param jira_domain: Your JIRA domain (e.g. 'your-domain.atlassian.net').
    :param api_token: A valid API token (bearer token) for authentication.
                     If you're using a Cloud JIRA, generate this token from your Atlassian account.
    :param project_key: The key of the JIRA project (e.g. 'ABC') in which the issue will be created.
    :param summary: The summary (title) of the issue.
    :param description: The body description of the issue (can be plain text or Jira markup).
    :param issue_type: The type of issue to create (e.g., "Story", "Task", "Bug"). Defaults to "Story".
    :param assignee_account_id: (Optional) The Atlassian Account ID of the user to assign the issue to.
                                For JIRA Cloud, you need the user's accountId (not username/email).
    :param custom_fields: (Optional) A dictionary of custom fields. For example:
                          {"customfield_10011": "Value", "customfield_10012": 1234}
    :return: The JSON response from JIRA if successful, otherwise raises an exception.
    """

    # Construct the JIRA REST API endpoint for creating issues
    url = f"https://{jira_domain}/rest/api/3/issue"

    # Standard fields required by the JIRA v3 API
    # Note "fields" is a dictionary that includes 'project', 'issuetype', 'summary', 'description', etc.
    fields_payload = {
        "project": {
            "key": project_key
        },
        "summary": summary,
        "description": description,
        "issuetype": {
            "name": issue_type
        }
    }

    # If an assignee is specified, add it to the payload
    # For JIRA Cloud, you must use "accountId" instead of "name"/"emailAddress".
    if assignee_account_id:
        fields_payload["assignee"] = {"accountId": assignee_account_id}

    # If we have custom fields, merge them into the fields payload
    if custom_fields:
        fields_payload.update(custom_fields)

    # Construct the final payload to send to the API
    payload = {
        "fields": fields_payload
    }

    # Set up headers, using Bearer token auth for JIRA Cloud
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Perform the POST request to create the issue
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload)
    )

    # Check for non-201 status codes (201 = Created)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create issue in JIRA. Status code: {response.status_code}, "
                        f"Response: {response.text}")

    # Return the JSON response if successful
    return response.json()


if __name__ == "__main__":
    """
    Example usage of create_jira_story.
    Replace the placeholders with actual values:
      - <your-domain>.atlassian.net
      - <YOUR_API_TOKEN>
      - <PROJECT_KEY>
      - <YOUR_ACCOUNT_ID> (if you want to assign someone)
    
    Run:
        python3 create_jira_issue.py
    """
    # ----------------------------
    # Required variables:
    JIRA_DOMAIN = "your-domain.atlassian.net"
    API_TOKEN = "<YOUR_API_TOKEN>"
    PROJECT_KEY = "ABC"
    
    # Example input for the story
    SUMMARY = "Automated Story Creation from Python"
    DESCRIPTION = (
        "This story was created via REST API. \n\n"
        "Steps to reproduce:\n"
        "1. Write the code.\n"
        "2. Provide necessary fields.\n"
        "3. Execute the script.\n"
        "Expected: A new Story is created in JIRA."
    )
    
    # Optional: If you have an Account ID for the user you'd like to assign
    ASSIGNEE_ACCOUNT_ID = "<YOUR_ACCOUNT_ID>"

    # Optional: Additional custom fields (dictionary).
    # Example: "customfield_10011": "Some string value"
    custom_fields_dict = {
        # "customfield_10011": "Some string value",
        # "customfield_10012": 1234
    }

    try:
        issue_response = create_jira_story(
            jira_domain=JIRA_DOMAIN,
            api_token=API_TOKEN,
            project_key=PROJECT_KEY,
            summary=SUMMARY,
            description=DESCRIPTION,
            issue_type="Story",  # Could also be "Task", "Bug", etc.
            assignee_account_id=ASSIGNEE_ACCOUNT_ID,
            custom_fields=custom_fields_dict
        )

        print("Issue created successfully!")
        print("Issue Key:", issue_response.get("key"))
        print("Full Response:", issue_response)

    except Exception as e:
        print("Error creating issue:", e)