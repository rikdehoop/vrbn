
from sqlalchemy import create_engine, text

# Prompting user for database credentials
# host = input("Enter the host: ")
# database = input("Enter the database name: ")
# user = input("Enter the user: ")
# password = input("Enter the password: ")


# Database connection parameters
db_params = {
    'dbtype': '',
    'host': '',
    'port': '',
    'database': '',
    'user': '',
    'passwd': ''
}

engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["passwd"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
# Create a Session
session = Session()

def add_user_to_group(group_id, user_mail):
#104
    sql_query = f"""
        INSERT INTO data.groups_users (group_id, user_id)
        SELECT g.id AS group_id, u.id AS user_id
        FROM data.groups g
        CROSS JOIN auth.users u
        WHERE g.id = {group_id}
        AND lower(u.name) = lower('{user_mail}')
        AND NOT EXISTS (
            SELECT 1
            FROM data.groups_users gu
            WHERE gu.group_id = g.id
            AND gu.user_id = u.id
        );
    """

    try:
        # Execute the SQL query
        session.execute(text(sql_query))
        # Commit the transaction
        session.commit()
    except Exception as e:
        # Rollback in case of error
        session.rollback()
        raise e
    finally:
        # Close the session
        session.close()






import pandas as pd
pd.set_option('display.max_rows', None)  # None means unlimited rows
pd.set_option('display.max_columns', None)  # None means unlimited columns
pd.set_option('display.width', 200)
# Reading the CSV file with semicolon delimiter
df = pd.read_csv('namenoverzicht_tbv_collectie_vakbekwaamheid.csv', delimiter=';', encoding='latin1')
# Filtering rows where 'afdeling' contains 'brandweerzorg' (case-insensitive)
# query_contain = input('vrbn afdeling? : ')
# filtered_df = df[df['afdeling'].str.contains(f'{query_contain}', case=False, na=False)]
# Printing the first 5 rows of the DataFrame

bwz_leden = df[['email']] 
# Initialize iteration counter
iter = 0

# Iterating through emails and printing each along with iteration count
group_id = input('group id? : ')
for index, row in bwz_leden.iterrows():
    email = row['email']
    iter += 1
    print(email)
    print(f"Iteration {iter} / {len(bwz_leden)}")
    add_user_to_group(group_id, email)



        
