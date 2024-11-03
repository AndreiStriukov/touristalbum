# ![](static/touristalbum/img/favicon.ico) WorldSNAP
## Contents
1. [About the website](#About-the-website)
2. [App Functionality](#App-Functionality)
3. [Tools](#Tools)
4. [Development Plans](#Development-Plans)

## About the website

WorldSnap is a platform for travelers to share their memories and emotions from trips. 

Travel enthusiasts can create albums, upload photos, and share their experiences about the places they've visited and the trips they've taken.

Visitors can freely browse photo albums, but registration is required to upload photos and create albums.

## Website Functionality

The homepage has a unified layout for both registered users and guests. It features a brief description of the website and displays the latest albums, allowing visitors to dive into new travel experiences and stories.

![](static/touristalbum/img//screens/homepage_ru.png)

![](static/touristalbum/img//screens/homepage_sm_ru.png)

![](static/touristalbum/img//screens/menu_sm_ru.png)

The website (project) consists of 2 applications (modules):
1. account - functionality for managing user accounts
2. album - functionality for managing created albums and published photos

### Account Module

The module allows users to:

* Register with email confirmation;
* Log in and out securely;
* Recover the password;
* In the personal account:
    + View and edit the profile;
    + Change the avatar;
    + Change the password.

![](static/touristalbum/img//screens/account_ru.png)


### Album Module

The module allows users to:

* Perform actions with albums:
    + View a list of albums with filtering options;
    + View information about an album;
    + Create an album;
    + Edit album properties;
* Perform actions with photos:
    + View photos:
        - in a gallery;
        - in a selected album;
        - as a general list;
    + Search for photos;
    + Publish photos linked to an album;
    + Edit a photo properties.

![](static/touristalbum/img//screens/albums_ru.png)

![](static/touristalbum/img//screens/gallery_ru.png)

## Tools
1. **Python** (3.12);
2. **Django** (Wev Framework);
3. **PostgreSQL** (database), psycopg (PostgreSQL database adapter for Python);
4. Django library: Pillow for image processing;
5. Slick slider library (downloaded) - a slider used for the image gallery.

## Development Plans

1. Add a captcha for a new user registration;
2. Change password functionality;
3. Deleting a profile;;
4. Pagination for viewing photos;
5. Deleting a photo;
6. Photo rating by visitors;
7. Album privacy settings (public/private);
8. Multilingual functionality.
