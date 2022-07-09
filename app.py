from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'table-responsive'})
row=table.find_all('td', attrs={'class' : 'text-narrow-screen-hidden'})

row_length = len(row)

temp = [] #initiating a list 

for i in range(1, 130):

    #get date 
    Date = table.find_all('td')[4*(i)-4].text
    
    #get rate
    Rate = table.find_all('td')[4*(i)-2].text
    Rate = Rate.strip() #to remove excess white space
    
    temp.append((Date,Rate)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date','Rate'))

#insert data wrangling here
#replace IDR and change the "," to "."
df['Rate'] = df['Rate'].str.replace(',','')
df['Rate']=df['Rate'].str.replace('IDR','')

#change date to datetime64 & rate to float64
df['Date']=df['Date'].astype('datetime64') 
df['Rate']=df['Rate'].astype('float64')

#set index column to date
df=df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (15,6)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)