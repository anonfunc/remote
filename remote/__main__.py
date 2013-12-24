import os

from bottle import route, run, request, abort, static_file, view
import bottle
import harmony.util
import pyroku
import requests

from soco import SoCo
from soco import SonosDiscovery

from remote import config

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'views'))

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

@route('/')
@view('index')
def index():
  return dict()

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
  return 'channels, press/button, type/string'

@route('/roku/channel')
@route('/roku/channels')
def roku():
  return requests.get('http://' + roku_client.roku_address + "/query/apps")

@route('/roku/channel/<id>')
@route('/roku/channels/<id>')
def roku_launch(id):
  return requests.post('http://' + roku_client.roku_address + "/launch/" + id)

@route('/roku/press')
def roku_press_index():
  return """
Home
Rev
Fwd
Play
Select
Left
Right
Down
Up
Back
InstantReplay
Info
Backspace
Search
Enter
Lit_*"""

@route('/roku/press/<button>')
def roku_press(button):
  roku_client.keypress(button)

@route('/roku/type/<string>')
def roku_press(string):
  buttons = [ 'Ltr_' + ch for ch in string ]
  for button in buttons:
    roku_client.keypress(button)

@route('/sonos')
def sonos_view():
  speakers = {}
  sonos_devices = SonosDiscovery()
  for ip in sonos_devices.get_speaker_ips():
    device = SoCo(ip)
    info = device.get_speaker_info()
    info['ip'] = ip
    zone_name = info.get('zone_name', None)
    if zone_name is not None:
      speakers[zone_name] = info
  return speakers

@route('/sonos/<ip>')
def sonos_view(ip):
  device = SoCo(ip)
  info = device.get_speaker_info()
  info['ip'] = ip
  return info

@route('/sonos/<ip>/volume')
def sonos_volume(ip):
  device = SoCo(ip)
  val = request.query.val
  if val:
    try:
      val = int(val)
    except:
      abort(500, "Bad value")
    return device.volume(val)
  else:
    return str(device.volume())

#@route('/sonos/<ip>/<method_name>')
#def sonos_method(ip, method_name):
  #device = SoCo(ip)
  #method = getattr(device, method_name)
  #result = method()
  #return result

@route('/static/<filepath:path>')
def server_static(filepath):
  module_dir = os.path.dirname(__file__)
  return static_file(filepath, root=os.path.join(module_dir, 'static'))

@route('/bower_components/<filepath:path>')
def bower_static(filepath):
  module_dir = os.path.dirname(__file__)
  bower_dir = os.path.abspath(os.path.join(module_dir, '..', 'bower_components'))
  return static_file(filepath, root=bower_dir)

try:
  run(host='0.0.0.0', port=9090, debug=True, reloader=True)
finally:
  if harmony_client_obj is not None:
    harmony_client().disconnect()
