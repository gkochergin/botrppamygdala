from config_reader import config
import sqlalchemy as db

engine = db.create_engine('sqlite:///products-sqlalchemy.db')

connection = engine.connect()

metadata = db.MetaData()

products = db.Table('products', metadata,
                    db.Column('product_id', db.Integer, primary_key=True),
                    db.Column('product_name', db.Text),
                    db.Column('supplier_name', db.Text),
                    db.Column('price_per_tonne', db.Integer)
                    )

metadata.create_all(engine)

insertion_query = products.insert().values([
    {'product_name':'Banana', 'supplier_name':'United Bananas', 'price_per_tonne':7000},
    {'product_name':'Avocado', 'supplier_name':'United Avocados', 'price_per_tonne':12000},
    {'product_name':'Tomatoes', 'supplier_name':'United Tomatoes', 'price_per_tonne':3100},
])

# connection.execute(insertion_query)

select_all_query = db.select([products])

select_all_result = connection.execute(select_all_query)

print(select_all_result.fetchall())
