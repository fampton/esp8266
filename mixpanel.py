import urequests

headers = {'Authorization':'Basic <b64encoded (api_key + colon)>'}

event = "Call Ended"

def main(datestring):
  r = urequests.get('https://mixpanel.com/api/2.0/events?interval=1&type=general&event=%5B%22Call+Ended%22%5D&unit=day', headers=headers)
  json_response = r.json()
  calls = json_response['data']['values'][event]
  #today = list(calls.values())[1]
  today = calls[datestring]
  return today

if __name__ == '__main__':
    main()
