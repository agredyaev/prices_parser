prices_parser
=====================
__Getting compatitors prises from X website__

Why
-----
* Need to validate ML's model forecast accuracy in case of competitors prices factor added

Stack
-----
* Python
* Selenium
    - Web page navigation, grab data from HTML
* [docker-rotating-proxy](https://github.com/mattes/rotating-proxy)
    - Lots of IP addresses for one single endpoint.
* PostgreSQL

Operation process
-----------------
The program generates a list of links for a given site and a list of cities. Then links opens in multiple Windows of the browser and collects information about the products. 
The result is stored in the database. 

Logging is performed for debugging.

Usage
------
1. Install Docker
2. Configure [docker-rotating-proxy](https://github.com/mattes/rotating-proxy)
3. Configure db connection properties in __config.py__
4. Start docker container: docker run -d -p 5566:5566 -p 4444:4444 --env tors=25 mattes/rotating-proxy
5. Start program: python main.py 


Further Readings
----------------
