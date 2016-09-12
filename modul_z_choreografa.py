from naoqi import ALProxy
import sys

NAO_IP = "192.168.210.109"

HOST = "153.19.55.217"              # Adresem labolatoryjnym jest '153.19.54.27'
PORT = 9559                     # Portem labolatoryjnym jest 50002

alconnman = ALProxy("ALConnectionManager", NAO_IP, 9559)

print "network state: " + alconnman.state()
# if len(sys.argv) != 2:
#     print sys.argv[0] + " <serviceId>"
#     sys.exit(1)

alconnman = ALProxy("ALConnectionManager", NAO_IP, 9559)

try:
    print(sys.argv, "wodka wodka czaj randalena")
    alconnman.connect((PORT, HOST))
except Exception as e:
    print e, "popo"#.what()
    sys.exit(1)