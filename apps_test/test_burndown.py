import datetime
import os
import pickle

import plotly as plt
import plotly.graph_objects as go
import pytz
import tzlocal
from dateutil import parser, tz
from jira import JIRA

from styles import colors, font


def parse_burndown_timestamp(ts):
    localzone = tzlocal.get_localzone()
    naive = datetime.datetime.fromtimestamp(int(ts) / 1000, tz=pytz.utc).replace(tzinfo=None)
    return localzone.localize(naive)

def determine_sprint_weekends(sprint_start, sprint_end):
    endOfWeek = sprint_start.replace(hour=0, minute=0, second=0, microsecond=0) + \
                datetime.timedelta(days=7 - sprint_start.weekday())
    startOfWeekend = endOfWeek - datetime.timedelta(days=2)
    weekends = []

    while startOfWeekend < sprint_end:
        startOfNonWork = max(sprint_start, startOfWeekend)
        endOfNonWork = min(sprint_end, endOfWeek)

        weekends.append({'start': startOfNonWork,
                         'duration': endOfNonWork - startOfNonWork})

        endOfWeek += datetime.timedelta(weeks=1)
        startOfWeekend = endOfWeek - datetime.timedelta(days=2)
    return weekends

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)

def get_ideal_burndown(sprint_start, sprint_end, initialStoryPoints):

    weekends = determine_sprint_weekends(sprint_start, sprint_end)

    # List the week days
    weekendDays = list()
    firstWeekendDay = list()
    for weekend in weekends:
        weekendDays.append(weekend['start'].strftime("%B %d, %Y"))
        firstWeekendDay.append(weekend['start'].strftime("%B %d, %Y"))
        for ii in range(1, weekend['duration'].days + 1):
            weekendDays.append((weekend['start'] + datetime.timedelta(days=ii)).strftime("%B %d, %Y"))

    sprintLength = sprint_end - sprint_start
    storyPointPerSecond = initialStoryPoints / ((3600 * 24 * sprintLength.days + sprintLength.seconds) -
                                                (2 * 3600 * 24 * len(firstWeekendDay)))

    x = [sprint_start]
    y = [initialStoryPoints]
    for ii, dt in enumerate(daterange(sprint_start, sprint_end)):
        print(dt.strftime("%B %d, %Y %H:%M:%S"))
        #if dt.strftime("%B %d, %Y") == sprint_start.strftime("%B %d, %Y"):
        if dt.strftime("%B %d, %Y") == sprint_start.strftime("%B %d, %Y"):
            pass
        elif dt.strftime("%B %d, %Y") == sprint_end.strftime("%B %d, %Y"):
            x.append(sprint_end)
            y.append(0)
        elif dt.strftime("%B %d, %Y") in weekendDays:
            x.append(dt.replace(hour=00, minute=00, second=00, microsecond=000))
            if dt.strftime("%B %d, %Y") in firstWeekendDay:
                dtime = x[-1] - x[-2]
                if dtime.days == 1 and dtime.seconds == 0:
                    factor = 3600 * 24
                else:
                    factor = dtime.seconds
                y.append(y[-1] - (storyPointPerSecond * factor))
            else:
                y.append(y[-1])
        else:
            x.append(dt.replace(hour=00, minute=00, second=00, microsecond=000))
            dtime = x[-1] - x[-2]
            if dtime.days == 1 and dtime.seconds == 0:
                factor = 3600 * 24
            else:
                factor = dtime.seconds
            y.append(y[-1] - (storyPointPerSecond * factor))

    return x, y

with open('scope_change_burndown_chart.pkl', 'rb') as f:
    scope_change_burndown_chart, sprint_start, sprint_end, sprint_completed = pickle.load(f)


JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
jiraServer = 'https://jira-vira.volvocars.biz'  # VCC JIRA Server
jira = JIRA(basic_auth=(JIRA_USERNAME, JIRA_PASSWORD),
            options={'server': jiraServer},
            validate=False)

if not sprint_completed:
    sprint_completed = sprint_end

jira_statuses = dict()
issue_statuses = jira.statuses()
for issue_status in issue_statuses:
    jira_statuses[issue_status.id] = issue_status.name

issueDict = dict()
for timestamp, changelist in scope_change_burndown_chart['changes'].items():
    timestamp = parse_burndown_timestamp(timestamp)
    for change in changelist:
        # Skip parent issues
        if change['key'] in scope_change_burndown_chart['issueToParentKeys']:
            continue

        # Add the new issue to issueDict
        if change['key'] not in issueDict:
            issueDict[change['key']] = {}

        if (timestamp <= sprint_start and 'column' in change and 'done' in change['column']):
            issueDict[change['key']]['Workflow'] = 'Completed outside'
        elif (timestamp <= sprint_start and 'added' in change and change['key'] in issueDict):
            issueDict[change['key']]['Workflow'] = 'Committed'
        elif (timestamp <= sprint_end and 'added' in change and change['added'] and change['key'] in issueDict):
            issueDict[change['key']]['Workflow'] = 'Added'
        elif (timestamp > sprint_start and timestamp <= sprint_end and
              'added' in change and not change['added'] and change['key'] in issueDict):
            if issueDict[change['key']]['Workflow'] == 'Committed':
                issueDict[change['key']]['Workflow'] = 'Committed and Removed'
            elif issueDict[change['key']]['Workflow'] == 'Added':
                issueDict[change['key']]['Workflow'] = 'Added and Removed'
            else:
                issueDict[change['key']]['Workflow'] = 'Removed with unkown previous status'


issue_list = []
for timestamp, changelist in scope_change_burndown_chart['changes'].items():
    timestamp = parse_burndown_timestamp(timestamp)
    for change in changelist:
        if change['key'] not in issue_list:
            issue_list.append(change['key'])

