from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Подключение к базе данных PostgreSQL
engine = create_engine('postgresql://username:password@localhost:5432/bd_name')
Session = sessionmaker(bind=engine)

# Определение моделей данных
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship('Publisher', back_populates='books')
    purchases = relationship('Purchase', back_populates='book')

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='publisher')

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books.id'))
    id_shop = Column(Integer, ForeignKey('shops.id'))
    count = Column(Integer)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    data_sale = Column(DateTime)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer)

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String)

def create_tables(session):
    Base.metadata.create_all(engine)

def get_shops(session, publisher_data):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.data_sale
    ).select_from(Sale).\
           join(Sale.stock).\
           join(Stock.book).\
           join(Book.publisher).\
           join(Stock.shop)

    if publisher_data.isdigit():
        results = query.filter(Publisher.id == int(publisher_data)).all()
    else:
        results = query.filter(Publisher.name == publisher_data).all()

    for book_title, shop_name, price, sale_date in results:
        print(f"{book_title: <40} | {shop_name: <10} | {price: <8} | {sale_date.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    with Session() as session:
        create_tables(session)
        publisher_data = input("Введите имя или ID издателя: ")
        get_shops(session, publisher_data)