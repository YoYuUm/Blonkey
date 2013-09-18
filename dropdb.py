#from app.models import base, engine
#base.metadata.drop_all(engine)

from app import db
db.drop_all()