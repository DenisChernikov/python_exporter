import paths

def db_identify():
    with open(paths.tm + 'db_mode', 'r') as f:
        db_type = f.readline().strip()
        return db_type
        
db_type = db_identify()
