from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine and session
engine = create_engine('sqlite:///your_database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Reflect existing database tables
metadata = MetaData(bind=engine)

# Define the table to clear (e.g., 'User')
user_table = Table('User', metadata, autoload=True)

# Clear all rows from the 'User' table
delete_query = user_table.delete()
session.execute(delete_query)

# Commit the transaction to apply changes
session.commit()

# Close the session
session.close()

print("All data cleared from the 'User' table.")
