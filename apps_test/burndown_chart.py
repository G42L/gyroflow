from jira import JIRA

# borad_id = 2058
# sprint_id = 35573
# https://jira-vira.volvocars.biz/rest/greenhopper/latest/rapid/charts/scopechangeburndownchart?rapidViewId=2058&sprintId=35573

# Connect to JIRA
jira = JIRA(basic_auth=('glegigan', 'FYNdni75@('),
            options={'server': 'https://jira-vira.volvocars.biz/'},
            validate=False)
# Get board names
boards = jira.boards()
board_id = 2058
sprint_id = 27693
data = jira._get_json('rapid/charts/scopechangeburndownchart?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                                      base=jira.AGILE_BASE_URL)
data = jira._get_json('rapid/charts/scopechangeburndownchart?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                                      base=jira.AGILE_BASE_URL)

jql_Mario = 'project = ARTINFO AND "Leading Work Group" = "ARTINFO Team - Mario" ORDER BY Rank ASC'
jql_ForcePush = 'project = ARTINFO AND "Leading Work Group" = "ARTINFO Team - Force Push" ORDER BY Rank ASC'
data = jira.search_issues(jql_Mario, startAt=0, maxResults=1000, validate_query=True, fields='key', expand=None, json_result=False)


jql_request = jira.search_issues('SPRINT IN ("Force Push PI_19w37_1") AND ' +
                                 'status changed ON ("2019-09-27 19:00")',
                                 startAt=0,
                                 maxResults=1000,
                                 validate_query=True,
                                 fields='status',
                                 expand=None,
                                 json_result=False)
issues = jira.search_issues('SPRINT IN ("Force Push PI_19w37_1")',
                                 startAt=0,
                                 maxResults=1000,
                                 validate_query=True,
                                 fields='issuetype',
                                 expand=None,
                                 json_result=False)
issues[0].fields.issuetype.name


sprint_completed_issues_planned = jira.search_issues(
                    'issueFunction IN completeInSprint("ARTINFO PO DevOps", "Force Push PI_19w37_1") AND ' + \
                    'issueFunction NOT IN addedAfterSprintStart("ARTINFO PO DevOps", "Force Push PI_19w37_1")',
                    startAt=0,
                    maxResults=1000,
                    validate_query=True,
                    fields='customfield_10708',
                    expand=None,
                    json_result=False)
sprint_completed_issues_planned[0].key


print(data)