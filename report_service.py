
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_task_report(tasks):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "AI Task Assistant - Task Report")
    y -= 45

    pdf.setFont("Helvetica", 11)

    for task in tasks:
        if y < 70:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50

        status = "Completed" if task.completed else "Pending"

        title = task.title[:75]
        line = f"#{task.id} | {title} | {status}"

        pdf.drawString(50, y, line)
        y -= 25

    if not tasks:
        pdf.drawString(50, y, "No tasks available.")

    pdf.save()
    buffer.seek(0)

    return buffer
