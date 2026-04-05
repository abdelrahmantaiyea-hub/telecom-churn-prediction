import pandas as pd
from sqlalchemy import create_engine

# Load
df = pd.read_csv('cell2celltrain.csv', low_memory=False)

# Clean names for SQL compatibility
df.columns = [c.replace(' ', '_').replace('.', '').replace('-', '_') for c in df.columns]

# The Connection (root:PASSWORD@localhost/DATABASE_NAME)
engine = create_engine("mysql+pymysql://root:Abdo1234@localhost/cell2cell")
# Push
df.to_sql('train_data', con=engine, if_exists='replace', index=False)
print("Done! Check MySQL Workbench.")