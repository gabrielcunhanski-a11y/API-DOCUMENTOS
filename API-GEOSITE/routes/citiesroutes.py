from flask import Blueprint
from controllers.citiescontroller import CityController
from middlewares.auth import auth_required
from middlewares.admmiddleware import admin_required

cities_bp = Blueprint('cities_bp', __name__)

# GET: Geralmente aberto para todos os usuários logados
cities_bp.route('/', methods=['GET'])(auth_required(CityController.get_all))
cities_bp.route('/<string:slug>', methods=['GET'])(auth_required(CityController.get_by_slug))

# POST/PUT/DELETE: Restrito apenas para Administradores
cities_bp.route('/', methods=['POST'])(admin_required(CityController.create))
cities_bp.route('/<string:slug>', methods=['PUT'])(admin_required(CityController.update))
cities_bp.route('/<string:slug>', methods=['DELETE'])(admin_required(CityController.delete))
