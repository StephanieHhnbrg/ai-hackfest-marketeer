import functions_framework
from flask import Flask, request, jsonify, make_response
from google.cloud import firestore

@functions_framework.http
def get_all_events(request):
  if request.method == 'OPTIONS':
    return handle_cors()

  data = fetch_data()
  return create_response(data)


def fetch_data():
  db = firestore.Client(database='marketing-campaign')
  docs = db.collection('events').stream()

  result = []
  for doc in docs:
    data = doc.to_dict()
    result.append(data)
  return result

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
