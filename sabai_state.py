from dhcpd_static import DhcpdStatic
from assignment import Assignment
from sabai_entry import SabaiEntry
from dhcpd_lease import DhcpdLease
import json

class SabaiState:
    # array of SabaiEntry objects
    entries = []

    # ###################################################################
    # constructor
    # ###################################################################
    def __init__(self, arpString, dhcpdStaticString, dhcpdLeaseString):
            #print(dhcpdStaticString)
            #print(dhcpdLeaseString)
            # dhcpd static ----------------
            dhcpdStaticList = []
            elements = dhcpdStaticString.split(">")
            for element in elements:
                if (len(element)>0):
                    dhcpdStaticList.append(DhcpdStatic(element))

            # wldev ----------------
            # todo

            # arp ----------------
            # todo

            # dhcpd lease ----------------
            dhcpdLeaseList = []
            dhcpdLeaseString = dhcpdLeaseString.replace("'","\"")
            jdata = json.loads(dhcpdLeaseString)
            for element in jdata:
                dhcpdLeaseList.append(DhcpdLease(element))

            # now create a giant SabaiState object
            states = []
            for dhcpLeaseElement in dhcpdLeaseList:
                entry = SabaiEntry(dhcpLeaseElement.mac, dhcpLeaseElement.ip, dhcpLeaseElement.name, Assignment.UNKNOWN);
                #print(">>>>>"+entry.mac)
                self.updateState(states,entry)
            #

            for dhcpStaticElement in dhcpdStaticList:
                entry = SabaiEntry(dhcpStaticElement.mac, dhcpStaticElement.ip, dhcpStaticElement.name, dhcpStaticElement.assignment);
                #print(">>>>>"+entry.mac)
                self.updateState(states,entry);
            
            self.entries = []
            for state in states:
                self.entries.append(state)
            

    # ###################################################################
    def updateState(self, sabaiStates, sabaiEntry):
        found = False
        for sabaiState in sabaiStates:
            if (sabaiState.mac == sabaiEntry.mac):
                if len(sabaiState.name)==0:
                    sabaiState.name = sabaiEntry.name
                if sabaiState.assignment==Assignment.UNKNOWN:
                    sabaiState.assignment = sabaiEntry.assignment
                found = True

        if found!=True:
            sabaiStates.append(sabaiEntry)


    # ###################################################################
    def getArray(self, startStr, endStr, str):
        start = str.index(startStr)+len(startStr)
        end = str.index(endStr, start)
        return str[start: end]
    
    # ###################################################################
    def testState():
        arpString = "[ ['192.168.199.92','10:96:93:D3:A1:EC','br0'],['192.168.199.34','DE:72:65:0C:E9:B5','br0'],['192.168.199.56','D0:57:7B:77:E4:9E','br0'],['192.168.199.2','00:01:2E:A0:BE:CD','br0'],['192.168.199.159','10:5A:17:8F:46:B8','br0'],['192.168.70.254','98:86:5D:A2:F1:D4','vlan2'],['192.168.199.169','B0:DE:28:0E:48:A0','br0'],['192.168.199.19','C4:DD:57:1F:64:5B','br0']]"
        dhcpdStaticString = "00:01:2E:A0:BE:CD<192.168.199.2<vpna<0<1>58:85:E9:F3:16:FB<192.168.199.167<realme-X2<0<3>F8:FF:C2:05:A0:29<192.168.199.222<Stephens-MBP<0<0>98:F7:81:7C:45:3E<192.168.199.78<<0<0>AC:9B:0A:10:4C:8C<192.168.199.240<android-96237537fe2ef76e<0<0>DE:72:65:0C:E9:B5<192.168.199.34<Karine-s-Galaxy-S20-FE<0<3>82:B2:C9:80:21:C7<192.168.199.248<realme-3<0<1>58:85:E9:73:16:FB<192.168.199.168<<0<0>C4:DD:57:1F:64:5B<192.168.199.19<ESP_1F645B<0<1>D0:57:7B:77:E4:9E<192.168.199.56<lhubert-GL702VM<0<1>"
        dhcpdLeaseString = "[['Stephens-MBP','192.168.199.169','B0:DE:28:0E:48:A0','0 days, 23:47:57'],['','192.168.199.83','40:A9:CF:54:5E:38','0 days, 03:50:37'],['Karine-s-Galaxy-S20-FE','192.168.199.34','DE:72:65:0C:E9:B5','0 days, 00:00:00'],['ESP_1F645B','192.168.199.19','C4:DD:57:1F:64:5B','0 days, 00:00:00'],['','192.168.199.92','10:96:93:D3:A1:EC','0 days, 23:20:03'],['realme-X2','192.168.199.167','58:85:E9:F3:16:FB','0 days, 00:00:00'],['wlan0','192.168.199.159','10:5A:17:8F:46:B8','0 days, 19:19:42'],['vpna','192.168.199.2','00:01:2E:A0:BE:CD','0 days, 00:00:00'],['','192.168.199.109','5E:47:E6:EE:AE:DF','0 days, 00:30:58'],['lhubert-GL702VM','192.168.199.56','D0:57:7B:77:E4:9E','0 days, 18:26:51'],['Galaxy-A32-5G','192.168.199.33','8A:46:85:F3:9A:A6','0 days, 22:43:17']]"

        sabaiState = SabaiState(arpString, dhcpdStaticString, dhcpdLeaseString)
        print("Found {} entries".format(len(sabaiState.entries)))
        for state in sabaiState.entries:
            print("{} \n{} \n{}\n{}\n".format(state.name,state.ip,state.mac,state.assignment.name))

#SabaiState.testState()
# 00:01:2E:A0:BE:CD<192.168.199.2<vpna<0<1>
# 58:85:E9:F3:16:FB<192.168.199.167<realme-X2<0<3>
# F8:FF:C2:05:A0:29<192.168.199.222<Stephens-MBP<0<0>
# 98:F7:81:7C:45:3E<192.168.199.78<<0<0>
# AC:9B:0A:10:4C:8C<192.168.199.240<android-96237537fe2ef76e<0<0>
# DE:72:65:0C:E9:B5<192.168.199.34<Karine-s-Galaxy-S20-FE<0<3>
# 82:B2:C9:80:21:C7<192.168.199.248<realme-3<0<1>
# 58:85:E9:73:16:FB<192.168.199.168<<0<0>
# C4:DD:57:1F:64:5B<192.168.199.19<ESP_1F645B<0<1>
# D0:57:7B:77:E4:9E<192.168.199.56<lhubert-GL702VM<0<1>
# B0:DE:28:0E:48:A0<192.168.199.169<Stephens-MBP1<0<1>