from flask import Flask, render_template, request, redirect,url_for
from whitenoise import WhiteNoise
from markupsafe import escape
import visuals
import gather
import os
import converter

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="/static")

def test():
    print("Hello")

@app.route("/",methods=['GET', 'POST'])
def home():
    #ioc=None
    if (request.method == 'POST'):
        ioc=escape(request.form.get("ioc"))
        date=request.form.get("date")
        #submit1=request.form.get("action1")
        #submit2=request.form.get("action2")
        capture_name="index.html"
        check_mark=converter.ioc_check(ioc)
        successful=gather.writer(ioc,date)
        if(check_mark and ioc!=""):
            if(successful==1):
                
                capture_name=visuals.visual()
                return redirect(url_for('Iocfound',pathf=capture_name))

            else:
                return render_template("index.html",content="enter ioc")
        elif(ioc!="" and check_mark==0):
            ioc_dictionary=converter.search(ioc)
            headings=["IOC", "IOC_ID"]
            
            return render_template("index.html",headings=headings,row_data=ioc_dictionary)
        else:
            return render_template("index.html",IOC_MATCH_NULL="No IOC match found")
              


        

    return render_template("index.html")
@app.route("/graph",methods=['GET', 'POST'])
def Iocfound():
    capture_name=request.args["pathf"]
    try:
        
        return render_template(capture_name)
    except Exception as e:
        print(e)
        return render_template(capture_name)

    
if __name__ == "__main__":
    app.run(debug=True, port=9995)