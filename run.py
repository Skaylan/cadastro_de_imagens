from app import app
from app.models.conn import db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)