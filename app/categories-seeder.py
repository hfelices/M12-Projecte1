from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder
from . import db_manager as db

# load entities
entities = load_entities_from_json('categories.json')

# Initializing Seeder
seeder = Seeder(db.session)

# Seeding
seeder.seed(entities)

# Committing
db.session.commit()  