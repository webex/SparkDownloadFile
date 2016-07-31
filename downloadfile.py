from itty import *
import urllib2
import json

def sendSparkGET(url):
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request)
    return contents


@post('/')
def index(request):
    webhook = json.loads(request.body)
    if webhook['data'].has_key('files'):
        for file_url in webhook['data']['files']:
            response = sendSparkGET(file_url)
            content_disp = response.headers.get('Content-Disposition', None)
            if content_disp is not None:
                filename = content_disp.split("filename=")[1]#split on the string "filename=", then save the second item as name
                filename = filename.replace('"', '')
                with open(filename, 'w') as f:
                    f.write(response.read())
                    print 'Saved-', filename
            else:
                print "Cannot save file- no Content-Disposition header received."
    else:
        print "No files attached to retrieve!"
    return "true"


####CHANGE THIS VALUE#####
bearer = "BOT_TOKEN_HERE"

run_itty(server='wsgiref', host='0.0.0.0', port=10002)