from config.database import db
from models.citiesmodel import City
import re

class CityService:
    @staticmethod
    def create_slug(name):
        return re.sub(r'\s+', '-', name.strip().lower())

    @staticmethod
    def create_city(name, population=None, description=None):
        if not name:
            raise ValueError("City name is required")

        existing_city = City.query.filter_by(name=name).first()
        if existing_city:
            raise ValueError("City with this name already exists")

        slug = CityService.create_slug(name)
        new_city = City(name=name, slug=slug, population=population, description=description)
        db.session.add(new_city)
        db.session.commit()
        return new_city.to_dict()

    @staticmethod
    def get_all_cities(name=None):
        query = City.query
        
        if name:
            query = query.filter(City.name.ilike(f"%{name}%"))
            
        cities = query.all()
        return [{
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "population": c.population,
            "description": c.description
        } for c in cities]

    @staticmethod
    def get_city_by_slug(slug):
        city = City.query.filter_by(slug=slug).first()
        if not city:
            return None
        return city.to_dict()

    @staticmethod
    def update_city(slug, data):
        city = City.query.filter_by(slug=slug).first()
        if not city:
            return None

        if 'name' in data:
            city.name = data['name']
            city.slug = CityService.create_slug(data['name'])

        if 'population' in data:
            city.population = data['population']

        if 'description' in data:
            city.description = data['description']

        db.session.commit()
        return city.to_dict()

    @staticmethod
    def delete_city(slug):
        city = City.query.filter_by(slug=slug).first()
        if not city:
            return False

        db.session.delete(city)
        db.session.commit()
        return True