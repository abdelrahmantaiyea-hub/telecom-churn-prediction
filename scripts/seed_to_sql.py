import pandas as pd
from sqlalchemy import create_engine

# Load
# df = pd.read_csv('cell2celltrain.csv', low_memory=False)
df2 = pd.read_csv('cell2cellholdout.csv', low_memory=False)

# Clean names for SQL compatibility
df2.columns = [c.replace(' ', '_').replace('.', '').replace('-', '_') for c in df2.columns]

# The Connection (root:PASSWORD@localhost/DATABASE_NAME)
engine2 = create_engine("mysql+pymysql://root:Abdo1234@localhost/cell2cell")
# Push
df2.to_sql('test_data', con=engine2, if_exists='replace', index=False)
print("Done! Check MySQL Workbench.")