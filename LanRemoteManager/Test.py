import os
import psutil


AF_INET_NUM = psutil.net_if_addrs()['WLAN'][1].family
AF_LINK_NUM = psutil.net_if_addrs()['WLAN'][0].family


print(os.environ.get("FULLNAME"))