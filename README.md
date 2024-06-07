<h3 align="center">SpritzCollege</h3>

---

<p align="center"> SpritzCollege revolutionizes the dormitory experience by merging top-notch accommodation with comprehensive student support.

The design combines traditional hotel management with advanced student tracking. Facilities include a variety of rooms and amenities, seamlessly managing personal data and diverse career paths. Additionally, a robust system enriches student life with a dynamic calendar of events and courses, open to both the public and registered visitors.

*SpritzCollege* is more than just a place to stay; it is a vibrant community designed to support and enhance the student experience.
    <br> 
</p>

## 🍹 Introduction <a name="getting_started"></a>

<p align="center">
  <img src="img_readme/total.svg" />
</p>


- *Profiles App* This application handles user management, including registration, profile updates, and deletion. It inherits functionality from the Django framework for login and registration. Users can specify their interests during registration, which helps tailor their experience. The app also includes a notification system to alert users of new events and a chat system for real-time communication between users in the same course.

- *Activities App* This application manages information about events and courses. Users can browse available events and courses, register, and book seats. The app supports CRUD operations for events and courses, and authorized users can manage these activities comprehensively, including viewing and exporting booking data.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### 💻 Download Repo

If you don't have Git installed on your system, follow these steps to install it:

#### Windows 

1. Download Git from the official website: [https://git-scm.com/](https://git-scm.com/).

2. Run the downloaded file (.exe) and follow the installer instructions.

3. During installation, make sure to select "Use Git from the Windows Command Prompt" to add Git to your PATH.

4. Verify the installation by running the following command in the command prompt or PowerShell:

    ```bash
    git --version
    ```
#### MacOS

1. Open the terminal.

2. Install Git using Homebrew (if you don't have Homebrew, follow the instructions at [https://brew.sh/](https://brew.sh/)):

    ```bash
    brew install git
    ```

3. Verify the installation by running the following command in the terminal:

    ```bash
    git --version
    ```
#### Linux (Debian/Ubuntu):

1. Open the terminal.

2. Run the following commands:

    ```bash
    sudo apt-get update
    sudo apt-get install git
    ```

3. Verify the installation by running the following command in the terminal:

    ```bash
    git --version
    ```

Now you are ready! Run the following command to clone repo:

```
git clone https://github.com/Piltxi/SpritzCollege
```
##  <p style="color:orange; display:inline;"> *SpritzCollege* </p> setup and first <p style="color:red; display:inline;"> *drinks* </p>

In the following lines you can find some commands necessary to set up the development environment for the web platform.

After cloning the repo:
``` bash
cd SpritzCollege 
```

``` bash
python3 manage.py makemigrations Profiles
python3 manage.py makemigrations Activities
python3 manage.py makemigrations
python3 manage.py migrate
```

``` bash
python3 manage.py createsuperuser
```

After cloning the project, you can import some data into the database to start a demo session; to import them:
``` bash
python3 manage.py letmedream
```

Now you are ready to start:
``` bash
python3 manage.py runserver
```

*SpritzCollege* users can communicate with each other via chat, based on WebSocket and django-channels. 
To use it, docker must be installed. Then, using the following command, start the redis channel layer, as <a href="https://channels.readthedocs.io/en/stable/tutorial/part_2.html">described here</a>.
``` bash
docker run -p 6379:6379 -d redis:5
```
*Now you can make the most of the potential of the best orange platform in the world.*

If you want to do the first tests to check: 
``` bash
python3 manage.py test Activities
```

##  Active User 
<center>

| **Username** | **Password** | **Group**          |
|--------------|--------------|--------------------|
| admin        | admin    | *nd*            |
| elia        | pitz    | *all*           |
| visitor1        | tecnologieweb    | visitor           |
| visitor2        | tecnologieweb    | visitor           |
| Nicola        | capodieci    | culture       |
| Claudia        | django-channels    | administration           |
</center>
