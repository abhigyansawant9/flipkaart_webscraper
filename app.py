from flask import Flask , render_template, jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log",level=logging.INFO)

app = Flask(__name__)

@app.route("/",methods=['GET'])
def homepage():
    return render_template("index.html")
@app.route("/review",methods=["POST",'GET'])
def index():
    if requests.method=='POST':
        try:
            searchString=request.form['content'].replace(' ',"")
            flipkart_url="https://www.flipkart.com/search?q="+searchString
            uclient=uReq(flipkart_url)
            flipkartPage=uclient.read()
            uclient.close()
            flipkart_html=bs(flipkartPage,"html.parser")
            bigbox=flipkart_html.find_all("div",{"class":"_1AtVbE col-12-12"})
            del bigbox[0:3]
            box=bigbox[0]
            productlink="https://www.flipkart.com"+box.div.div.div.a['href']
            prodRes=requests.get(productlink) 
            prodRes.encoding='utf-8'
            prod_html=bs(prodRes.text,"html.parser")
            print(prod_html)
            commentboxes=prod_html.find_all("div",{"class":"_16PBlm"})
            filename=SearchString+".csv"
            fw=open(filename,"w")
            headers="Product,Customer,Name,Rating,Heading,Comment\n"
            fw.write(headers)
            reviews=[]
            for commentbox in commentboxes:
                try:    
                    name=commentbox.div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})
                except:
                    logging.info("name")
                try:
                    rating=commentbox.div.div.div.div.text

                except:
                    rating="no rating"
                    logging.info(rating)        
                try:
                    commenthead=commentbox.div.div.div.p.text
                except:
                    commenthead="no comment head"
                    logging.info("commentHead")
                try:
                    comtag=commentbox.div.div.find_all("div",{"class":""})
                    custcomment=comtag[0].div.text
                except Exception as e:
                    logging.info(e)
                mydict={"product":searchstring,"name":name,"Rating":rating,"commenthead":commenthead,"comment":custcomment}
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))
            return render_template("result.html",reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return "somthing is wrong"
    else:
        return render_template(index.html)                



if __name__=="__main__":
    app.run(host="0.0.0.0")
