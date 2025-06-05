from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://myuser:mypassword@localhost:5432/spacetraders")
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())
