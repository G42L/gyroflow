# ------------------------------------------------------------------------------
# API settings
# ------------------------------------------------------------------------------
local_host, port = '127.0.0.1',  8050                   # No need to change this

# ------------------------------------------------------------------------------
# Jira settings
# ------------------------------------------------------------------------------
jiraServer = 'https://jira-vira.volvocars.biz'      # VCC JIRA Server
api_version = ['1.0', '2.0', 'latest']              # latest must be placed at last
url = "http://" + local_host + ":" + str(port)      # Address used to launch the web browser

# ------------------------------------------------------------------------------
# User settings
# ------------------------------------------------------------------------------
default_board_id = 2058                             # Board id in Jira (need a scrum board)
project_name = 'ARTINFO'                            # Project name in Jira
working_hours_per_day = 8                           # Set the number or working hours a day
time_to_storypoints = 1                             # Default is 1 (1d = 1 SP). For 1h = 1 SP, set value to 8 (8h/d)
unestimated_story_point = 1                         # Story Points to assign if issue not estimated
config = dict(
    # Download png as same size as on screen
    toImageButtonOptions=dict(
        format='svg',                               # one of png, svg, jpeg, webp
        filename='Plotly_Chart',
        width=None,
        height=None,
        scale=1,                                    # Multiply title/legend/axis/canvas sizes by this factor
    ),
    # Unbranded plotly
    modeBarButtonsToRemove=[
        'sendDataToCloud',
        #'zoomIn2d',
        #'zoomOut2d',
        #'hoverClosestCartesian',
        #'hoverCompareCartesian',
        #'hoverClosest3d',
        #'hoverClosestGeo',
        #'resetScale2d'
    ],
    scrollZoom=True,
    displaylogo=False,
    showLink=False)
margin_left = '0.0%'
margin_right = '0.0%'


# ------------------------------------------------------------------------------
# Agile Safe @ VCC - week split in PIs and PI sprints
# ------------------------------------------------------------------------------
PI_weeks = {
    # PI names
    'names': ['10', '22', '37', '49'],
    # PI weeks
    'PI10': ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
    'PI22': ['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37'],
    'PI37': ['38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49'],
    'PI49': ['50', '51', '52', '53', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
    'PI49_1': ['50', '51', '52', '53'],                                         # split for year change
    'PI49_2': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],     # split for year change
    # PI 10 Sprint weeks
    'PI10_S1':  ['11', '12'],
    'PI10_S2':  ['13', '14'],
    'PI10_S3': ['15', '16'],
    'PI10_S4': ['17', '18'],
    'PI10_S5': ['19', '20'],
    'PI10_S6': ['21', '22'],
    # PI 22 Sprint weeks
    'PI22_S1': ['23', '24'],
    'PI22_S2': ['25', '26'],
    'PI22_S3': ['27', '28'],
    'PI22_S4': ['29', '30', '31', '32', '33'],
    'PI22_S5': ['34', '35'],
    'PI22_S6': ['36', '37'],
    # PI 37 Sprint weeks
    'PI37_S1': ['38', '39'],
    'PI37_S2': ['40', '41'],
    'PI37_S3': ['42', '43'],
    'PI37_S4': ['44', '45'],
    'PI37_S5': ['46', '47'],
    'PI37_S6': ['48', '49'],
    # PI 49 Sprint weeks
    'PI49_S1': ['50', '51'],
    'PI49_S2_1': ['52', '53'],
    'PI49_S2_2': ['01', '02'],
    'PI49_S3': ['03', '04'],
    'PI49_S4': ['05', '06'],
    'PI49_S5': ['07', '08'],
    'PI49_S6': ['09', '10'],
}
