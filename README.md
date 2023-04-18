# Django Image Sharing App Backend
This is a backend for an image sharing app built using Django framework. The app includes features like liking image posts, uploading images, creating a user, making comments, liking comments and deleting images and comments.

## Installation
To run this app on your local machine, please follow these steps:

Clone the repository by running the following command in your terminal:

git clone https://github.com/yourusername/your-repo-name.git
Navigate to the root directory of the project and create a virtual environment by running:

python3 -m venv venv
Activate the virtual environment by running:

bash
source venv/bin/activate
Install the required packages by running:

pip install -r requirements.txt
Create a .env file in the root directory of the project and set the following environment variables:

makefile
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
Run database migrations by running the following command in your terminal:

python manage.py migrate
Run the server by running:

python manage.py runserver
