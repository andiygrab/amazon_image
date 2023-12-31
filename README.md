# golubnYk

This Django REST framework-based API serves as a RESTful interface for a social media platform.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/amazon_image
```

2. Change to the project's directory:
```bash
cd amazon_image
```
3. Authorize on aws


4. Once you're in the desired directory, run the following command to create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

6. Install the dependencies

```bash
pip install -r requirements.txt
```

7. Set up the database:

Run the migrations

```bash
alembic upgrade head
```


8. Start the development server
```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
9. Access the website locally at http://localhost:8000.


10. Link to the swagger documentation http://localhost:8000/docs

