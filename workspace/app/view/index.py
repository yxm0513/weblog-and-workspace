from flask import Module, render_template, request, flash,\
        redirect, url_for, jsonify
from app.model import db,Host, Ssh, Type, Link, Ring
import subprocess
from socket import *
import setting
from app.lib.decorator import no_cache_header

mod = Module(__name__)

def check_port(address, port):
    targetIP = gethostbyname(address)
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((targetIP, port))
    if(result == 0) :
        s.close()
        return 1
    else:
        s.close()
        return 0

@mod.route("/_check_port")
def _check_port():
    hostname = request.args.get('hostname')
    result = {}
    if int(subprocess.call("ping -n 1 %s" % hostname)):
        return render_template("_get_port.html", hostname = hostname, result = None)
    else:
        for service in setting.SERVICES:
            result[service] = check_port(hostname, setting.SERVICES[service])
        return render_template("_get_port.html", hostname = hostname, result = result)


@mod.route("/host_edit", methods=["GET", "POST"])
def host_edit():
    if request.method == "POST":
        hostname = request.form['hostname']
        host = Host.query.filter_by(hostname=hostname).first_or_404()
        if request.values.get('type'):
            host.type = request.values.get('type')
        if request.form.get('web_user') and request.form.get('web_pwd'):
            host.web_user = request.form.get('web_user')
            host.web_pwd = request.form.get('web_pwd')
        if request.form.get('naviseccli_user') and request.form.get('naviseccli_pwd'):
            host.naviseccli_user = request.form.get('naviseccli_user')
            host.naviseccli_pwd = request.form.get('naviseccli_pwd')
        if request.form.get('rdp_user') and request.form.get('rdp_pwd'):
            host.rdp_user = request.form.get('rdp_user')
            host.rdp_pwd = request.form.get('rdp_pwd')
        if request.form.get('ra_user') and request.form.get('ra_pwd'):
            host.ra_user = request.form.get('ra_user')
            host.ra_pwd = request.form.get('ra_pwd')
        if request.form.get('putty_user') and request.form.get('putty_pwd'):
            host.putty_user = request.form.get('putty_user')
            host.putty_pwd = request.form.get('putty_pwd')
        if request.values.get('ring'):
            name = request.values.get('ring')
            try:
                ring = Ring.query.filter_by(name=name).first()
                host.ring_id = ring.id
            except:
                host.ring_id = 1 # unringed
        host.update()
        types = Type.query.all()
        flash("Host: %s updated." % host.hostname, "successfully")
        return redirect(url_for("index"))
    else:
        hostname = request.args.get('hostname')
        host = Host.query.filter_by(hostname=hostname.strip()).first_or_404()
        types = Type.query.all()
        rings = Ring.query.all()
        return render_template("host.html", host = host, types = types, rings = rings)

@mod.route("/host_delete")
def host_delete():
    hostname = request.args.get('hostname')
    host = Host.query.filter_by(hostname=hostname.strip()).first_or_404()
    host.delete()
    flash("Host: %s removed." % host.hostname, 'successfully' )
    return redirect(url_for("index"))

@mod.route("/", methods = ["GET", "POST"])
@no_cache_header
def index():
    if request.method == "POST":
        # Add host
        if not request.form['host']:
            flash('Host is required', 'error')
        else:
            host = Host(request.form['host'].strip())
            type = request.values['type']
            hostname=host.hostname
            host.type = type
            # check unique
            try:
                if Host.query.filter_by(hostname=hostname).first():
                    flash("Host: %s has been registered before." % hostname)
                    return redirect(url_for("index"))
            except:
                # create_all
                db.create_all()
            # check pingable
            if int(subprocess.call("ping -n 1 %s" % hostname)):
                flash("Host: %s is not pingable." % (hostname), 'error')
                return redirect(url_for("index"))
            # check system information
            host.save()
            flash("Host: %s added." % hostname, 'successfully')
            return redirect(url_for("index"))
    else:
        try:
            types = Type.query.all()
            rings = Ring.query.order_by(Ring.id.desc()).all()
#            availeble = []
#            for ring in rings:
#                if ring.hosts[]:
#                    print(ring.name)
#                    availeble.append(ring) 
            return render_template("index.html", types = types, rings = rings)
        except:
            db.create_all()
            return render_template("index.html", types = None, rings = None)


@mod.route('/about')
def about():
    return render_template("about.html")

@mod.route('/message')
def message():
    return render_template("_message.html")