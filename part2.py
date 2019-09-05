import requests
import random
import time
import uuid
import sys
import re
username = 'qz2190'
password = 'NVo6U2'
request_id = 'awgaawefwef'
cancel_id = 'awefawefwafdv'
slot_id = '0'
headers = {'Content-Type': 'application/xml', 'Accept' : 'application/xml'} # set what server accepts
xml = ''
recieved = ''
recieved_get = ''

######################################################################
# Form the XML structures
def form_reserve_xml(request_id, username, password, slot_id):
    global xml

    # Form the XML structure for the reserve request
    xml = """<?xml version='1.0' encoding='ASCII'?>
   <reserve>
       <request_id>""" + request_id + """</request_id>
       <username>""" + username + """</username>
       <password>""" + password + """</password>
       <slot_id>""" + slot_id + """</slot_id>
   </reserve>"""

    return xml

def form_cancel_xml(request_id, username, password, slot_id):
    global xml

    # Form the XML structure for the cancel request
    xml = """<?xml version='1.0' encoding='ASCII'?>
   <cancel>
       <request_id>""" + request_id + """</request_id>
       <username>""" + username + """</username>
       <password>""" + password + """</password>
       <slot_id>""" + slot_id + """</slot_id>
   </cancel>"""

    return xml

def form_available_xml(request_id, username, password):
    global xml

    # Form the XML structure for the check availability request
    xml_check_available = """<?xml version='1.0' encoding='utf-8'?>
   <availability>
       <request_id>""" + request_id + """</request_id>
       <username>""" + username + """</username>
       <password>""" + password + """</password>
   </availability>"""

    return xml

def form_bookings_xml(request_id, username, password):
    global xml
    # Form the XML structure for the check bookings request
    xml_check_bookings = """<?xml version='1.0' encoding='utf-8'?>
   <bookings >
       <request_id>""" + request_id + """</request_id>
       <username>""" + username + """</username>
       <password>""" + password + """</password>
   </bookings >"""
    return xml

######################################################################
# Reserve a slot
def reserve_hotel(username, password, request_id, slot_id):

    url = 'http://jewel.cs.man.ac.uk:3010/queue/enqueue'

    print("\nThe slot you want to reserve is " + slot_id )

    form_reserve_xml(request_id, username, password, slot_id)
    send_request(url)

    time.sleep(2)

    # Check the reservation
    recieved_url = recieved.strip('<msg_uri>').strip('</msg_uri>')
    get_response = recieved_url + '?username=' + username + '&password=' + password

    #print 'Merged server response URL with username and password: ' + get_response + '\n'
    print ('\nChecking status of reservation...')

    response_waiting(get_response)
    print ('\nResponse that is recieved from the server: \n' + recieved_get)
    status_hotel = re.findall('\d+',recieved_get)
    statu_hotel = status_hotel[0]
    print (statu_hotel)
    if statu_hotel == "200":
        print ("8888888888888888888888888888888888888888888888888888888888")

def reserve_band(username, password, request_id, slot_id):

    url = 'http://jewel.cs.man.ac.uk:3020/queue/enqueue'

    print("\nThe slot you want to reserve is " + slot_id )

    form_reserve_xml(request_id, username, password, slot_id)
    send_request(url)

    time.sleep(2)

    # Check the reservation
    recieved_url = recieved.strip('<msg_uri>').strip('</msg_uri>')
    get_response = recieved_url + '?username=' + username + '&password=' + password

    #print 'Merged server response URL with username and password: ' + get_response + '\n'
    print ('\nChecking status of reservation...')

    response_waiting(get_response)
    print ('\nResponse that is recieved from the server: \n' + recieved_get)
    status_band = re.findall('\d+',recieved_get)
    statu_band = status_band[0]
    print (statu_band)
    if statu_band == "200":
        print ("8888888888888888888888888888888888888888888888888888888888")
