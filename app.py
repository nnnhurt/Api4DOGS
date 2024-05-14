"""A module, which contains the main Flask app."""
from os import getenv
from io import BytesIO
import base64
from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from model import Dog, ColorEnum, BreedEnum, Base
from dotenv import load_dotenv
import requests
from PIL import Image
load_dotenv()
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_PASSWORD = getenv('PG_PASSWORD')
PG_USER = getenv('PG_USER')
PG_DBNAME = getenv('PG_DBNAME')
app = Flask(__name__)


engine = create_engine(
    f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@app.get('/')
def index():
    """
    Displays the main page.

    Returns:
        HTML: Home page template.
    """
    return render_template('index.html')


def get_dog_info(breed):
    """
    Fetches information about a dog breed from an external API.

    Args:
        breed (str): The name of the dog breed.

    Returns:
        dict or None: A dictionary containing information about the dog breed,
        excluding the image link, if successful.
        None if the request fails or the breed is not found.
    """
    url = f"https://api.api-ninjas.com/v1/dogs?name={breed}"
    response = requests.get(url, headers={'x-api-key': getenv('API_KEY')})
    if response.status_code == 200:
        answer = response.json()[0]
        answer.pop('image_link')
        return answer
    else:
        return None


def is_enum_member(enum_type, string):
    """
    Checks if a string is a valid member of the specified enumeration type.

    Args:
        enum_type (Enum): The enumeration type to check against.
        string (str): The string to check for membership in the enumeration.

    Returns:
        bool: True if the string is a valid member of the enumeration, False otherwise.
    """
    try:
        enum_type(string)
    except ValueError:
        return False if string else True
    return True


@app.route('/get_random_dog_image', methods=['GET'])
def get_random_dog_image():
    """
    Retrieves a random image of a dog based on breed and color.

    Args:
        breed (str): The breed of the dog.
        color (str): The color of the dog.

    Returns:
        HTML: The rendered template with the random dog image and information.

    Raises:
        HTTPException: If the specified breed or color is not found.
    """
    breed = request.args.get('breed')
    color = request.args.get('color')
    if not is_enum_member(BreedEnum, breed) or not is_enum_member(ColorEnum, color):
        abort(404, 'such characteristics do not exist')
    with Session() as session:
        query = session.query(Dog)
        if breed:
            query = query.filter_by(breed=BreedEnum(breed))
        if color:
            query = query.filter_by(color=ColorEnum(color))

        random_dog = query.order_by(func.random()).first()

        if random_dog:
            dog_info = get_dog_info(random_dog.breed.value)
            if dog_info:

                image_base64 = base64.b64encode(
                    random_dog.image).decode('utf-8')
                return render_template('dog.html', image=image_base64, info=dog_info)

        abort(404, "Failed to retrieve dog breed information.")


@app.post('/upload')
def upload_file():
    """
    Uploads a file (dog image) and associated data to the server.

    Returns:
        HTTP response: Redirects to the index page upon successful upload.
    """
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    color = request.form['color']
    breed = request.form['breed']
    if file.filename == '':
        return redirect(request.url)
    image_bytes = BytesIO()
    image = Image.open(file)
    image.save(image_bytes, format='png')
    with Session() as session:
        new_dog = Dog(image=image_bytes.getvalue(),
                      color=ColorEnum[color.upper()], breed=BreedEnum[breed.upper()])
        session.add(new_dog)
        session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=getenv('FLASK_PORT'))
