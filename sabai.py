from http.client import HTTPConnection
from base64 import b64encode
from sabai_state import SabaiState

import requests
from requests.auth import HTTPBasicAuth

class Sabai_api:
    username = "admin"
    password = "sabaipass123"
    uri = "192.168.199.1"

    # ###################################################################
    # Get the list of status objects
    # ###################################################################
    def get_Network_Gateways(self):
        print("Connecting to router on {} as {}".format(self.uri, self.username));
        deviceListOffset = "/sabai-gw.asp"

        #This sets up the https connection
        connection = HTTPConnection(self.uri,timeout=5)
        #then connect
        headers = { 'Authorization' : self.basic_auth(self.username, self.password) }

        try:
            connection.request('GET', deviceListOffset, headers=headers)
            response = connection.getresponse()
            if (response.status==200):
                data = response.read()
                # create the SabaiState object from the html response
                return Sabai_api.getSabaiStateFromResponse(data)
            else:
                print("Server reported : {} {}".format(response.status, response.reason))
                return SabaiState("","","")
        except Exception as e:
           print("Failed to connect :"+str(e))
           return SabaiState("","","")
        finally:  # always close the connection
            connection.close()


    def set_Network_Gateways(self, sabaiState):
        updateOffset = "/s_sabaigw.cgi"
        headers = { 
            'Accept' : '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language':'en-IE,en-US;q=0.9,en;q=0.8',
            'Cookie':'tomato_status_overview_refresh=0',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Content-Type': 'text/plain;charset=UTF-8'
        }
        pload = {
            "gw_def":"0",
            "mimeType": "text/plain;charset=UTF-8",
            "text": "gw_def=1&dhcpd_static=00:01:2E:A0:BE:CD<192.168.199.2<vpna<0<1>58:85:E9:F3:16:FB<192.168.199.167<realme-X2<0<3>F8:FF:C2:05:A0:29<192.168.199.222<Stephens-MBP<0<0>98:F7:81:7C:45:3E<192.168.199.78<<0<0>AC:9B:0A:10:4C:8C<192.168.199.240<android-96237537fe2ef76e<0<0>DE:72:65:0C:E9:B5<192.168.199.34<Karine-s-Galaxy-S20-FE<0<3>82:B2:C9:80:21:C7<192.168.199.248<realme-3<0<0>58:85:E9:73:16:FB<192.168.199.168<<0<0>C4:DD:57:1F:64:5B<192.168.199.19<ESP_1F645B<0<1>B0:DE:28:0E:48:A0<192.168.199.169<Stephens-MBP1<0<0>&_http_id=TIDe8e95ecea97b0c7"
        }
        curr_url = 'http://'+self.uri+updateOffset
        print("`Connecting to "+curr_url)
        try:
            r = requests.post(curr_url,auth=(self.username, self.password),data=str(pload), headers=headers)
        except Exception as e:
            print("Failed to connect :"+str(e))
        
    # ###################################################################
    # Set the list of status objects
    # ###################################################################
    def set_Network_GatewaysXXX(self, sabaiState):
        updateOffset = "/s_sabaigw.cgi"
        print("Connecting to router on {}{} as {}".format(self.uri, updateOffset, self.username) )

        #This sets up the https connection
        connection = HTTPConnection(host=self.uri,timeout=5)
        #then connect
        headers = { 
            'Accept' : '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language':'en-IE,en-US;q=0.9,en;q=0.8',
            'Cookie':'tomato_status_overview_refresh=0',
            'Authorization' : self.basic_auth(self.username, self.password) ,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Content-Type': 'text/plain;charset=UTF-8',
            "Origin":"http://192.168.199.1",
            "Referer": "http://192.168.199.1/sabai-gw.asp"
        }
        body = {
            "gw_def":"0",
            "mimeType": "text/plain;charset=UTF-8",
            "text": "gw_def=1&dhcpd_static=00:01:2E:A0:BE:CD<192.168.199.2<vpna<0<1>58:85:E9:F3:16:FB<192.168.199.167<realme-X2<0<3>F8:FF:C2:05:A0:29<192.168.199.222<Stephens-MBP<0<0>98:F7:81:7C:45:3E<192.168.199.78<<0<0>AC:9B:0A:10:4C:8C<192.168.199.240<android-96237537fe2ef76e<0<0>DE:72:65:0C:E9:B5<192.168.199.34<Karine-s-Galaxy-S20-FE<0<3>82:B2:C9:80:21:C7<192.168.199.248<realme-3<0<0>58:85:E9:73:16:FB<192.168.199.168<<0<0>C4:DD:57:1F:64:5B<192.168.199.19<ESP_1F645B<0<1>B0:DE:28:0E:48:A0<192.168.199.169<Stephens-MBP1<0<0>&_http_id=TIDe8e95ecea97b0c7"
        }
        #body = body.encode("utf-8")
        try:
            print("0>>>>>>>>>>>>>"+'http://'+self.uri+updateOffset)
            connection.request(method="POST",url='http://'+self.uri+updateOffset, body=body, headers=headers)
            print("1>>>>>>>>>>>>>")
            response = connection.getresponse()
            print("2>>>>>>>>>>>>>"+str(response))
            if (response.status==200):
                data = response.read()
                # create the SabaiState object from the html response
                #return Sabai_api.getSabaiStateFromResponse(data)
            else:
                print("Server reported : {} {}".format(response.status, response.reason))
                # return SabaiState("","","")
        except Exception as e:
            print("Failed to connect :"+str(e))
            # return SabaiState("","","")
        finally:  # always close the connection
            connection.close()


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

sabaiState = Sabai_api().get_Network_Gateways()
for state in sabaiState.entries:
    print("mac={} name={} assignment={}".format(state.mac,state.name,state.assignment.name))
#Sabai_api().set_Network_Gateways(sabaiState)
#Sabai_api().set_Network_Gateways(SabaiState("","",""))
