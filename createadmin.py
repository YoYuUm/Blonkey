
from app import db
from app.models import User
user = User()
user.nickname = "admin"
user.email = "admin@admin.com"
user.password = "FastMonkeys"
user.role = 1
db.session.add(user)
db.session.commit()
