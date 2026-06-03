from models.documentosmodels import Documento
from config.database import db

class DocumentoService:
    @staticmethod
    def create_document(titulo, url, tipo, user_id, descricao=None):
        new_doc = Documento(
            titulo=titulo,
            url=url,
            tipo=tipo,
            user_id=user_id,
            descricao=descricao
        )
        db.session.add(new_doc)
        db.session.commit()
        return new_doc

    @staticmethod
    def get_all_documents():
        return Documento.query.all()

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
