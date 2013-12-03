import re

'''
victor:

help to fetch proper service section by check requesting hostname

an experience: checking remote ip is not a good way, because it is always
127.0.0.1 when request by a domain name instead an ip address

usage:
- in view:
from libtahoe import *
  if isdev(request):
     do something
     
- in template
<%! from libtahoe import isdev,isdemo1,isdemo2 %>
% if isdemo1(request):
do something
% endif
 
'''

def isdev(request):
    ip=request.META['REMOTE_ADDR']
    dn=request.META['HTTP_HOST']  # request.get_host()
    if re.match('127.0.0.1',dn):
        return True
    if re.match('localhost',dn):
        return True
    if re.match('www0',dn):
        return True
    if re.match('studio0',dn):
        return True    

def isdemo1(request):
    ip=request.META['REMOTE_ADDR']
    dn=request.META['HTTP_HOST']  # request.get_host()
    if re.match('www1',dn):
        return True
    if re.match('studio1',dn):
        return True    
    if re.match('l1',dn):
        return True
    if re.match('c1',dn):
        return True
    if re.match('demo',dn):
        return True    

def isdemo2(request):
    ip=request.META['REMOTE_ADDR']
    dn=request.META['HTTP_HOST']  # request.get_host()
    if re.match('www1',dn):
        return True
    if re.match('studio1',dn):
        return True    
    if re.match('l1',dn):
        return True
    if re.match('c1',dn):
        return True     
