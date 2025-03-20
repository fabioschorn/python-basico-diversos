import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# I'm still tweaking and playing around, but I'll upload it anyway!!!
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis("off") # Turn on if you want to see the axes

# --- Colors ---
lambda_color = "#F58536"
s3_color     = "#569A31"
db_color     = "#527FFF"
jira_color   = "#0052CC"
light_gray   = (0.92, 0.92, 0.92)

# --------------------------------------------------
# 1) Left Column: CSV Box & S3
# --------------------------------------------------
# Left bounding box for "Report Qualys (CSV)"
report_x, report_y = 0.5, 1.0
report_w, report_h = 3.0, 6.0

report_box = mpatches.FancyBboxPatch(
    (report_x, report_y),
    report_w,
    report_h,
    boxstyle="round,pad=0.3",
    edgecolor="gray",
    facecolor="none",
    linestyle="--"
)
ax.add_patch(report_box)

ax.text(report_x + report_w/2, report_y + report_h - 0.3,
        "Report Qualys (CSV)", ha="center", va="top",
        fontsize=11, fontweight="bold")

# User (top of the box)
user_x = report_x + report_w/2
user_y = report_y + report_h - 1.0
ax.text(user_x, user_y, "User",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="circle,pad=0.3",
                  edgecolor="black", facecolor="white"))

# CSV labels stacked
csv_coords = [
    (user_x, user_y - 1.3),
    (user_x, user_y - 2.2),
    (user_x, user_y - 3.1),
]
for i, (cx, cy) in enumerate(csv_coords, start=1):
    ax.text(cx, cy, f"CSV {i}",
            ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="square,pad=0.3",
                      edgecolor=s3_color, facecolor="white"))

# Amazon S3 to the right of CSV box
s3_pos = (3.1, 4.0)  # x=4.5, y=4.5
ax.text(*s3_pos,
        "Amazon S3\n(Reports)",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.5",
                  edgecolor="black", facecolor=s3_color, alpha=0.8))

# Arrow from top CSV to S3
ax.annotate("Upload CSVs",
            xy=s3_pos,
            xytext=(report_x + report_w, csv_coords[0][1]),
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="bottom", fontsize=9)

# --------------------------------------------------
# 2) AWS Cloud bounding box (covering center to right)
# --------------------------------------------------
aws_x, aws_y = 4.2, 0.5
aws_w, aws_h = 11.5, 7.0

aws_box = mpatches.FancyBboxPatch(
    (aws_x, aws_y),
    aws_w,
    aws_h,
    boxstyle="round,pad=0.3",
    edgecolor="black",
    facecolor=light_gray,
    alpha=0.5,
    linewidth=1.5
)
ax.add_patch(aws_box)

ax.text(aws_x + aws_w/2, aws_y + aws_h - 0.3,
        "AWS Cloud", ha="center", va="top",
        fontsize=12, fontweight="bold")

# --------------------------------------------------
# 3) Layout Inside AWS: We'll make a simple grid
#    Row 1 (y=6):  Parse & Split, Compare & Identify, Ticket Status
#    Row 2 (y=4):  Test Data from S3, Create JIRA, JIRA
#    Row 3 (y=2):  Send to DB,  Store QIDs (DB), Teams
# --------------------------------------------------

# Row 1
parse_pos   = (6.0, 6.0)
compare_pos = (9.0, 6.0)
ticket_pos  = (12.0, 6.0)

ax.text(*parse_pos, "Lambda:\nParse & Split\nCSV",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.6",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

ax.text(*compare_pos, "Lambda:\nCompare & Identify\n(CSVs Diff)",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

ax.text(*ticket_pos, "Lambda:\nTicket Status\nCheck",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

# Row 2
testS3_pos    = (6.0, 4.0)
createJira_pos= (9.0, 4.0)
jira_pos      = (12.0, 4.0)

ax.text(*testS3_pos, "Lambda:\nTest Data\nfrom S3",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

ax.text(*createJira_pos, "Lambda:\nCreate JIRA",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

ax.text(*jira_pos, "JIRA",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=2.9",
                  edgecolor="black", facecolor=jira_color, alpha=0.9))

# Row 3
sendDB_pos  = (6.0, 2.0)
storeDB_pos = (9.0, 2.0)
teams_pos   = (12.0, 2.0)

ax.text(*sendDB_pos, "Lambda:\nSend to DB",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3",
                  edgecolor="black", facecolor=lambda_color, alpha=0.8))

ax.text(*storeDB_pos, "Store QIDs\n(DB)",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=1.3",
                  edgecolor="black", facecolor=db_color, alpha=0.8))

ax.text(*teams_pos, "Teams\n(Signed Tickets)",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=1.3",
                  edgecolor="red", facecolor="white"))

# --------------------------------------------------
# 4) Connect with Short, Non-Crossing Arrows
# --------------------------------------------------

# S3 -> Parse
ax.annotate("Trigger",
            xy=(parse_pos[0]-0.4, parse_pos[1]),
            xytext=(s3_pos[0]+0.4, s3_pos[1]),
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="center", fontsize=8)

# Parse -> Compare (straight line on Row 1)
ax.annotate("Parsed data",
            xy=compare_pos,
            xytext=parse_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="bottom", fontsize=8)

# Compare -> TicketStatus (straight line on Row 1)
ax.annotate("Check tickets",
            xy=ticket_pos,
            xytext=compare_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="bottom", fontsize=8)

# Compare -> Send to DB (vertical from row 1 down to row 3)
ax.annotate("Diff results",
            xy=sendDB_pos,
            xytext=(compare_pos[0], compare_pos[1]-0.5),
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="center", fontsize=8)

# Send DB -> Store DB (row 3, horizontal)
ax.annotate("", xy=storeDB_pos, xytext=sendDB_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5))

# S3 -> Test Data from S3 (diagonal but short)
ax.annotate("Ticket data",
            xy=testS3_pos,
            xytext=(s3_pos[0]+0.2, s3_pos[1]),
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="center", fontsize=8)

# DB -> Create JIRA (vertical from row 3 to row 2)
ax.annotate("QIDs data",
            xy=createJira_pos,
            xytext=storeDB_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5),
            ha="center", va="center", fontsize=8)

# Create JIRA -> JIRA (row 2, horizontal)
ax.annotate("", xy=jira_pos, xytext=createJira_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5))

# TicketStatus -> JIRA (vertical from row 1 to row 2)
ax.annotate("", xy=jira_pos,
            xytext=ticket_pos,
            arrowprops=dict(arrowstyle="->", lw=1.5))

# JIRA -> Teams (horizontal on row 2 to row 2)
ax.annotate("Signed Tickets",
            xy=(teams_pos[0]-0.3, teams_pos[1]),
            xytext=(jira_pos[0]+0.4, jira_pos[1]),
            fontsize=8, ha="center",
            arrowprops=dict(arrowstyle="->", lw=1.5))

plt.show()