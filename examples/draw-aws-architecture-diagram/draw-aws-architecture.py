import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Define colors and styles
box_style = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgray")

# AWS Services Boxes
components = {
    "Amazon S3": (1, 8),
    "AWS Lambda\n'Parser'": (3, 8),
    "Amazon DynamoDB\nor RDS": (5, 8),
    "AWS Lambda\n'Comparer'": (7, 8),
    "JIRA (External)": (9, 8),
    "AWS Lambda\n'TicketStatusCheck'": (7, 5),
}

# Draw AWS components
for text, (x, y) in components.items():
    ax.text(x, y, text, ha="center", va="center", fontsize=10,
            bbox=box_style)

# Arrows representing data flow
arrows = [
    ((1.8, 8), (2.2, 8), "CSV"),
    ((3.8, 8), (4.2, 8), "Parse & Split"),
    ((5.8, 8), (6.2, 8), "Store QID"),
    ((7.8, 8), (8.2, 8), "Compare & Identify Diff"),
    ((9, 7.7), (9, 6.3), "Call JIRA"),
    ((9, 5.7), (9, 5.3), "Webhook/Poll"),
    ((8.2, 5), (7.8, 5), "Check Ticket Status"),
    ((7, 4.3), (7, 3.7), "Update DB or S3"),
]

# Draw arrows
for (x1, y1), (x2, y2), label in arrows:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, label,
            ha="center", va="center", fontsize=8, color="black")

# Display the architecture diagram
plt.show()