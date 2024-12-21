import pyodbc
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Połączenie z bazą danych Azure SQL
def check_plate_in_database(plate_number):
    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=smart-parkomat.database.windows.net,1443;"
        "Database=smart-parkomat-db;"
        "Uid=SmartAdmin;"
        "Pwd=Parkomat123!;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plates WHERE plate_number = ?", (plate_number,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Analiza obrazu za pomocą Azure Computer Vision
image_url = "https://example.com/plate.jpg"
credentials = CognitiveServicesCredentials("<YOUR_SUBSCRIPTION_KEY>")
client = ComputerVisionClient("<YOUR_ENDPOINT>", credentials)

# OCR
read_response = client.read(image_url, raw=True)
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break

# Sprawdzenie numeru
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            if any(char.isdigit() for char in line.text) and any(char.isalpha() for char in line.text):
                plate_number = line.text
                print("Wykryto numer:", plate_number)
                
                if check_plate_in_database(plate_number):
                    print("Numer znajduje się w bazie!")
                else:
                    print("Numer NIE znajduje się w bazie.")
