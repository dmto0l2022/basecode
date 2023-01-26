from flask import Blueprint, render_template, flash, request, jsonify
##from flask import current_app
from app.models import Plots
from app.forms import EnterNewPlotForm, FormCreatePlot
from datetime import datetime
import json
from datetime import datetime

def stringdate():
    plotidnow = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    return plotidnow

plotids_bp = Blueprint('plotids_bp', __name__)
'''
@plotids_bp.route('/plots/new/')
def CreateNewPlot():
    name = 'new plot'
    plotid = 'P123455662357989092370'
    plotids = Plots.create(plotid,name)
    y =  {
        "plotid": plotid,
        "name": name
        }
    r = json.dumps(y)
    return r
'''

@plotids_bp.route('/plots/getall/', methods=["GET", "POST"])
def getallplots():
    j = jsonify(Plots.getall())
    return j

'''
@plotids_bp.route("/plots/enter", methods=["GET", "POST"])
def EnterNewPlotFunc():
    """Standard 'plot' form."""
    form = EnterNewPlotForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "newplot.html",
        form=form,
        template="form-template"
    )
'''

@plotids_bp.route("/plots/success", methods=["GET", "POST"])
def success():
   return "success"


#####

@plotids_bp.route("/plots", methods=["GET", "POST"])
def plots():
   return "plots"

# add a new plot to the database
@plotids_bp.route('/plots/create/', methods=['GET', 'POST'])
def FuncCreatePlot():
    form1 = FormCreatePlot()
    if form1.validate_on_submit():
        name = request.form['name']
        plotid = request.form['plotid']
        Plots.create(plotid,name)
        # create a message to send to the template
        message = f"The data for plot {plotid} has been submitted."
        return render_template('create_plot.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('create_plot.html', form1=form1)

# add a new plot to the database
@plotids_bp.route('/plots/read/', methods=['GET', 'POST'])
def FuncReadPlot():
    plotid = request.form['plotid']
    plot = Plots.read(plotid)
    form1 = ShowPlot()
    return render_template('read_plot.html', form1=form1)

# add a new plot to the database
@plotids_bp.route('/plots/update/', methods=['GET', 'POST'])
def FuncUpdatePlot():
    plotid = request.form['plotid']
    newname = "newname"
    plot = Plots.update(plotid, newname)
    plots = Plots.get
    form1 = ShowPlot()
    return render_template('update_plot.html', form1=form1)

# add a new plot to the database
@plotids_bp.route('/plots/delete/', methods=['GET', 'POST'])
def FuncDeletePlot():
    plotid_in = request.args.get('plotid')
    howmany = Plots.delete(plotid_in)
    return howmany

'''

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    sock = Sock.query.filter(Sock.id == id).first()
    # two forms in this template
    form1 = AddRecord()
    form2 = DeleteForm()
    return render_template('edit_or_delete.html', sock=sock, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    sock = Sock.query.filter(Sock.id == id).first()
    if purpose == 'delete':
        db.session.delete(sock)
        db.session.commit()
        message = f"The sock {sock.name} has been deleted from the database."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
def edit_result():
    id = request.form['id_field']
    # call up the record from the database
    sock = Sock.query.filter(Sock.id == id).first()
    # update all values
    sock.name = request.form['name']
    sock.style = request.form['style']
    sock.color = request.form['color']
    sock.quantity = request.form['quantity']
    sock.price = request.form['price']
    # get today's date from function, above all the routes
    sock.updated = stringdate()

    form1 = AddRecord()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"The data for sock {sock.name} has been updated."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        sock.id = id
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, sock=sock, choice='edit')
'''
