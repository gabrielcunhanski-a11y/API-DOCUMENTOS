from config.database import db
from datetime import datetime, timezone

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    autor = db.relationship('User', backref=db.backref('documentos', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "url": self.url,
            "tipo": self.tipo,
            "user_id": self.user_id,
            "city_id": self.city_id,    
            "created_at": self.created_at.isoformat()
        }
