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
    create_issue_url = f"{jira_base_url}/rest/api/2/issue"

    fields_data = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }

    if assignee_username:
        fields_data["assignee"] = {"name": assignee_username}

    if custom_fields:
        fields_data.update(custom_fields)

    payload = {"fields": fields_data}
    auth_str = f"{auth_user}:{auth_pass}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {b64_auth}"
    }

    response = requests.post(
        url=create_issue_url,
        headers=headers,
        data=json.dumps(payload)
    )
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create issue: {response.status_code}\n{response.text}")

    return response.json()


if __name__ == "__main__":
    # Make sure you have the full HTTPS URL here:
    JIRA_BASE_URL = "https://jira.service.test.com"

    USERNAME = "your_jira_username"
    PASSWORD = "your_jira_password"  # or personal access token
    PROJECT_KEY = "TEST"

    SUMMARY = "Sample Story from Python"
    DESCRIPTION = "Creating a story in Jira 9.x with the correct https:// scheme."

    try:
        response = create_jira_issue(
            jira_base_url=JIRA_BASE_URL,
            auth_user=USERNAME,
            auth_pass=PASSWORD,
            project_key=PROJECT_KEY,
            summary=SUMMARY,
            description=DESCRIPTION,
            issue_type="Story"
        )
        print("Issue created successfully:", response)
    except Exception as e:
        print("Error creating issue:", e)