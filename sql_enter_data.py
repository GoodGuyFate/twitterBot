import mysql.connector
import json

def load_config():
    """Loads configuration data from the JSON file."""
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Error: config.json file not found!")
        exit()


config = load_config()
database_config = config["database"]
# Database connection details (replace with your actual credentials)
mydb = mysql.connector.connect(
  host=database_config["host"],
  user=database_config["user"],
  password=database_config["password"],
  database=database_config["database_name"],
)

mycursor = mydb.cursor()

# Sample facts as a list of tuples
facts_to_insert = [
    
    
]

for index, (fact_text, category) in enumerate(facts_to_insert):
  sql = "INSERT INTO facts (fact_text, category, tweeted) VALUES (%s, %s, %s)"
  mycursor.execute(sql, (fact_text, category, False))
  print(f"Inserting fact {index+1}")  # Print loop iteration count


mydb.commit()  # Commit the changes

print("Facts inserted successfully!")

mycursor.close()
mydb.close()