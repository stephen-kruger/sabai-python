from http.client import HTTPConnection
from base64 import b64encode
from sabai_state import SabaiState

class Sabai_api:
    username = "admin"
    password = "sabaipass123"
    uri = "192.168.199.1"
    updateOffset = "/s_sabaigw.cgi"

    # ###################################################################
    # Get the list of status objects
    # ###################################################################
    def get_api(self):
        print("Connecting to router on {} as {}".format(self.uri, self.username));
        deviceListOffset = "/sabai-gw.asp"

        #This sets up the https connection
        connection = HTTPConnection(self.uri)
        #then connect
        headers = { 'Authorization' : self.basic_auth(self.username, self.password) }
        connection.request('GET', deviceListOffset, headers=headers)

        try:
            #get the response back
            response = connection.getresponse()
            print("Status: {} and reason: {}".format(response.status, response.reason))
            # at this point you could check the status etc
            # this gets the page text
            if (response.status==200):
                data = response.read()
                # create the SabaiState object from the html response
                # print(data);
                return Sabai_api.getSabaiStateFromResponse(data)
            else:
                print("something bad happened")
        except Exception as e:
           print(e)

    # ###################################################################
    # Authorization token: we need to base 64 encode it
    # and then decode it to acsii as python 3 stores it as a byte string
    # ###################################################################
    def basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    # ###################################################################
    # Grep the html response and pull out the data we need to construct
    # a normalised view of the state objects
    # ###################################################################
    def getSabaiStateFromResponse(response):
        #arp ----------------
        thing = "arplist";
        # convert javascript quotes to something json can digest
        arpString = Sabai_api.getArray(thing+" = ",";", response).replace("'", "\"");

        # dhcpd static ----------------
        thing = "dhcpd_static";
        dhcpdStaticString = Sabai_api.getArray(thing+" = ",";", response)
        dhcpdStaticString = dhcpdStaticString[1:dhcpdStaticString.index("'.split('")];

        # wldev ----------------
        # thing = "wldev";

        # dhcpd lease ----------------
        thing = "dhcpd_lease";
        dhcpdLeaseString = Sabai_api.getArray(thing+" = ",";", response).replace("'", "\"");

        return SabaiState(arpString, dhcpdStaticString, dhcpdLeaseString)
    
    # ###################################################################
    def getArray(startStr, endStr, response):
        decodedStr = response.decode() 
        start = decodedStr.index(startStr)+len(startStr)
        end = decodedStr.index(endStr, start)
        return decodedStr[start:end]

#ss = SabaiState()

#obj = Sabai_api()
#obj.get_api()
sabaiState = Sabai_api().get_api()
for state in sabaiState.entries:
    print("mac={} name={} assignment={}".format(state.mac,state.name,state.assignment.name))
