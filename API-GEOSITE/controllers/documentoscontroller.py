from flask import request, jsonify
from services.documentosservice import DocumentoService

class DocumentoController:
    @staticmethod
    def create():
        user_id = getattr(request, 'user_id', None)
        
        # Obter dados do formulário (Multipart Form)
        titulo = request.form.get('titulo')
        tipo = request.form.get('tipo')
        city_id = request.form.get('city_id')
        descricao = request.form.get('descricao')
        url = request.form.get('url') # Opcional
        
        if not titulo or not tipo or not city_id:
            return jsonify({"error": "Bad Request", "message": "Missing required fields (titulo, tipo, city_id)"}), 400
            
        if 'file' not in request.files:
            return jsonify({"error": "Bad Request", "message": "No file part"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Bad Request", "message": "No selected file"}), 400
            
        try:
            # Salvar o arquivo físico
            filename = DocumentoService.save_file(file)
            
            # Criar o registro no banco
            doc = DocumentoService.create_document(
                titulo=titulo,
                file_path=filename,
                tipo=tipo,
                user_id=user_id,
                city_id=city_id,
                url=url,
                descricao=descricao
            )
            return jsonify({
                "message": "Document created successfully",
                "document": doc.to_dict()
            }), 201
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def update(doc_id):
        user_id = getattr(request, 'user_id', None)
        data = request.get_json()
        
        try:
            doc, message = DocumentoService.update_document(doc_id, user_id, data)
            if not doc:
                if "not found" in message.lower():
                    return jsonify({"error": "Not Found", "message": message}), 404
                return jsonify({"error": "Unauthorized", "message": message}), 403
                
            return jsonify({
                "message": message,
                "document": doc.to_dict()
            }), 200
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def get_all():
        titulo = request.args.get('titulo')
        tipo = request.args.get('tipo')
        city_id = request.args.get('city_id')
        
        docs = DocumentoService.get_all_documents(titulo=titulo, tipo=tipo, city_id=city_id)
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
