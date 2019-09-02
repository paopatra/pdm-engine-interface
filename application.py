from flask import Flask, redirect, url_for, request,render_template
import pyodbc
import pandas as pd

def as_pandas_DataFrame(cursor):
    names = [metadata[0] for metadata in cursor.description]
    return pd.DataFrame([dict(zip(names, row)) for row in cursor], columns=names)

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:pdm-engine-interface-server.database.windows.net,1433;Database=PdM-Engine-Interface-DB;Uid=pdm-engine-interface-server@pdm-engine-interface-server;Pwd=Luckyday@2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()
app = Flask(__name__)
url = 'http://127.0.0.1:5000/'

###############################################################################
###### template equipment form
###############################################################################
@app.route('/')
def index():
   cursor.execute("SELECT * FROM tempequipment")
   df = as_pandas_DataFrame(cursor)
   return render_template('tempequipment_form.html', var = {'url': url,'data':df})

@app.route('/tempequipment_add',methods = ['POST', 'GET'])
def tempequipment_add():
   result = request.form
   cursor.execute("INSERT INTO tempequipment (tempequipment_name,tempequipment_desc) VALUES ('"+
                  result['equipment_name'] +"','" +result['equipment_des'] + "');")

   return redirect('/')

@app.route('/tempequipment_del',methods = ['POST', 'GET'])
def tempequipment_del():
   result = request.form
   cursor.execute("DELETE FROM tempequipment where tempequipment_id = "+result['tempequipment_id'])
   return redirect('/')
###############################################################################
####### template sensor form
###############################################################################
@app.route('/tempsensor_form',methods = ['POST', 'GET'])
def tempsensor_form():
   result = request.form
   cursor.execute("SELECT * FROM tempsensor where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempsensor_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})
@app.route('/tempsensor_add',methods = ['POST', 'GET'])
def tempsensor_add():
   result = request.form
   cursor.execute("INSERT INTO tempsensor (tempequipment_id,tempsensor_name,tempsensor_desc) VALUES ('"+
                  result['tempequipment_id'] +"','"+result['sensor_name'] +"','" +result['sensor_des'] + "');")
   cursor.execute("SELECT * FROM tempsensor where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempsensor_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})
@app.route('/tempsensor_del',methods = ['POST', 'GET'])
def tempsensor_del():
   result = request.form
   cursor.execute("DELETE FROM tempsensor where tempsensor_id = "+result['tempsensor_id'])
   cursor.execute("SELECT * FROM tempsensor where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempsensor_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})

###############################################################################
####### template failure form
###############################################################################
@app.route('/tempfailure_form',methods = ['POST', 'GET'])
def tempfailure_form():
   result = request.form
   cursor.execute("SELECT * FROM tempfailure where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempfailure_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})
@app.route('/tempfailure_add',methods = ['POST', 'GET'])
def tempfailure_add():
   result = request.form
   cursor.execute("INSERT INTO tempfailure (tempequipment_id,tempfailure_name) VALUES ('"+
                  result['tempequipment_id'] +"','"+result['failure_name'] + "');")
   cursor.execute("SELECT * FROM tempfailure where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempfailure_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})
@app.route('/tempfailure_del',methods = ['POST', 'GET'])
def tempfailure_del():
   result = request.form
   cursor.execute("DELETE FROM tempfailure where tempfailure_id = "+result['tempfailure_id'])
   cursor.execute("SELECT * FROM tempfailure where tempequipment_id = "+result['tempequipment_id'])
   df = as_pandas_DataFrame(cursor)
   return render_template('tempfailure_form.html', var = {'url': url,'data':df,'parent':result['tempequipment_id']})



###############################################################################
###############################################################################
if __name__ == '__main__':
   app.run(debug = False)
