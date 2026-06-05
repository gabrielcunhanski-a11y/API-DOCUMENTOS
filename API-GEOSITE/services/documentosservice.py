import os
from werkzeug.utils import secure_filename
from flask import current_app
from models.documentomodel import Documento
from config.database import db

class DocumentoService:
    @staticmethod
    def save_file(file):
        if not file:
            return None
        
        filename = secure_filename(file.filename)
        # Ensure the filename is unique to avoid overwriting
        # You might want to add a timestamp or UUID here
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename

    @staticmethod
    def create_document(titulo, file_path, tipo, user_id, city_id, url=None, descricao=None):
        new_doc = Documento(
            titulo=titulo,
            url=url,
            file_path=file_path,
            tipo=tipo,
            user_id=user_id,
            city_id=city_id,
            descricao=descricao
        )
        db.session.add(new_doc)
        db.session.commit()
        return new_doc

    @staticmethod
    def update_document(doc_id, user_id, data):
        doc = Documento.query.get(doc_id)
        if not doc:
            return None, "Document not found"
        
        if doc.user_id != user_id:
            return None, "Unauthorized: You are not the owner of this document"

        if 'titulo' in data:
            doc.titulo = data['titulo']
        if 'url' in data:
            doc.url = data['url']
        if 'tipo' in data:
            doc.tipo = data['tipo']
        if 'descricao' in data:
            doc.descricao = data['descricao']
        if 'city_id' in data:
            doc.city_id = data['city_id']

        db.session.commit()
        return doc, "Document updated successfully"

    @staticmethod
    def get_all_documents(titulo=None, tipo=None, city_id=None):
        query = Documento.query
        
        if titulo:
            query = query.filter(Documento.titulo.ilike(f"%{titulo}%"))
        if tipo:
            query = query.filter_by(tipo=tipo)
        if city_id:
            query = query.filter_by(city_id=city_id)
            
        return query.all()

    @staticmethod
    def get_document_by_id(doc_id):
        return Documento.query.get(doc_id)

    @staticmethod
    def get_documents_by_user(user_id):
        return Documento.query.filter_by(user_id=user_id).all()

    @staticmethod
    def delete_document(doc_id, user_id):
        doc = Documento.query.get(doc_id)
        if not doc:
            return None, "Document not found"
        
        if doc.user_id != user_id:
            return None, "Unauthorized: You are not the owner of this document"
            
        db.session.delete(doc)
        db.session.commit()
        return True, "Document deleted successfully"
