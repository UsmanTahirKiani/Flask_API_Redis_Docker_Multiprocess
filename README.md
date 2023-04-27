# Flask App template with 
1) JWT Authentication configured
2) Authorisation Configured
3) Redis Configured
4) Login, Registered Routes 
5) SQLLite Database

## Installation

### Flask API (single process)

 **Commands**

````
sudo virtualenv env
source env/bin/activate
pip install -r requirements.txt
python app.py
````


### Flask API (Multi process)
````
uwsgi wsgi.ini
````
### Docker (Multiprocess)
````
sudo docker-compose stop
sudo docker-compose rm
sudo docker-compose build
sudo docker-compose up
````

## Contributing

Everyone can contribute to this project.

## License

Anyone can use or modify