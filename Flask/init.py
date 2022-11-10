from flask import Flask
from flask import request

app = Flask(__name__)

def test():
    print("Hello")

@app.route("/",methods=['GET', 'POST'])
def home():
    #ioc=None
    if request.method == 'POST':
        ioc=request.form.get("ioc")
        #submit1=request.form.get("action1")
        #submit2=request.form.get("action2")

        return'''
             <h2>The IOC is: {} </h2>
             <input type="submit" value="Submit" onclick={}>
        '''.format(ioc,test())

    return '''
              <form method="POST" action="/">
                 
                  <div><label>Reading IOC: <input type="text" name="ioc"></label></div>
                  <input type="submit" value="Submit">
                  <input type="submit" value="submit" name="action1" />
                  <input type="submit" value="submit" name="action2" />
              </form>'''
    
if __name__ == "__main__":
    app.run(debug=True, port=1508)