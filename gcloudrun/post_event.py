import functions_framework
from flask import Flask, request, jsonify, make_response
from google.cloud import firestore
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

load_dotenv()

@functions_framework.http
def post_event(request):
  if request.method == 'OPTIONS':
    return handle_cors()

  event = request.get_json()
  campaigns = create_campaigns(event)
  add_event(event, campaigns)

  for c in campaigns:
    send_emails(c)
    c['recipients'] = len(c['recipients'])
  return create_response({ 'campaigns': campaigns})


def add_event(event_data, campaigns):
  campaign_ids = [campaign["id"] for campaign in campaigns]
  event_data['campaigns'] = campaign_ids

  db = firestore.Client(database='marketing-campaign')
  db.collection('events').add(event_data)


def create_campaigns(event):
  campaign_a, campaign_b = call_gemini(event)
  group_a, group_b = split_users()
  result = []
  result.append(add_campaign(campaign_a, group_a))
  result.append(add_campaign(campaign_b, group_b))
  return result


def add_campaign(campaign, group):
  db = firestore.Client(database='marketing-campaign')
  doc_ref = db.collection('marketing-campaign').document()
  data = {
    'id': doc_ref.id,
    'name': campaign['name'],
    'variant': campaign['variant'],
    'subjectLine': campaign['subjectLine'],
    'content': campaign['content'],
    'recipients': group
  }
  doc_ref.set(data)
  return data

def call_gemini(event):
  # generation_config = {"temperature":0.4, "top_p":1.0, "top_k":32, "max_output_tokens":2048}
  genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
  model = genai.GenerativeModel("gemini-1.5-pro-001")
  prompt = f"""
    You are a professional email copywriter for a high-performing e-commerce store. Your goal is to craft two compelling marketing emails that maximize engagement and boost sales.
    An email campaign is scheduled for the event: "{event['description']}", on {event['date']}.

    Task: Write two distinct email variants (A and B), each with a catchy subject line and a well-structured HTML email body.

    Requirements:
    - The user should be addressed as <USER-NAME> (this placeholder will be replaced dynamically). Do not use any other placeholders.
    - Start each email with an <h2> headline that captures attention.
    - Include the following call-to-action link embedded in a HTML button or styled link tag: https://stephaniehhnbrg.github.io/ai-hackfest-webstore/
    - The tone should be exciting, friendly, and persuasive, encouraging the user to engage or make a purchase.

    Output format:
    Return your response as raw JSON with the following fields
    - campaign_name
    - subject_line_A
    - mail_body_A
    - subject_line_B
    - mail_body_B

    Do not frame your response with ```json and do not use \\n or markdown to format it.
  """

  response = model.generate_content(prompt)

  json_string = response.candidates[0].content.parts[0].text
  print(json_string)
  data = json.loads(json_string)
  campaign_a = {
    'name': data['campaign_name'],
    'variant': 'A',
    'subjectLine': data['subject_line_A'],
    'content': data['mail_body_A']
  }
  campaign_b = {
    'name': data['campaign_name'],
    'variant': 'B',
    'subjectLine': data['subject_line_B'],
    'content': data['mail_body_B']
  }

  print("Generated campaign:", data['campaign_name'])
  return campaign_a, campaign_b


def split_users():
  db = firestore.Client(database='marketing-campaign')
  docs = db.collection('users').stream()

  mails = []
  for doc in docs:
    data = doc.to_dict()
    mails.append({"mail": data.get("mail"), "name": data.get("name")})
  random.shuffle(mails)

  mid = len(mails)
  group_a = mails[:mid]
  group_b = mails[mid:]

  return group_a, group_b


def send_emails(campaign):
  from_mail = os.environ.get("SENDER_MAIL")
  from_password = os.environ.get("SENDER_MAIL_PW")

  msg = MIMEMultipart()
  msg['From'] = from_mail
  msg['Subject'] = campaign['subjectLine']
  html_body = f"""
  <html>
    <body>
      <div>{campaign['content']}</div>
      <img src="https://track-pixel-mwc2mmip4a-ey.a.run.app?user_id=<USER-ID>&campaign_id={campaign['id']}" width="1" height="1" style="display:none;" />
    </body>
  </html>
  """
  link = f"https://stephaniehhnbrg.github.io/ai-hackfest-webstore/?utm_campaign={campaign['id']}&utm_user_id=<USER-ID>"
  html_body = html_body.replace("https://stephaniehhnbrg.github.io/ai-hackfest-webstore/", link)
  msg.attach(MIMEText(html_body, 'html'))

  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_mail, from_password)

    for user_data in campaign['recipients']:
      msg['To'] = user_data['mail']
      mail_body = msg.as_string().replace("<USER-NAME>", user_data['name']).replace("<USER-ID>", user_data['mail'])
      server.sendmail(from_mail, user_data['mail'], mail_body)
      update_tracking_db(user_data['mail'], campaign['id'])

  except Exception as e:
    print(f"Error: {e}")

  finally:
    server.quit()


def update_tracking_db(user_id, campaign_id):
  db = firestore.Client(database='marketing-campaign')
  db.collection('tracking').add({
    "user_id": user_id,
    "campaign_id": campaign_id,
    "event": "email_sent",
    "timestamp": firestore.SERVER_TIMESTAMP
  })


ALLOWED_ORIGINS = [
  'http://localhost:4200',
  'https://stephaniehhnbrg.github.io'
]


def handle_cors():
  response = make_response()
  response.status_code = 204
  for origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
  response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  return response


def create_response(data):
  response = make_response(jsonify(data))
  response.status_code = 200
  for origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
  return response

