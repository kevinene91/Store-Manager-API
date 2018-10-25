from flask_restful import reqparse, Resource
from flask_jwt_extended import get_jwt_identity
from ..models.sales import SalesModel 
from ..models.auth import UserModel
from ...middleware.middleware import (admin_allowed, both_roles_allowed,
                                      attendant_allowed)
import ast

class SalesListResource(Resource):
    """ sales list resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("sale_items", type=dict, action='append')
    parser.add_argument("customer", type=str, required=True)
  
 
    @attendant_allowed
    def post(self): 
        """ save products """
        data = SalesListResource.parser.parse_args()
        current_user = get_jwt_identity()
        user_id = current_user[0]
        user = UserModel()
        user = user.get_item('users', user_id=user_id)
        attendant_email = user['email']
        attendant = attendant_email
        name = data['customer']

        for k, v in data.items():
            if v == "":
                return {"message": "{} cannot be an empty".format(k)}
    
        sale_list = data['sale_items']

        product_id = 0
        quantity = 0
        for item in sale_list:
            list_length = len(sale_list)
            iteration = list_length
            product_id = item['product_id']
            quantity = item['quantity']
            sale = SalesModel(customer=name, quantity=quantity)
            complete_sale = sale.create_sale(attendant, product_id, iteration)
            return complete_sale, 201

