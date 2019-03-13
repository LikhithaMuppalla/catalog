# Item Catalog Application
An Udacity Full Stack Web Developer  Nanodegree project developed by Likhitha Muppalla.

## About
This application provides a list of items within a variety of categories as well as provide a user authentication system. Users will have the ability to post, edit and delete their own items.

##Prerequisite Resources
You will need the following Python resources for it to run:

Python 2.7 or above (https://www.python.org/downloads/).
Git (https://git-scm.com/downloads).
Vagrant (https://www.vagrantup.com/).
VirtualBox (https://www.virtualbox.org/wiki/Downloads).
Sqlalchemy (https://www.sqlalchemy.org/download.html)

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd/vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run sudo pip install requests
7. Setup application database `python /item-catalog/john_setup.py`
8. *Insert fake data `python /item-catalog/ctstud_init.py`
9. Run application using `python /item-catalog/ehanjoel.py`
10. Access the application locally using http://localhost:9000


##JSON endpoints
1.Displays the whole catalog,categories and all items.
/Bag/JSON
2.Displays all  bag categories
/Bag/bagcatagories/JSON
3.Displays all bag items
/Bag/items/JSON
4.Displays items for a specific category
Bag/<path:bag_name>/items/JSON
5.Displays a specific category item
Bag/<path:item_name>/<path:edition_name>/JSON