from flask import Flask, render_template, redirect, flash, url_for, session, request, logging
#import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import psycopg2

app = Flask(__name__, template_folder='template')
auth = HTTPBasicAuth()

#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:@localhost/bbm'
#db=SQLAlchemy(app)
con=psycopg2.connect(dbname='DBMS_PROJECT',user='postgres',password='Sushma&sagar')
cur=con.cursor()

Patient_username = ['Patient1','Patient2','Patient3']
Patient_password = ['Pass1','Pass2','Pass3']

Doctor_username = ['Doctor1','Doctor2','Doctor3']
Doctor_password = ['Doc1','Doc2','Doc3']

@app.route("/")
def home():
    return render_template("HOME.html")

'''@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        user=request.form["un"]
        return render_template("Patient") 
    else:
       return render_template("HOME.html")'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #print("Something is happening here")
    #print(request.form["username"],request.method)
    if request.method == 'POST':
        if request.form['username'] in Patient_username or request.form['password'] in Patient_password:
            return render_template('login.html')
        elif request.form['username'] in Doctor_username or request.form['password'] in Doctor_password:
            return render_template('doctor.html')
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('loginfailed.html', error=error)
    pass 
    
   
@app.route("/Patient",methods=["POST","GET"])
def Patient():
    
    #return render_template("Patient.html")
    if request.method  == 'POST':
        # Get Form Fields
        appointment_id = request.form.get("appointment_id")
        d_id = request.form.get("d_id")
        p_id = request.form.get("p_id")
        email_id = request.form.get("email_id")
        cur.execute("INSERT INTO appointment(appointment_id,d_id,p_id,email_id)  VALUES(%s, %s, %s, %s)",(appointment_id,d_id,p_id,email_id))
        con.commit()
        return render_template("HOME.html")
    return render_template("Patient.html")
    
        
        
    
@app.route("/New_Patient",methods=["POST","GET"])
def New_Patient():
    
    #return render_template("Patient.html")
    if request.method  == 'POST':
        # Get Form Fields
        p_id = request.form.get("p_id")
        address=request.form.get("address")
        email_id = request.form.get("email_id")
        dob = request.form.get("dob")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        doctor_id=request.form.get("doctor_id")

        
        cur.execute("INSERT INTO Patient(p_id,address,email_id,dob,first_name,middle_name,last_name,doctor_id)  VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(p_id,address,email_id,dob,first_name,middle_name,last_name,doctor_id))
        con.commit()

    return render_template("New_Patient.html")


@app.route("/New_Doctor",methods=["POST","GET"])
def New_Doctor():
    
    #return render_template("Doctor.html")
    if request.method  == 'POST':
        # Get Form Fields
        d_id = request.form.get("d_id")
        d_name= request.form.get("d_name")
        d_phone= request.form.get("d_phone")
        d_addr=request.form.get("d_addr")
        avaliable_hours = request.form.get("avaliable_hours")

        
        cur.execute("INSERT INTO Doctor(d_id,d_name,d_phone,d_addr,avaliable_hours)  VALUES(%s, %s, %s, %s, %s)",(d_id,d_name,d_phone,d_addr,avaliable_hours))
        con.commit()

    return render_template("New_Doctor.html")

    
@app.route('/view')
def view():
    cur.execute("SELECT * FROM medicine")
    data = cur.fetchall()
    #print(data)
    return render_template('view.html', data=data)    

@app.route('/Complex')
def doctor():
    cur.execute("select medicine.medicine_name from (medicine inner join prescription on medicine.medicine_id =prescription.med_id) where prescription.d_id=6")
    data = cur.fetchall()
    #print(data)
    return render_template('Complex.html', data=data) 

'''
@app.route('/userlogin')
def userlogin():
     return render_template('userlogin.html')'''
'''@app.route('/Patient',methods=['GET','POST'])
def Patient():

    if request.method=='POST':
       
        password = request.form['password']
        username = request.form['usertype']

        if username=='Patient1' and password =='1234':
            return render_template('/Patient.html')
        elif username=='Patient2' and password =='1511':
            return render_template('/Patient.html')
    return render_template('/HOME.html')

''''''@app.route('/admin')
def admin():
     return render_template('admin.html')

@app.route('/patient',methods=['GET','POST'])
def patient():
    return render_template('patient.html')

@app.route('/viewCamps')
def viewcamps():
    cur.execute("SELECT * from camp")
    
    details = cur.fetchall()
    
    if len(details)>0:
        return render_template('viewCamps.html',details=details)
    else:
         msg = ' Blood Bank is Empty '
         return render_template('viewcamps.html',msg=msg)

    #close connection
@app.route('/donarlist')
def donarlist():
    cur.execute("SELECT * from donar")
    
    details = cur.fetchall()
    
    if len(details)>0:
        return render_template('donarlist.html',details=details)
    else:
         msg = ' Blood Bank is Empty '
         return render_template('donarlist.html',msg=msg)


@app.route('/donar_dashboard',methods=['GET','POST'])
def donar_dashboard():
    if request.method  == 'POST':
        # Get Form Fields
        dname = request.form["d_name"]
        age = request.form["d_age"]
        address = request.form["d_address"]
        demail = request.form["d_email"]
        donar_id = request.form["donar_id"]
        blood_grp = request.form["blood_grp"]
        campid=request.form["campid"]
        print("hello")
        #create a cursor
        #cur=con.cursor()

        #Inserting values into tables
        cur.execute("INSERT INTO donar(d_name,d_age,d_address,d_email,donar_id,d_blood_grp,cid) VALUES(%s, %s, %s, %s, %s, %s, %s)",(dname,age,address,demail,donar_id,blood_grp,campid))
        #Commit to DB
        con.commit()
        #close connection
        flash('Success! Donor details Added.','success')
        #return redirect(url_for('donor_dashboard'))

    return render_template('donar_dashboard.html')
'''
'''@app.route('/camps')
def camp():
     return render_template('camps.html')
'''
'''@app.route('/logout')
def logout():
    return render_template('logout.html')'''

if __name__=='__main__':
    app.secret_key='some secret key'
    app.config['SESSION_TYPE']='filesystem'
    app.run(debug=True)
