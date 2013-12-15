from bottle import route, run

import harmony.util

from remote import config

@route('/hello')
def hello():
  return "Hello World!"

harmony_client = harmony.util.get_client(config.harmony_ip,
                                         config.harmony_port,
                                         config.harmony_email,
                                         config.harmony_password)

@route('/harmony')
def harmony():
  return "config, activity"

@route('/harmony/config')
def harmony_config():
  import pprint
  return pprint.pformat(harmony_client.get_config(), width=200)

@route('/harmony/activity')
@route('/harmony/activities')
def harmony_activity():
  config = harmony_client.get_config()
  activities = config['activity']
  return dict((a['label'], a['id']) for a in activities)

@route('/harmony/activity/<id>')
@route('/harmony/activities/<id>')
def harmony_activity_start(id):
  return harmony_client.start_activity(id)

try:
  run(host='localhost', port=8080, debug=True)
finally:
  harmony_client.disconnect()

