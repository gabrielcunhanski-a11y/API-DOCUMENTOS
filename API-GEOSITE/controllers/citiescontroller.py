from flask import request, jsonify
from services.citiesservice import CityService

class CityController:
    @staticmethod
    def create():
        data = request.get_json() or {}
        name = data.get('name')
        population = data.get('population')
        description = data.get('description')

        if not name:
            return jsonify({"error": "Bad Request", "message": "City name is required"}), 400

        try:
            city = CityService.create_city(name, population=population, description=description)
            return jsonify(city), 201
        except ValueError as e:
            return jsonify({"error": "Conflict", "message": str(e)}), 409
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def get_all():
        try:
            name_filter = request.args.get('name')
            cities = CityService.get_all_cities(name=name_filter)
            return jsonify(cities), 200
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def get_by_slug(slug):
        try:
            city = CityService.get_city_by_slug(slug)
            if city is None:
                return jsonify({"error": "Not Found", "message": "City not found"}), 404
            return jsonify(city), 200
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def update(slug):
        data = request.get_json() or {}
        try:
            city = CityService.update_city(slug, data)
            if city is None:
                return jsonify({"error": "Not Found", "message": "City not found"}), 404
            return jsonify(city), 200
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500

    @staticmethod
    def delete(slug):
        try:
            success = CityService.delete_city(slug)
            if not success:
                return jsonify({"error": "Not Found", "message": "City not found"}), 404
            return jsonify({"message": "City deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500
