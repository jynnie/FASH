from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fash.models.user import *

engine = create_engine('sqlite:///fash.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

user = session.query(Users).filter(Users.email == 'jynnie@mit.edu').first()
print('\n USERS', user)
task = session.query(Tasks).filter(Tasks.id == 1).first()
completion = Completed(player=user, task=task, link="", valid=True)
session.add(completion)

# fam = session.query(Families).filter(Families.name == 'BFFL').first()
# print(fam.name)
# user.fam_mem = fam
# print(user.family)

# # Inserting families
# for family in ['Greater than U', 'Funky Bobasaurs', 'BFFL', 'Pirates', 'Gangstas']:
#     f = Families(name = family)
#     session.add(f)

session.commit()
