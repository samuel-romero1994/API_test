from flask_restx import Resource, fields, Namespace
from .models import Item
from . import db

api = Namespace('items', description='Operaciones relacionadas con items')

item_model = api.model('Item', {
    'id': fields.Integer(readOnly=True, description='El identificador único del item'),
    'name': fields.String(required=True, description='Nombre del item'),
    'description': fields.String(description='Descripción del item')
})

parser = api.parser()
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
parser.add_argument('description', type=str)

@api.route('/')
class ItemListResource(Resource):
    @api.marshal_list_with(item_model)
    def get(self): # método GET
        """Lista todos los items"""
        items = Item.query.all()
        return items

    @api.expect(item_model, validate=True)
    @api.marshal_with(item_model, code=201)
    def post(self): # método POST
        """Crea un nuevo item"""
        data = api.payload
        new_item = Item(name=data['name'], description=data.get('description'))
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201

@api.route('/<int:item_id>')
@api.param('item_id', 'El identificador del item')
@api.response(404, 'Item no encontrado')
class ItemResource(Resource):
    @api.marshal_with(item_model)
    def get(self, item_id): # Médoto GET de nuevo
        """Obtiene un item por su ID"""
        item = Item.query.get_or_404(item_id)
        return item

    @api.expect(item_model, validate=True)
    @api.marshal_with(item_model)
    def put(self, item_id): # Método PUT
        """Actualiza un item existente"""
        data = api.payload
        item = Item.query.get_or_404(item_id)
        item.name = data['name']
        item.description = data.get('description')
        db.session.commit()
        return item

    @api.response(200, 'Item eliminado')
    def delete(self, item_id): # Método DELETE
        """Elimina un item"""
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item eliminado'}, 200