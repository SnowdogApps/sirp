# SIRP - Image Based Recommendation System
SIRP (pl. System Inteligentnej Rekomendacji Produktów - intelligent product recommendation system)

#### Research repository
https://github.com/SnowdogApps/sirp-research

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
Using `SERVER_CONFIG` environmental variable you can choose config, by default 
there two options:  
* `SERVER_CONFIG=base` - base configuration
* `SERVER_CONFIG=dev` - development configuration (more about this in next 
section)

##### Configuration
You can change or add your configuration by editing `config.py`. There are two
basic configuration classes:
* Config - Base Configuration, you can inherit this class to create your own 
configurations
* Development - turns on debugging and pretty print for responses  

In configuration file you can set paths to your recommendation data and [other 
Flask configuration values](http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values)

#### Endpoint
* GET `recommendations/<id>`
Get recommendations for given product ID.  
Optional querystring arguments:
* `limit` - number of recommendations to be returned (default: 5)
* `including_first` - to include or not first recommendation(default: False / 0)* 

Example request:  
`curl localhost:4350/recommendations/13?limit=3&including_first=1`   

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
\* When you're looking for nearest neighbour using image from recommendation 
dataset it will find the same image as first result. Sometimes it is useful but 
in case of recommendation system probably you don't want to get the same product
as recommendation.

#### Generating recommendation space
```
usage: generator.py [-h] [--model {vgg16,inception,inception_resnet}]
                    [--output OUTPUT] [--scda]
                    images

Script for generating recommendation k-d tree

positional arguments:
  images                Path to text file with paths to images

optional arguments:
  -h, --help            show this help message and exit
  --model {vgg16,inception,inception_resnet}
                        Model which will be used as feature extractor
  --output OUTPUT       Path to where output should be saved.
  --scda                Activates Selective Convolutional Descriptor
                        Aggregation
``` 