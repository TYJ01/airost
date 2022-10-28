# analysis.py - analyze data collected from lazada.py and recommend top10 products based on no. of ratings and average rating
# opens tabs of the top10 products on the browser

import pandas
from selenium.webdriver import Chrome
from IPython.display import display
from lazada import browse_1


def score(dataframe):
    score = []
    for i in range(len(dataframe.index)):
        score.append(dataframe['no. of ratings'][i]*dataframe['average rating'][i])
    dataframe['score'] = score


def del_duplicates(dataframe, filepath):
    newdataframe = data_frame.drop_duplicates(subset=['link'])
    newdataframe.to_csv(filepath)
    return newdataframe


def analyze(filepath):
    global data_frame
    data_frame = pandas.read_csv(filepath, encoding='latin1')
    data_frame = del_duplicates(data_frame,filepath)
    score(data_frame)


def recommend(productname, method):
    if method == 'saved':
        analyze("D:\Documents\OneDrive\PYTHON\SCRIPTS\Airostrecruit\lazada product " + productname + '.csv')
    if method == 'new':
        browse_1(productname)
        analyze("D:\Documents\OneDrive\PYTHON\SCRIPTS\Airostrecruit\lazada product " + productname + '.csv')
    top10index = data_frame['score'].nlargest(n=10).index
    print('index and no. of ratings of top10 products')
    print(data_frame['no. of ratings'].iloc[top10index])
    print('index and average rating of top10 products')
    print(data_frame['average rating'].iloc[top10index])
    top10 = data_frame['link'].iloc[top10index]
    print('links to the top10 products : ')
    display(top10)
    browser=Chrome("D:\Documents\OneDrive\PYTHON\SCRIPTS\Airostrecruit\chromedriver_win32\chromedriver.exe")
    i = 1
    for link in top10:
        browser.get('http:' + link)
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[i])
        i+=1
    x = input('press x to exit ')


# To recommend top10 from saved product data
# run : recommend('product name','saved') , replace 'product name' with product of your choice

# recommend top10 for product not saved in excel
# run : recommend('product name','new') , replace 'product name' with product of your choice

# for example, lazada product ipad is saved in the proejct:
#recommend('ipad', 'saved')  # delete the '#' in the beginning of this line to run the programme

recommend('casio men analog','new')