#############################################################################
# Cancel a slot
def cancel(username, password, request_id, slot_id):

    url = 'http://jewel.cs.man.ac.uk:3010/queue/enqueue'

    print("\nThe slot you want to cancel is " + slot_id )

    form_cancel_xml(request_id, username, password, slot_id)
    send_request(url)

    # Check the cancelation
    recieved_url = recieved.strip('<msg_uri>').strip('</msg_uri>')

    get_response = recieved_url + '?username=' + username + '&password=' + password

    #print 'Merged server response URL with username and password: ' + get_response + '\n'
    print ('\nChecking status of cancellation...')
    response_waiting(get_response)

    print ('\nResponse that is recieved from the server: \n' + recieved_get)



    url = 'http://jewel.cs.man.ac.uk:3020/queue/enqueue'
    print("\nThe slot you want to cancel is " + slot_id )
    form_cancel_xml(request_id, username, password, slot_id)
    send_request(url)

    # Check the cancelation
    recieved_url = recieved.strip('<msg_uri>').strip('</msg_uri>')

    get_response = recieved_url + '?username=' + username + '&password=' + password

    #print 'Merged server response URL with username and password: ' + get_response + '\n'
    print ('\nChecking status of cancellation...')
    response_waiting(get_response)

    print ('\nResponse that is recieved from the server: \n' + recieved_get)

#############################################################################
# Check bookings
def check_bookings(username, password, request_id):

    url = 'http://jewel.cs.man.ac.uk:3010/booking/'
    print("\nChecking bookings for you..")

    form_bookings_xml(request_id, username, password)

    recieved_bookings = requests.put(url, data=xml, headers=headers).text
    time.sleep(2)
    while recieved_bookings == 'Service Unavailable':
        print ('Service unavailable, retrying...')
        time.sleep(2)
        recieved_bookings = requests.put(url, data=xml, headers=headers).text

    # Check the bookings
    recieved_bookings_url = recieved_bookings.strip('<msg_uri>').strip('</msg_uri>')
    print (recieved_bookings_url)

# Check minimum slots
def check_available(username, password, request_id):
    global debug
    url1 = 'http://jewel.cs.man.ac.uk:3010/booking/available'
    url2 = 'http://jewel.cs.man.ac.uk:3020/booking/available'
    print("\nChecking availability...")

    form_available_xml(request_id, username, password)
    send_request(url1)
    recieve1 = re.findall('\d+',recieved)
    recieve1.pop(0)
    recieve1.pop(0)
    print(recieve1)
    send_request(url2)
    recieve2 = re.findall('\d+',recieved)
    recieve2.pop(0)
    recieve2.pop(0)
    print(recieve2)
    common = set(recieve1).intersection(recieve2)
    print (common)
    if not common:
        return int(1000)
    else:
        minimum_num = min(common)
        print (minimum_num)
        return int(minimum_num)


def printStats():
    print("\nYour username is " + username)
    print("Your password is " + password)
    print("Generated request ID: " + request_id)
    return

def send_request(url):
    global recieved, xml, headers
    # Reserve a slot
    recieved = requests.put(url, data=xml, headers=headers).text

    print ('Request sent...')
    print_warning = True

    while recieved == 'Service Unavailable':

        if print_warning:
            print ('\nService unavailable, retrying...')

        print_warning = False
        time.sleep(2)
        recieved = requests.put(url, data=xml, headers=headers).text

def response_waiting(get_response):
    global recieved_get
    print ('Waiting for response, might take a while...')
    recieved_get = requests.get(get_response).text
    time.sleep(2)

    while recieved_get == 'Message unavailable' or recieved_get == 'Service unavailable':
        time.sleep(2)
        recieved_get = requests.get(get_response).text

#---------------------------------------------------------
current = int(10000)
statu_hotel = "0"
statu_band = "0"
reserve_stat = 0
check_stat = 0
old = 0
while True:
	# while getlatest != current and hotel
	#    current = getlatest
	#    reserve current slotid for hotel
    #    reserve band
    time.sleep(1)
    print ("processing ......")
    request_id = str(uuid.uuid4())
    while check_available(username, password, request_id) < current or statu_hotel!="200" or statu_band!="200":
        # if check_available(username, password, request_id) < current:
        #     print("###########~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # if statu_hotel=="200":
        #     print ("awaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # if statu_band=="200":
        #    print ("awaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        if check_available(username, password, request_id) == 1000:
            print ('no slots are currently available qaq')
            check_stat = 1
            break
        check_stat = 0

        current = check_available(username, password, request_id)
        request_id = str(uuid.uuid4())
        reserve_hotel(username, password, request_id, str(current))
        request_id = str(uuid.uuid4())
        reserve_band(username, password, request_id, str(current))
        if reserve_stat == 1:
            request_id = str(uuid.uuid4())
            cancel(username, password, request_id, str(old))
    #two has been reserved or no available
    if check_stat != 1:
        reserve_stat = 1;
        old = current
        # print ("##########################success#######################")
