from manage import db,app

class birthdays(db.Model):
    __tablename__ = 'birthdays'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.DATE)

    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
