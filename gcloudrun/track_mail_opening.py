import functions_framework
from flask import Flask, request, send_file
from google.cloud import firestore
import io

@functions_framework.http
def track_pixel(request):
  if request.method == 'OPTIONS':
    return createTransparentImg()

  track_user(request)
  return createTransparentImg()


def track_user(request):
  request_json = request.get_json(silent=True)
  request_args = request.args
  user_id = get_field_from_req(request_json, request_args, 'user_id')
  campaign_id = get_field_from_req(request_json, request_args, 'campaign_id')


  db = firestore.Client(database='marketing-campaign')
  db.collection('tracking').add({
    "user_id": user_id,
    "campaign_id": campaign_id,
    "event": "email_opened",
    "timestamp": firestore.SERVER_TIMESTAMP
  })


def get_field_from_req(request_json, request_args, field):
  if request_json and field in request_json:
    return request_json[field]
  elif request_args and field in request_args:
    return request_args[field]
  else:
    return ""


def createTransparentImg():
  pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00' \
          b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00' \
          b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
  return send_file(io.BytesIO(pixel), mimetype='image/gif')
