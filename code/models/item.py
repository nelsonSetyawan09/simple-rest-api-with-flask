import pymysql.cursors

from db import db


class ItemModel(db.Model):
    __tablename__='items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store=db.relationship('StoreModel')


    def __init__(self,name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price,'store_id': self.store_id}

    @classmethod
    def find_by_name(cls,name): #chair
        return cls.query.filter_by(name=name).first()

    # insert inTO items values(self.name,self.price)
    def save_update_item_to_db(self):
        db.session.add(self) 
        db.session.commit()

    # delete from items where name='meja'
    def delete_item_from_db(self):
        db.session.delete(self)
        db.session.commit()
