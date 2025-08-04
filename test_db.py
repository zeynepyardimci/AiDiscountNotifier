from backend.gemini.models import db, TrackedProduct
from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'shared', 'instance', 'products.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def test_db():
    with app.app_context():
        db.create_all()

        product = TrackedProduct(
            category="Elektronik",
            color="Siyah",
            size="Orta",
            gender="Unisex",
            features="Bluetooth"
        )
        db.session.add(product)
        db.session.commit()
        print("Ürün eklendi.")

        products = TrackedProduct.query.all()
        for p in products:
            print(f"{p.id}: {p.category}, {p.color}, {p.size}, {p.gender}, {p.features}")

        db.session.delete(product)
        db.session.commit()
        print("Ürün silindi.")

if __name__ == "__main__":
    test_db() 