# Django Service Marketplace Website

The Django Service Marketplace Website offers a sophisticated template utilizing Django and Django Template Language (DTL), facilitating the effortless creation and administration of service-oriented websites. It serves as a streamlined platform that bridges service providers with potential clients. Service providers can enlist their offerings on the site to captivate an audience seeking their services. Conversely, customers may utilize the platform to explore available services, peruse evaluations, and procure a service of their choice.</b>

 <span style="font-size:larger;">[Click here](https://tinyurl.com/MotoMatchWebsite) <b>and watch the website in action!</b></span></b>

[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Django Version](https://img.shields.io/badge/django-5.0.4-green.svg)](https://www.djangoproject.com/download/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Requirements (Prerequisites)
- Django 5.0.4
- Pillow 10.3.0

## Installation
1. Clone the repository: `git clone https://github.com/ariel-pi/MarketPlace.git`
2. Navigate to the project directory: `cd MarketPlace`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

you can delete the existing service and users by the administration site, for this, you need super user.<br>
### Creating a superuser in Django and Accessing the Django Admin Panel

1. Open a terminal or command prompt.

2. Navigate to your Django project directory.

3. Run the following command:
   `python manage.py createsuperuser`

4. Fill in the credentials.

5. Go to http://127.0.0.1:8000/admin

6. Log in with superuser credentials.

7. After successful authentication, you will be redirected to the Django admin panel, where you can manage your Django application's data, including models, users, groups, permissions, and more.





### Home Page
![Screenshot of Home Page](/MarketPlace/screenshots/Screenshot_home.png)

### Service Provider Dashboard
![Screenshot of Service Provider Dashboard](/MarketPlace/screenshots/Screenshot_service_provider_dashboard.png)

## Features
- User Authentication: Allows users to register, log in, log out, and update their profile information.
- Service Management: Service providers can add, edit, and delete services they offer.
- Booking System: Users can book services provided by service providers, including selecting service items and specifying booking details.
- Review System: Users can leave reviews and ratings for service providers after booking their services.
- Service Provider Dashboard: Service providers have access to a dashboard where they can manage their services, view bookings, and update booking statuses.
- Search Functionality: Users can search for services based on keywords.
- Responsive Design: The website is designed to be responsive and accessible on various devices.
- User-Friendly Interface: The interface is intuitive and easy to navigate for both users and service providers.

## DATABASE Scheme
[Click here](/database_scheme.svg) to view the structure of the database and the relationships between the models.


## Website Customization
The project is a ready-made website for example, but built in a way that allows you to adapt it to your needs with only a few minor changes:
1. Update the html files so that they contain your website data, for example replace MotoMatch with your website name, the "about" part of your website description, etc.
2. Make changes to [style.css](/MarketPlace/MarketPlaceWebsite/Website/static/css/style.css) (optional).
3. Change the [header image](/MarketPlace/MarketPlaceWebsite/Website/static/img/header_image.jpg).
4. change Change the fields in the ServiceItem class in the [models.py](/MarketPlace/MarketPlaceWebsite/Website/models.py) file according to the item on which the service is performed (in the example website this is actually the car).
Add/remove fields according to the website you are creating.
You can see in the project an example of several useful and common field types.
5. Change the labels in the ServiceItemForm class in the [forms.py](/MarketPlace/MarketPlaceWebsite/Website/forms.py) file.
They determine how the user will see the fields that he must fill in on your website when creating a new service item
6. In the current configuration of the website, slots can be ordered by the hour, if you want to change the site so that users can order a service by days (for example for staying in a hotel), look at the view booking_view_check_in_check_out() in [views.py](/MarketPlace/MarketPlaceWebsite/Website/views.py).
don't forget to update the Booking Model in [models.py](/MarketPlace/MarketPlaceWebsite/Website/models.py), BookingForm in [forms.py](/MarketPlace/MarketPlaceWebsite/Website/forms.py) and the url in Website/urls.py.


## Deployment Notes

A A convenient option to deploy the project is by [pythonanywhere](https://www.pythonanywhere.com/).<br>
This option is suitable for small projects, such as a university project, etc.<br>
For a commercial website, which is required to handle a large user traffic, we recommend considering alternative options.
Here you can find a guide for deploying a Django project on pythonanywhere.com:<br>
[Deploy a Django web app to Python Anywhere](https://www.youtube.com/watch?v=xtnUwvjOThg&ab_channel=CloudWithDjango)<br>

now, for loading yor static files, Check out this guide:
[Loading static files to pythonanywhere](https://help.pythonanywhere.com/pages/DjangoStaticFiles/)<br>
You can see [here](settings_for_deployment.py) how setting.py should look after deployment.<br>
Note that you update the SECRET_KEY, ALLOWED_HOSTS and STATIC_ROOT according to your data.

## Author

- Ariel Pinhas - Sole Developer/Creator
- [GitHub](https://github.com/ariel-pi)
- [Linkdin](http://www.linkedin.com/in/ariel-pinhas)

## License
This project is licensed under the MIT License.

