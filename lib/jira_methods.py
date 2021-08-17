"""
    This is a container of all JIRA methods used to extract data
"""

import os
import getpass
from jira import JIRA


def get_username_password():
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
    if not JIRA_USERNAME:
        JIRA_USERNAME = input('User ID: ')
    if not JIRA_PASSWORD:
        JIRA_PASSWORD = getpass.getpass('Password:')

    return JIRA_USERNAME, JIRA_PASSWORD


def create_jira_client(user, token, jiraServer):
    # ------------------------------------------------------------------------------
    # Connect to JIRA and get some parameters
    # ------------------------------------------------------------------------------
    return JIRA(basic_auth=(user, token), options={'server': jiraServer}, validate=False)


def get_project_workflows(JIRA_USERNAME, JIRA_PASSWORD, project, jiraServer):
    def search_for_project_workflows(JIRA_USERNAME,
                                     JIRA_PASSWORD,
                                     jiraServer=None,
                                     api_version='latest',
                                     projectIdOrKey="ARTINFO"):
        import requests
        import json

        url = jiraServer + '/rest/api/' + api_version + '/project/' + projectIdOrKey + '/statuses'
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "X-Atlassian-Token": "no-check"
        }
        query = {
            'projectId': 13204,
            'projectKey': 'ARTINFO',
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            # params=query,
            auth=(JIRA_USERNAME, JIRA_PASSWORD)
        )
        data = json.loads(response.text)

        return data

    # Get workflows in a project
    workflows = search_for_project_workflows(JIRA_USERNAME,
                                             JIRA_PASSWORD,
                                             jiraServer=jiraServer,
                                             api_version='latest',
                                             projectIdOrKey=project)
    # Get the index in workflows of all issue types
    workflows_key, workflows_statuses = dict(), dict()
    for idx1, key in enumerate(workflows):
        workflows_key[key['name']] = idx1
        if key['name'] not in workflows_statuses:
            workflows_statuses[key['name']] = dict()
        for idx2, status in enumerate(workflows[idx1]['statuses']):
            if status['name'] not in workflows_statuses[key['name']]:
                workflows_statuses[key['name']][status['name']] = idx2
    return workflows, workflows_key, workflows_statuses


def get_lead_time(jira: JIRA, project: str, lwg: str):
    query = 'project={} AND "Leading Work Group" IN ({}) AND status IN (Closed, Done) AND issuetype IN (Story)'
    issues = [jira.issue(x) for x in jira.search_issues(query.format(project, lwg))]
    return [{
        'Key': x.key,
        'Summary': x.fields.summary,
        'Description': x.fields.description,
        'Type': x.fields.issuetype.name,
        'Created': x.fields.created,
        'Updated': x.fields.updated,
        'Resolution': x.fields.resolution.name,
        'ResolutionDate': x.fields.resolutiondate,
             } for x in issues]


def get_active_incidents(jira: JIRA, project: str, lwg: str, fields: list):
    query = 'project={} AND "Leading Work Group" IN ({}) AND status NOT IN (Closed, Done) AND issuetype IN (Defect, "Problem Report", "Fault Report")'
    issues = [jira.issue(x) for x in jira.search_issues(query.format(project, lwg),
                                                        startAt=0,
                                                        maxResults=1000,
                                                        validate_query=True,
                                                        fields=','.join(fields),
                                                        expand=None,
                                                        json_result=False,
                                                        )]
    return [{
        'Key': x.key,
        'Summary': x.fields.summary,
        'Description': x.fields.description,
        'Type': x.fields.issuetype.name,
        'Created': x.fields.created,
        'Updated': x.fields.updated,
        'Resolution': x.fields.resolution.name if x.fields.resolution else None,
        'ResolutionDate': x.fields.resolutiondate,
    } for x in issues]


def get_closed_incidents(jira: JIRA, project: str, lwg: str, fields: list):
    query = 'project={} AND "Leading Work Group" IN ({}) AND status IN (Closed, Done) AND issuetype IN (Defect, "Problem Report", "Fault Report")'
    issues = [jira.issue(x) for x in jira.search_issues(query.format(project, lwg),
                                                        startAt=0,
                                                        maxResults=1000,
                                                        validate_query=True,
                                                        fields=','.join(fields),
                                                        expand=None,
                                                        json_result=False,
                                                        )]
    return [{
        'Key': x.key,
        'Summary': x.fields.summary,
        'Description': x.fields.description,
        'Type': x.fields.issuetype.name,
        'Created': x.fields.created,
        'Updated': x.fields.updated,
        'Resolution': x.fields.resolution.name if x.fields.resolution else None,
        'ResolutionDate': x.fields.resolutiondate,
    } for x in issues]
