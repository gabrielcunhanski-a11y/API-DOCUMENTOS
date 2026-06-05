from config.database import db


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)

    documents = db.relationship('Documento', backref='city', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'population': self.population,
            'description': self.description,
            'documents': [doc.to_dict() for doc in self.documents],
        }
