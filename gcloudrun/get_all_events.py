import functions_framework
from flask import Flask, request, jsonify, make_response
from google.cloud import firestore

@functions_framework.http
def get_all_events(request):
  if request.method == 'OPTIONS':
    return handle_cors(request)

  data = fetch_data()
  return create_response(data, request)


def fetch_data():
  db = firestore.Client(database='marketing-campaign')
  docs = db.collection('events').stream()

  result = []
  for doc in docs:
    data = doc.to_dict()
    campaign_ids = data.get('campaigns', [])
    campaign_names = [fetch_campaign_name(campaign_id) for campaign_id in campaign_ids]
    data['campaigns'] = campaign_names
    result.append(data)
  return result

def fetch_campaign_name(id):
  db = firestore.Client(database='marketing-campaign')
  docs_ref = db.collection('marketing-campaign')
  doc = docs_ref.document(id).get()

  if doc.exists:
    data = doc.to_dict()
    return f"{data.get('name')}_{data.get('variant')}"
  else:
    return 'Campaign not found'


ALLOWED_ORIGINS = [
  'http://localhost:4200',
  'https://stephaniehhnbrg.github.io'
]


def handle_cors(request):
  response = make_response()
  response.status_code = 204
  origin = request.headers.get('Origin')
  if origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
  response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  return response


def create_response(data, request):
  response = make_response(jsonify(data))
  response.status_code = 200
  origin = request.headers.get('Origin')
  if origin in ALLOWED_ORIGINS:
    response.headers['Access-Control-Allow-Origin'] = origin
  return response

