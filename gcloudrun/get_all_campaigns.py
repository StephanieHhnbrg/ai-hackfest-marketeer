import functions_framework
from flask import Flask, request, jsonify, make_response
from google.cloud import firestore

@functions_framework.http
def get_all_campaigns(request):
  if request.method == 'OPTIONS':
    return handle_cors()

  data = fetch_data()
  return create_response(data)


def fetch_data():
  db = firestore.Client(database='marketing-campaign')
  docs = db.collection('marketing-campaign').stream()

  result = []
  for doc in docs:
    data = doc.to_dict()
    data['recipients'] = len(data['recipients'])
    data['purchases'] = count_tracking_events(data['id'], 'purchases_completed')
    data['clicks'] = count_tracking_events(data['id'], 'email_bttn_clicked')
    result.append(data)
  return result


def count_tracking_events(campaign_id, event_name):
  db = firestore.Client(database='marketing-campaign')
  docs_ref = db.collection('tracking')
  query = (docs_ref
           .where('campaign_id', '==', campaign_id)
           .where('event', '==', event_name))

  results = query.stream()
  count = sum(1 for _ in results)

  return count

def handle_cors():
  response = make_response()
  response.status_code = 204
  response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
  response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  return response


def create_response(data):
  response = make_response(jsonify(data))
  response.status_code = 200
  response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
  return response
