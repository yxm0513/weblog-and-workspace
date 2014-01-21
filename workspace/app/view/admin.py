from flask import Module, render_template, request, flash,\
        redirect, url_for, jsonify
from app.model import db, Host, Ssh, Type, Link, Ring

mod = Module(__name__)


@mod.route("/")
def index():
    return render_template("admin.html")

@mod.route("/initdb")
def initdb():
    try:
        db.create_all()
    except:
        db.drop_all()
        db.create_all()
    # init some data
    try:
        # ring required
        unringed = Ring(name = "unringed")
        unringed.save()
        # data for simon
        wiki = Link("Team Wiki", "http://twiki.emccrdc.com/twiki/bin/view/ESD/Test/UsdEftTeam")
        wiki.save()
        report = Link("Weekly Report", 'http://report.emccrdc.com/mytimesheet.php?action=showts&reporter_id=177')
        report.save()
        myssh =  Ssh("MyLinux", "10.109.17.204 ", "xinming", "111111")
        myssh.save()
        rayssh =  Ssh("RayLinux", "10.32.191.173 ", "simon", "simon")
        rayssh.save()
        iohost = Type("IO HOST")
        iohost.save()
        spa = Type("SPA")
        spa.save()
        spb = Type("SPB")
        spb.save()
        vm = Type("VM")
        vm.save()
        host = Host("localhost")
        host.ring_id = unringed.id
        host.type = spa.name
        host.save()
        flash("Init database successfully.", 'successfully')
    except Exception as e:
        flash("Init database failed. %s" % e, 'error')
    return redirect(url_for("admin.index"))

@mod.route("/dropdb")
def dropdb():
    db.drop_all()
    flash("Drop database successfully.", 'successfully')
    return redirect(url_for("admin.index"))

@mod.route("/ssh", methods = ["GET", "POST"])
def ssh():
    if request.method == "POST":
        if request.form.get('name') and \
           request.form.get('host') and \
           request.form.get('user') and \
           request.form.get('pwd'):
            ssh = Ssh(request.form.get('name').strip(),\
                        request.form.get('host').strip(),\
                        request.form.get('user').strip(),\
                        request.form.get('pwd').strip() )
        try:
            ssh.save()
            flash("SSH: %s added."% ssh.name, 'successfully')
            return redirect(url_for("admin.ssh"))
        except:
            db.create_all()
            flash("Add SSH: %s failed."% ssh.name, 'error')
            return redirect(url_for("admin.ssh"))
    else:
        sshs= Ssh.query.all()
        return render_template("ssh.html", sshs = sshs)
    
@mod.route("/listssh", methods = ["GET"])
def listssh():
    try:
        sshs= Ssh.query.all()
        return render_template("_ssh.html", sshs = sshs)
    except:
        db.create_all()
        return render_template("_ssh.html", sshs = None)

@mod.route("/delssh")
def delssh():
    name = request.args.get('name')
    ssh= Ssh.query.filter(Ssh.name == name).first_or_404()
    ssh.delete()
    flash("SSH: %s removed." % name, 'successfully')
    return redirect(url_for("index"))

@mod.route("/type", methods = ["GET", "POST"])
def type():
    if request.method == "POST":
        if request.form.get('name'):
            type = Type(name = request.form.get('name').strip())
            type.save()
            flash("Host Type: %s added."% type.name, 'successfully')
            return redirect(url_for("admin.type"))
    else:
        types = Type.query.all()
        return render_template("type.html", types = types)

@mod.route("/deltype")
def deltype():
    name = request.args.get('name')
    type= Type.query.filter(Type.name == name).first_or_404()
    type.delete()
    flash("Host Type: %s removed." % name)
    return redirect(url_for("admin.type"))

@mod.route("/link", methods = ["GET", "POST"])
def link():
    if request.method == "POST":
        if request.form.get('name') and request.form.get('url') :
            link = Link(name = request.form.get('name').strip(),
                        url = request.form.get('url').strip())
            link.save()
            flash("Link: %s added."% link.name, 'successfully')
            return redirect(url_for("admin.link"))
    else:
        links = Link.query.all()
        return render_template("link.html", links = links)

@mod.route("/dellink")
def dellink():
    name = request.args.get('name')
    link= Link.query.filter(Link.name == name).first_or_404()
    link.delete()
    flash("Link: %s removed." % name, 'successfully')
    return redirect(url_for("admin.link"))

@mod.route("/listlink", methods = ["GET"])
def listlink():
    try:
        links= Link.query.all()
        return render_template("_link.html", links = links)
    except:
        db.create_all()
        return render_template("_link.html", links = None)
    
@mod.route("/ring", methods = ["GET", "POST"])
def ring():
    if request.method == "POST":
        if request.form.get('name'):
            ring = Ring(name = request.form.get('name').strip())
            ring.save()
            flash("Ring: %s added."% ring.name, 'successfully')
            return redirect(url_for("admin.ring"))
    else:
        rings = Ring.query.all()
        return render_template("ring.html", rings = rings)

@mod.route("/delring")
def delring():
    name = request.args.get('name')
    ring= Ring.query.filter(Ring.name == name).first_or_404()
    for h in ring.hosts:
        h.delete()
        flash("Host: %s removed." % h.hostname, 'successfully')
    ring.delete()
    flash("Ring and Hosts: %s removed." % name, 'successfully')
    return redirect(url_for("admin.ring"))