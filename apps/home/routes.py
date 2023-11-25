# -*- encoding: utf-8 -*-

from sqlalchemy import null
from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from .backend import backend as back
import threading, signal
import subprocess

import socket 

@blueprint.route('/index')
@login_required
def index():
    # --------- dict of server name and its bi directional packets ---------
    totalPackets = sum(b_obj.totalPacketsDict.values())
    dist_sort = {k: v for k, v in sorted(b_obj.totalPacketsDict.items(), key=lambda item: item[1], reverse=True)}
    # Extracting Keys
    keys = list(dist_sort)
    keys = ' '.join(keys).split()

    # Extracting values
    values = list(dist_sort.values())

    # --------- List of last 10 sec packets --------- 
    t2 = threading.Thread(target=b_obj.packet_flow_per_minute())
    t2.daemon = True
    t2.start()

    return render_template('home/index.html', segment='index', runningDomains=b_obj.runningDomainList, blockedDomains=b_obj.blockedDomainList, t_protocols=(len(b_obj.blockedDomainList)+len(b_obj.runningDomainList)), t_packets=totalPackets, dicti=b_obj.totalPacketsDict, keys=keys, values=values, timelyList=b_obj.timelyPacketsList, timelyListSum=sum(b_obj.timelyPacketsList))

# ---------------------------------------------------------------------------------------

@blueprint.route('/block_it/<string:domain>')
def block_it(domain):
    #b_obj.runningDomainList.remove(domain)
    print(domain)

    #if domain not in b_obj.blockedDomainList:
        #b_obj.blockedDomainList.append(domain)

    return redirect("../index#here")

@blueprint.route('/unblock_it/<string:domain>')
def unblock_it(domain):
    b_obj.blockedDomainList.remove(domain)
    if domain not in b_obj.runningDomainList:
        b_obj.runningDomainList.append(domain)

    return redirect("../index#here")

@blueprint.route("/runnings.html")
def runnings():
    totalPackets = sum(b_obj.totalPacketsDict.values())
    return render_template('home/runnings.html', segment='runnings', runningDomains=b_obj.runningDomainList, blockedDomains=b_obj.blockedDomainList, t_protocols=(len(b_obj.blockedDomainList)+len(b_obj.runningDomainList)), t_packets=totalPackets, timelyListSum=sum(b_obj.timelyPacketsList))

@blueprint.route("/blocked.html")
def blocked():
    totalPackets = sum(b_obj.totalPacketsDict.values())
    return render_template('home/blocked.html',  segment='blocked', runningDomains=b_obj.runningDomainList, blockedDomains=b_obj.blockedDomainList, t_protocols=(len(b_obj.blockedDomainList)+len(b_obj.runningDomainList)), t_packets=totalPackets, timelyListSum=sum(b_obj.timelyPacketsList))

@blueprint.route('/block_it2/<string:domain><int:x>')
def block_it2(domain, x):
    ip_addresses = domain_to_ip(domain)
    print(ip_addresses)

    for ip_address in ip_addresses:
        iptables_command = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
        subprocess.run(iptables_command)


    b_obj.runningDomainList.remove(domain)
    if domain not in b_obj.blockedDomainList:
        b_obj.blockedDomainList.append(domain)

    return redirect("/runnings.html#"+str(x))

@blueprint.route('/unblock_it2/<string:domain><int:x>')
def unblock_it2(domain,x):
    ip_addresses_to_unblock = domain_to_ip(domain)
    # Build and run iptables commands to unblock each IP address
    for ip_address in ip_addresses_to_unblock:
        iptables_command = ["sudo", "iptables", "-D", "INPUT", "-s", ip_address, "-j", "DROP"]
        subprocess.run(iptables_command)

    b_obj.blockedDomainList.remove(domain)
    if domain not in b_obj.runningDomainList:
        b_obj.runningDomainList.append(domain)

    return redirect("/blocked.html#"+str(x))

@blueprint.route('/unblock_all')
def unblock_all():
    t4 = threading.Thread(target=b_obj.unblock_all_func)
    t4.daemon = True
    t4.start()

    if len(b_obj.blockedDomainList) > 0:
            b_obj.runningDomainList.extend(b_obj.blockedDomainList)
            b_obj.blockedDomainList.clear()
    # b_obj.unblock_func(domain)


    return redirect("/blocked.html")

@blueprint.route('/block_all')
def block_all():
    if len(b_obj.runningDomainList) > 0:
        b_obj.blockedDomainList.extend(b_obj.runningDomainList)
        b_obj.runningDomainList.clear()

    return redirect("/runnings.html")
# ---------------------------------------------------------------------------------------


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



def domain_to_ip(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses[2]
    except socket.gaierror as e:
        print(f"Error resolving {domain}: {e}")
        return []
    

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None


b_obj = back()
t= threading.Thread(target=b_obj.dpi_func)
t.daemon = True
t.start()