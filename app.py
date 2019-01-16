from flask import Flask, render_template, send_file
from PIL import Image
from StringIO import StringIO
import requests,json, io

app=Flask(__name__)

# def apiCall(parameter,publishType,value):
#     baseurl='http://www.omdbapi.com/?'
#     api_key='apikey=e78cd22f'
#     result=requests.get(baseurl+api_key+'&type='+publishType+'&'+parameter+'='+value).text
#     data=json.loads(result)
#     return data

class Movie:
    
    def __init__(self,parameter):
        self.baseurl='https://yts.am/api/v2/'
        self.parameter=parameter
        self.req_url=self.baseurl+self.parameter
        
    def movieList(self):
        result=requests.get(self.req_url).text
        data=json.loads(result)
        return data
        
    def movieDetails(self,movie_id):
        result=requests.get(self.req_url+'?movie_id='+str(movie_id)).text
        data=json.loads(result)
        return data
    
def pegination(total,per_page,page_id):
    front_menu=[]
    back_menu=[]
    menu=[]
    if((per_page*page_id) < total):
        for x in range(0,7):
            if(((page_id+x)*per_page) < total):
                front_menu.append(page_id+x)
                
        for y in range(0,7):
            if((page_id-y) >= 1):
                back_menu.append(page_id-y)
                
        menu = front_menu    
        for z in back_menu:
            if(z not in front_menu):
                menu.append(z)
        menu.sort()
        return menu
    
def downloadImage(url):
    imageUrl = url.split('/')
    dirName, imageName = imageUrl[-2:]
    try:
        os.mkdir('flask/static/images/movies/'+dirName)
    except FileExistError:
        print 'Unable to create directory to save image'
    response = requests.get(url)
    img = Image.open(StringIO(response.content))
    img.save('flask/static/images/movies/'+dirName+'/'+imageName)
        
    
@app.route('/')
def welcome():
    movie=Movie('list_movies.json')
    return render_template('home.html', data=movie.movieList()['data'], peges=pegination(movie.movieList()['data']['movie_count'],movie.movieList()['data']['limit'],movie.movieList()['data']['page_number']))

@app.route('/browse/<page_id>')
def browse(page_id):
    movie=Movie('list_movies.json?page='+page_id)
    return render_template('home.html', data=movie.movieList()['data'], peges=pegination(movie.movieList()['data']['movie_count'],movie.movieList()['data']['limit'],movie.movieList()['data']['page_number']))

@app.route('/movie/<imdbId>')
def movieDetails(imdbId):
    movie=Movie('movie_details.json')
    return render_template('movie-details.html', title=movie.movieDetails(imdbId)['data']['movie']['title_long'], data=movie.movieDetails(imdbId)['data']['movie'])

# @app.route('/logo.jpg')
# def logo():
#     with open('logo.jpg', 'rb') as bites:
#         return send_file(
#             io.BytesIO(bites.read()),
#             attachment_filename = 'logo.jpg'
#             mimetype = 'image/jpg'
#         )

if __name__ == "__main__":
    app.run()
