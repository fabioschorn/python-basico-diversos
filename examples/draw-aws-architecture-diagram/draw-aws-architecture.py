import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")

# Define colors and styles for AWS services
box_style = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
lambda_color = "#F58536"  # AWS Lambda color
db_color = "#527FFF"  # AWS RDS/DynamoDB color
s3_color = "#569A31"  # AWS S3 color
jira_color = "#0052CC"  # JIRA color

# Define positions for AWS services
components = {
    "Amazon S3": (1, 6, s3_color),
    "AWS Lambda 'Parser'": (3, 6, lambda_color),
    "Amazon DynamoDB / RDS": (5, 6, db_color),
    "AWS Lambda 'Comparer'": (7, 6, lambda_color),
    "JIRA (External)": (9, 6, jira_color),
    "AWS Lambda 'TicketStatusCheck'": (7, 3, lambda_color),
}

# Draw AWS components
for text, (x, y, color) in components.items():
    ax.text(x, y, text, ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor=color, alpha=0.7))

# Draw arrows for data flow
arrows = [
    ((1.8, 6), (2.2, 6), "(1) CSV"),
    ((3.8, 6), (4.2, 6), "(2) Parse & Split"),
    ((5.8, 6), (6.2, 6), "(3) Store QID"),
    ((7.8, 6), (8.2, 6), "(4) Compare & Identify Diff"),
    ((9, 5.5), (9, 4.5), "(5) Call JIRA"),
    ((9, 3.5), (9, 3), "Webhook / Poll"),
    ((8.2, 3), (7.8, 3), "(6) If Ticket Closed"),
    ((7, 2.5), (7, 2), "Update DB or S3"),
]

# Draw arrows
for (x1, y1), (x2, y2), label in arrows:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, label,
            ha="center", va="center", fontsize=8, color="black")

# Draw enclosing AWS Cloud Box
aws_box = mpatches.FancyBboxPatch((0.5, 1.5), 9, 6.5, boxstyle="round,pad=0.3",
                                  edgecolor="black", facecolor="lightgray", alpha=0.3)
ax.add_patch(aws_box)
ax.text(5, 7.5, "AWS Cloud", ha="center", va="center", fontsize=12, fontweight="bold")

# Show final architecture diagram
plt.show()