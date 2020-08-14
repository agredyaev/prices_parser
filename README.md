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


Further Readings
----------------
