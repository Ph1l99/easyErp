# EASY ERP
Easy ERP has been developed for a friend which owns a repair shop. He wanted an ERP fitted for its needs and, at the same time, easy to use.

## Features
The ERP comes with different features:
- Product management
- Repair management
- Customers and affiliation program management

## Technologies
The whole project has been developed using [Django](https://www.djangoproject.com/) as web framework
and [DjangoRestFramework](https://www.django-rest-framework.org/) has been used in order to build
reliable and flexible APIs; both of these frameworks are Python-based.

As persistent storage I have chosen the widely known and open source relational database
[PostgreSQL](https://www.postgresql.org/) since it best suits our needs.

The web pages (i.e. the frontend as we love to call it) have been developed as a [separate project](https://github.com/Ph1l99/easyerpui).

## Usage
The project can be downloaded and executed as is, by configuring it on a host machine. <br>
Docker support will be added in the future.

## Installation
- Download the project
- Install PostgreSQL and create a database named **EasyErp**
- Initialize a virtual environment and install dependencies `pip install -r requirements.txt`
- Set environment variables as required:
  - ENV -> DEV or PRD
  - DB_USERNAME -> user for PostgreSQL access
  - DB_USER_PASSWORD -> password for PostgreSQL user
  - DB_HOST -> PostgreSQL instance host
- Apply migrations `python3 manage.py migrate`
- Create a superuser `python3 manage.py createsuperuser`

If you just want to try EasyErp you can run the Django development server by typing `python3 manage.py runserver 8000`.

Otherwise, you have to install a web server in order to serve staticfiles and then run the project via gunicorn. [Here](https://djangodeployment.readthedocs.io/en/latest/) you can find a helpful guide.

#### Printers
The system supports two types of printing types and modes:
- Labels on Brother-QL
- Receipts on esc-pos printers

On Linux systems, since EasyErp is using `pyusb` as backend, in order to properly access the printers,
make sure to create a file (i.e `99-usb.rules` ) in `/etc/udev/rules.d/`. The file should contain two
lines which have the following syntax: `SUBSYSTEM=="usb", ATTRS{idVendor}=="PRINTER_VENDOR_ID", ATTRS{idProduct}=="PRINTER_PRODUCT_ID", MODE="0666", GROUP="dialout"`.
Then restart the service `sudo service udev restart`.

Make sure to run all the above commands as root user.

## Contributors
Thanks to [NessunoRAWRS](https://github.com/NessunoRAWRS).

## DISCLAIMER
EasyErp is provided "as is", with no guarantee of completeness and accuracy of the results obtained
from the use of this software, and without warranty of any kind, express or implied. <br>
The authors will not be liable to anyone for any decision made or action taken in reliance on
the information given by EasyErp or for any consequential, special or similar damages, even if advised of the possibility of such damages.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)