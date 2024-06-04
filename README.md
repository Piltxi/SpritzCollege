<h3 align="center">SpritzCollege</h3>

---

<p align="center"> SpritzCollege revolutionizes the dormitory experience by merging top-notch accommodation with comprehensive student support.

The design combines traditional hotel management with advanced student tracking. Facilities include a variety of rooms and amenities, seamlessly managing personal data and diverse career paths. Additionally, a robust system enriches student life with a dynamic calendar of events and courses, open to both the public and registered visitors.

*SpritzCollege* is more than just a place to stay; it is a vibrant community designed to support and enhance the student experience.
    <br> 
</p>

## :tropical_drink: Introduction <a name = "getting_started"></a>

SpritzCollege contains two different apps: 
1. Activities
2. Profiles
### Activities

Activities contains features for managing events and courses; it is accessible by unregistered users, and by users with greater privileges: users of <i>culture</i> and <i>administration</i> group.

### Profiles

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
##  First step

If you don't have a local db:

``` bash
cd SpritzCollege 
```

``` bash
python3 manage.py createsuperuser
```

``` bash
python3 manage.py makemigrations Profiles
python3 manage.py makemigrations Activities
python3 manage.py makemigrations
python3 manage.py migrate
```

Now you are ready to start:
``` bash
python3 manage.py runserver
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
