import functions_framework
from flask import Flask, request, jsonify, make_response
from google.cloud import firestore

@functions_framework.http
def get_webpage_metrics(request):
  if request.method == 'OPTIONS':
    return handle_cors()

  data = create_webpage_metrics()
  return create_response(data)


def create_webpage_metrics():
  clicks = count_tracking_events('webpage_call')
  email_sent = count_tracking_events('email_sent')
  email_opened = count_tracking_events('email_opened') - count_tracking_events('email_sent') # the tracking pixel is triggered while sending mail
  emails_bttn_clicked = count_tracking_events('email_bttn_clicked')
  purchases = count_tracking_events('purchases_completed')
  avg_purchases_time = sum_up_purchase_time() / purchases if purchases > 0 else 0

  return {
    "clicks": clicks,
    "mailsSent": email_sent,
    "openedMails": email_opened,
    "clickedMails": emails_bttn_clicked,
    "purchases": purchases,
    "avgPurchaseTime": avg_purchases_time,
  }


def count_tracking_events(event_name):
  db = firestore.Client(database='marketing-campaign')
  docs_ref = db.collection('tracking')
  query = (docs_ref
           .where('event', '==', event_name))

  results = query.stream()
  count = sum(1 for _ in results)

  return count

def sum_up_purchase_time():
  db = firestore.Client(database='marketing-campaign')
  docs_ref = db.collection('tracking')
  query = (docs_ref
           .where('event', '==', 'purchases_completed'))

  results = query.stream()
  total_time = sum(doc.to_dict().get('time', 0) for doc in results)

  return total_time


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
