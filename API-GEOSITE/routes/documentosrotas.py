from flask import Blueprint
from controllers.documentoscontroller import DocumentoController
from middlewares.auth import auth_required

documentos_bp = Blueprint('documentos_bp', __name__)

# Rotas protegidas
documentos_bp.route('/', methods=['POST'])(auth_required(DocumentoController.create))
documentos_bp.route('/', methods=['GET'])(auth_required(DocumentoController.get_all))
documentos_bp.route('/me', methods=['GET'])(auth_required(DocumentoController.get_my_documents))
documentos_bp.route('/<int:doc_id>', methods=['GET'])(auth_required(DocumentoController.get_by_id))
documentos_bp.route('/<int:doc_id>', methods=['DELETE'])(auth_required(DocumentoController.delete))
