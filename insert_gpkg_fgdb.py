import subprocess
import fiona
from datetime import datetime


def get_datasource_type(file_path):
    try:
        with fiona.open(file_path) as src:
            return src.driver.lower()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    


def get_layers_from_geodata(geodata_filepath):
    try:
        with fiona.Env():
            return fiona.listlayers(geodata_filepath)
    except Exception as e:
        print(f"Error reading layers from file: {e}")
        return []

def insert_gpkg_to_existing_schema(dbname, user, password, host, port, schema_name, geodata_filepath):
    try:
        # Check the datasource type (GeoPackage or File Geodatabase)
        datasource_type = get_datasource_type(geodata_filepath)
        if datasource_type not in ['gpkg', 'openfilegdb']:
            print("Unsupported file type.")
            return
        layers = get_layers_from_geodata(geodata_filepath)
        if not layers:
            print("No layers found or error reading FGDB.")
            return
        # Get the current date
        current_date = datetime.now()

        # Format the date as DDMMYY
        date_code = current_date.strftime("%d%m%y")

        for layer_name in layers:
            
        # Construct the GDAL command as a list of arguments
            table_name = layer_name.lower()+'_'+date_code
            print(table_name)
            yn = input('is the table name correctly formulated?  y/n.. ')
            if yn == 'n':
                table_name = input('insert corrected table name: ')
            else:
                print('transfering file...')
            gdal_command = [
                'ogr2ogr', '-f', 'PostgreSQL',
                f'PG:dbname={dbname} user={user} password={password} host={host} port={port}',
                '-nln', table_name,
                '-lco', f'SCHEMA={schema_name}',
                geodata_filepath, layer_name
            ]
        
        # Execute the GDAL command using subprocess


            subprocess.run(gdal_command, check=True)

            print("Data transfer successfull.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing GDAL command: {e}")

def main():
    dbname = input("Enter the database name: ")
    user = input("Enter the username: ")
    password = input("Enter the password: ")
    host = input("Enter the host: ")
    port = input("Enter the port: ")
    schema_name = input("Enter the existing schema name: ")
    
    gpkg_file = input("Enter the path to the file: ")

    # Insert GeoPackage into existing schema
    insert_gpkg_to_existing_schema(dbname, user, password, host, port, schema_name, gpkg_file)

if __name__ == "__main__":
    main()

    










