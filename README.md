# SIRP - Image Based Recommendation System
SIRP (pl. System Inteligentnej Rekomendacji Produktów - intelligent product recommendation system)
## API
Minimal working API with SIRP

### Quick start
#### Requirements:
* Python 3 (Python 3.6 recommended)
* TensorFlow

#### Install other requirements
`$ pip install -r requirements.txt`

#### Generate recommendations
Prepare CSV file with ids and paths to images in following format:
```
0, path/to/image/0.jpg
1, path/to/image/1.jpg
2, path/to/image/2.jpg
3, path/to/image/3.jpg
```

Run generator script with your CSV files  
`$ cd tools/`  
`$ python generator.py images.csv`

Run server
`$ cd..`
`$ python run.py`

Now you should be able to send request
```
$ curl localhost:4350/recommendations/13
{
    "recommended_products": [
         "13",
         "2284",
         "1517",
         "205",
         "2400"
          ]
}
```

### Documentation

#### Running server
By default server is running using Flask's built-in server but it shouldn't be 
used for production. 
[Here you can read more about deploying to production.](http://flask.pocoo.org/docs/1.0/tutorial/deploy/)

##### Configuration
You can change or add your configuration by editing `config.py`. There are two
basic configuration classes:
* Config - Base Configuration, you can 


#### Endpoint
* GET `recommendations/<id>`
Get recommendations for given product ID.  
Optional querystring arguments:
* `limit` - number of recommendations to be returned  

Example request:  
`curl localhost:4350/recommendations/13?limit=3`   

Example response:
```json
{
    "recommended_products": [
         "13",
         "2284",
         "1517"
          ]
}
```