for issue in issue_list:
    data = jira.issue(issue,
                      expand='changelog',
                      fields=[
                          'assignee',
                          'created',
                          'creator',
                          'customfield_10701',
                          'customfield_10708',
                          'issuetype',
                          'priority',
                          'reporter',
                          'resolution',
                          'status',
                          'updated'
                      ])

    # Save history
    issueDict[issue]['history'] = data.changelog.histories

    for changeLog in data.changelog.histories:
        for item in changeLog.items:
            # Get date
            timestamp = parser.parse(changeLog.created,
                                     tzinfos={"BRST": -7200,
                                              "CST": tz.gettz(tzlocal.get_localzone().zone)})

            if timestamp > sprint_end:
                # Stop the loop and take the next issue
                break
            elif item.field == 'Story Points':
                if timestamp <= sprint_start:
                    issueDict[issue]['StoryPoint'] = {
                        'Date': [sprint_start],
                        'Data': [float(item.toString)
                                 if item.toString != '' else None]
                    }
                elif timestamp <= sprint_end:
                    if 'StoryPoint' not in issueDict[issue]:
                        issueDict[issue]['StoryPoint'] = {
                            'Date': [timestamp],
                            'Data': [float(item.toString)
                                     if item.toString != '' else None]
                        }
                    else:
                        issueDict[issue]['StoryPoint']['Date'].append(timestamp)
                        issueDict[issue]['StoryPoint']['Data'].append(float(item.toString)
                                                                     if item.toString != '' else None)

            elif item.field == 'status':
                if timestamp <= sprint_start:
                    issueDict[issue]['Status'] = {
                        'Date': [sprint_start],
                        'Data': [{'from': item.fromString,
                                  'to': item.toString}]
                    }
                elif timestamp <= sprint_end:
                    if 'Status' not in issueDict[issue]:
                        issueDict[issue]['Status'] = {
                            'Date': [timestamp],
                            'Data': [{'from': item.fromString,
                                      'to': item.toString}]
                        }
                    else:
                        issueDict[issue]['Status']['Date'].append(timestamp)
                        issueDict[issue]['Status']['Data'].append({'from': item.fromString,
                                                                   'to': item.toString})

            elif item.field == 'Sprint':
                if timestamp <= sprint_start:
                    issueDict[issue]['Sprint'] = {
                        'Date': [sprint_start],
                        'Data': [{'from': item.fromString.split(',')[-1] if item.fromString else None,
                                  'to': item.toString.split(',')[-1]}]
                    }
                elif timestamp <= sprint_end:
                    if 'Sprint' not in issueDict[issue]:
                        issueDict[issue]['Sprint'] = {
                            'Date': [timestamp],
                            'Data': [{'from': item.fromString.split(',')[-1] if item.fromString else None,
                                      'to': item.toString.split(',')[-1]}]
                        }
                    else:
                        issueDict[issue]['Sprint']['Date'].append(timestamp)
                        issueDict[issue]['Sprint']['Data'].append({
                            'from': item.fromString.split(',')[-1] if item.fromString else None,
                            'to': item.toString.split(',')[-1]
                        })


"""
    Generate the plot
"""

weekends = determine_sprint_weekends(sprint_start, sprint_completed)

fig = go.Figure()

# Display weekends
wx, wy = list(), list()
for weekend in weekends:
    wx.extend([weekend['start'], weekend['start'],
       weekend['start'] + weekend['duration'], weekend['start'] + weekend['duration']])
    wy.extend([0, max(y)+3, max(y)+3, 0])
fig.add_trace(go.Scatter(
    name='Weekends' if len(weekends) != 1 else 'Weekend',
    x=wx,
    y=wy,
    fill='toself',
    fillcolor='lightgrey',
    hoveron='fills',
    line_color='lightgrey',
    mode="lines",
    opacity=0.5,
    text=None,
    hoverinfo=None)
)

# Team Burndown
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    text=hoverinfo,
    name="Team Burndown",
    mode='lines+markers',
    line_shape='hv',
    line=dict(color='red'),
),
)

xBurnIdeal, yBurnIdeal = get_ideal_burndown(sprint_start, sprint_end, initialStoryPoints)
fig.add_trace(go.Scatter(
    x=xBurnIdeal,
    y=yBurnIdeal,
    text=None,
    mode="lines",
    name="Ideal Burndown",
    marker=dict(symbol=None),
    line=dict(color='gray'),
),
)

fig.update_traces(hoverinfo='text')
fig.update_layout(title=None,
                  margin=dict(b=0,
                              l=5,
                              r=5,
                              t=5,
                              pad=0,
                              autoexpand=True),
                  autosize=True,
                  showlegend=True,
                  legend=dict(traceorder='normal',
                              font=dict(family=font['family'],
                                        size=font['size'],
                                        color=font['color'], ), ),
                  dragmode='zoom',
                  hovermode='closest',
                  paper_bgcolor=colors['paper_bgcolor'],
                  plot_bgcolor=colors['plot_bgcolor'],
                  font=dict(family=font['family'],
                            size=font['size'],
                            color=font['color'], ),
                  titlefont=dict(family=font['family'],
                                 size=font['size'],
                                 color=font['color'], ),
                  xaxis=dict(title='Time',
                             gridcolor="darkgrey",
                             range=[sprint_start, sprint_completed],
                             autorange=False,
                             zeroline=False,
                             zerolinecolor="black"),
                  yaxis=dict(title='Story Points',
                             gridcolor="darkgrey",
                             range=[0, max(y)+3],
                             dtick=5,
                             autorange=False,
                             zeroline=False,
                             zerolinecolor="black"),
                  )

plt.offline.plot(fig, filename='test.html')
