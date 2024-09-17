import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

from models import create_tables, Publisher, Shop, Book, Stock, Sale

load_dotenv()
DSN = os.getenv('DSN')
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
# запросы
writer = input('Input writer name or id: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(
    Sale)
if writer.isdigit():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()
for title, name, price, date_sale in query:
    print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")
