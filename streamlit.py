import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import imghdr
import os

# Function to send email
def send_email(receiver_email, subject, body, file_paths):
    sender_name = "LotharsApp.com"
    sender_email = "streamlitt@gmail.com"  # Update with your email address
    sender_password = "qias amqt donl wvgk"  # Update with your email password
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in file_paths:
        file_type_info = imghdr.what(file_path) if os.path.isfile(file_path) else (None, None)
        file_type = file_type_info[0] if file_type_info else None

        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        if file_type:
            part.add_header("Content-Type", f"image/{file_type}")

        msg.attach(part)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

# Streamlit app
def main():
    st.title("File Sharing System")
    st.markdown("<h1 style='font-size:24px; font-style: italic;'>Author: Lothar Tjipueja</h1>", unsafe_allow_html=True)
    st.write("Drag and drop files here:")

    files = st.file_uploader("Upload Files", type=['csv', 'xlsx', 'jpg', 'jpeg', 'png', 'mp4'], accept_multiple_files=True)

    if files:
        st.success("Files Uploaded Successfully!")

        email = st.text_input("Enter Receiver's Email")
        subject = st.text_input("Enter Email Subject", "File Sharing")
        body = st.text_area("Enter Email Body")

        send_button = st.button("Send Email")

        if send_button:
            if email == "":
                st.warning("Please enter an email address.")
            else:
                file_paths = [f"./{file.name}" for file in files]
                for file, file_path in zip(files, file_paths):
                    with open(file_path, "wb") as f:
                        f.write(file.getvalue())

                send_email(email, subject, body, file_paths)
                st.success(f"Email sent successfully to {email}!")

                # Remove the files after sending
                for file_path in file_paths:
                    os.remove(file_path)

                # Ask the user if they want to refresh the page
                if st.button("Refresh Page"):
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
