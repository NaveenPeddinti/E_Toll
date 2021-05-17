from flask import Flask, render_template, request, redirect, url_for
import sqlite3  
import logging      
app = Flask(__name__)  
     
@app.route("/")  
def index():  
    return render_template("index.html");  
     
@app.route("/register")  
def register():  
    return render_template("register.html")  
     
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    #logging.basicConfig(filename='example.log',level=logging.DEBUG)
    
    if request.method == "POST":  
        try:  
            vehiclenumber = request.form["vehiclenumber"]  
            account = request.form["accountnumber"]  
            source = request.form["startfrom"]  
            destination = request.form["destination"]
            mobile = request.form["mobilenumber"]
            #toll_data = []
            with sqlite3.connect("E_Toll.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Information (Vehiclenumber, Accountnumber, Startfrom, Destination, MobileNumber) values (?,?,?,?,?)",(vehiclenumber,account,source,destination,mobile))
                cursor = cur.execute("SELECT Toll_Plaza from Toll_Details where Source = ? and Destination = ?", (source,destination))
                #logging.info(cursor)
                #toll_data = cur.fetchall()
                #tolls = cur.fetchall() 
                for row in cursor:            
                    for record in row:
                        if(record != None):
                            toll_data = record 
                            #logging.info(toll_data)
                #logging.info(toll_data)             
                #value = str(toll_data).strip('[]')
                #translation = {39: None} 
                #data =  str(value).translate(translation)
                #toll_data = list(toll_data.split(","))
                con.commit()  
                msg = "Registered Successfully"  
        except:  
            con.rollback()  
            msg = "Regestration Un-Successfull"  
        finally:  
            
            #return render_template("success.html",msg = msg) 
            return redirect(url_for('view',tolls=toll_data,vc=vehiclenumber,src=source,dest=destination)) 
            con.close()  
     
@app.route('/view/<tolls>')  
def view(tolls): 
    vehiclenumber = request.args.get('vc')   
    source = request.args.get('src')  
    destination = request.args.get('dest')
    #rows = []
    tolls = tolls.split(",")
    toll_length = len(tolls)
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    toll_info = []
    con = sqlite3.connect("E_Toll.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor() 
    for i in range (toll_length):
        #logging.info(tolls[i])
        cursor = cur.execute('SELECT  Toll_Name, oneway, twoway from Toll_Data WHERE Toll_Name = ?', (tolls[i], ))  
        for row in cursor:  
            Toll_List = []          
            for record in row:
                if(record != None):
                    Toll_List.append(str(record)) 
            toll_info.append(Toll_List)         
        #rows = cur.fetchall()                  
    logging.info(toll_info)
    #toll_info = toll_info.strip('][').split(', ')
    
    return render_template("view.html",len = len(toll_info), rows = toll_info,vn=vehiclenumber,src=source,dest=destination,toll=tolls)
    #return redirect(url_for('display',row=toll_info,vc=vehiclenumber,src=source,dest=destination,toll=tolls))  
  


if __name__ == "__main__":  
    app.debug = True
    app.run()
    app.run(debug = True)  
