import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_task_reminder(task):
    """发送任务提醒邮件"""
    # 检查是否配置了邮件信息
    if not all(
        [
            os.getenv("MAIL_SERVER"),
            os.getenv("MAIL_PORT"),
            os.getenv("MAIL_USERNAME"),
            os.getenv("MAIL_PASSWORD"),
        ]
    ):
        return False, "Email configuration not complete"

    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg["From"] = os.getenv("MAIL_USERNAME")
        msg["To"] = os.getenv("MAIL_USERNAME")  # 发送给自己
        msg["Subject"] = f"Task Reminder: {task.title}"

        body = f"""
        Task Reminder:
        Title: {task.title}
        Description: {task.description or 'No description'}
        Priority: {task.priority}
        Completed: {'Yes' if task.completed else 'No'}
        """
        msg.attach(MIMEText(body, "plain"))

        # 发送邮件
        server = smtplib.SMTP(os.getenv("MAIL_SERVER"), os.getenv("MAIL_PORT"))
        server.starttls()
        server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
        text = msg.as_string()
        server.sendmail(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_USERNAME"), text)
        server.quit()

        return True, "Reminder email sent successfully"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
