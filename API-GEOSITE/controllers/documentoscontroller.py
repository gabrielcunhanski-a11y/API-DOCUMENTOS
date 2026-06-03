from flask import request, jsonify
from services.documentosservice import DocumentoService

class DocumentoController:
    @staticmethod
    def create():
        user_id = getattr(request, 'user_id', None)
        data = request.get_json()
        
        if not data or not data.get('titulo') or not data.get('url') or not data.get('tipo'):
            return jsonify({"error": "Bad Request", "message": "Missing required fields (titulo, url, tipo)"}), 400
            
        try:
            doc = DocumentoService.create_document(
                titulo=data['titulo'],
                url=data['url'],
                tipo=data['tipo'],
                user_id=user_id,
                descricao=data.get('descricao')
            )
            return jsonify({
                "message": "Document created successfully",
                "document": doc.to_dict()
            }), 201
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def get_all():
        docs = DocumentoService.get_all_documents()
        return jsonify([doc.to_dict() for doc in docs]), 200

    @staticmethod
    def get_by_id(doc_id):
        doc = DocumentoService.get_document_by_id(doc_id)
        if not doc:
            return jsonify({"error": "Not Found", "message": "Document not found"}), 404
        return jsonify(doc.to_dict()), 200

    @staticmethod
    def get_my_documents():
        user_id = getattr(request, 'user_id', None)
        docs = DocumentoService.get_documents_by_user(user_id)
        return jsonify([doc.to_dict() for doc in docs]), 200

    @staticmethod
    def delete(doc_id):
        user_id = getattr(request, 'user_id', None)
        success, message = DocumentoService.delete_document(doc_id, user_id)
        
        if not success:
            if "not found" in message.lower():
                return jsonify({"error": "Not Found", "message": message}), 404
            return jsonify({"error": "Unauthorized", "message": message}), 403
            
        return jsonify({"message": message}), 200
