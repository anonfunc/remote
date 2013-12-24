from bottle import route, run

import harmony.util
import pyroku
import requests

from remote import config

@route('/hello')
def hello():
  return "Hello World!"

harmony_client_obj = None
def harmony_client():
  global harmony_client_obj
  if harmony_client_obj is None:
    harmony_client_obj = harmony.util.get_client(config.harmony_ip,
                                             config.harmony_port,
                                             config.harmony_email,
                                             config.harmony_password)
  return harmony_client_obj

roku_client = pyroku.Roku(config.roku_ip)

@route('/harmony')
def harmony_index():
  return "config, activity"

@route('/harmony/config')
def harmony_config():
  import pprint
  return pprint.pformat(harmony_client().get_config(), width=200)

@route('/harmony/activity')
@route('/harmony/activities')
def harmony_activity():
  config = harmony_client().get_config()
  activities = config['activity']
  return dict((a['label'], a['id']) for a in activities)

@route('/harmony/activity/<id>')
@route('/harmony/activities/<id>')
def harmony_activity_start(id):
  current = harmony_client().get_current_activity()
  if str(current) != str(id):
    print "Current activity is %s, want %s"
    return harmony_client().start_activity(id)
  else:
    return "Current activity is already %s" % id

@route('/roku')
def roku():
  return 'channels'

@route('/roku/channel')
@route('/roku/channels')
def roku():
  return requests.get('http://' + roku_client.roku_address + "/query/apps")

@route('/roku/channel/<id>')
@route('/roku/channels/<id>')
def roku_launch(id):
  return requests.post('http://' + roku_client.roku_address + "/launch/" + id)

try:
  run(host='0.0.0.0', port=9090, debug=True)
finally:
  harmony_client.disconnect()

