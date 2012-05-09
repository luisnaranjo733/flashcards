from models import *

luis = User()
luis.username = 'luis'
luis.password = 'balls'

session.add(luis);session.commit()
