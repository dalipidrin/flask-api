# 🏦 Validata API

The Validata REST API for managing banks. This API allows you to create, update, delete, list, and retrieve bank details. 
It uses **Microsoft SQL Server** as the database and **SQLAlchemy** as the ORM.

---

## 🚀 Getting Started

### 1. Run Microsoft SQL Server in Docker

#### Pull the SQL Server image
```bash
docker pull mcr.microsoft.com/mssql/server:2022-latest
```

#### Run SQL Server container
```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=<your_password>" -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2022-latest
```

### 2. Create the Database and Table
Connect to SQL Server and execute the following SQL script:

```sql
-- Create database
CREATE DATABASE validataDb;
GO

-- Use the new database
USE validataDb;
GO

-- Create Banks table
CREATE TABLE banks (
    id uniqueidentifier PRIMARY KEY DEFAULT NEWID(),
    name VARCHAR(100),
    location VARCHAR(100)
);
GO
```
### 3. Set the database connection variables `.env`
```env
DB_SERVER=127.0.0.1,1433
DB_NAME=validataDb
DB_USER=sa
DB_PASSWORD=<your_password>
DB_DRIVER=ODBC Driver 18 for SQL Server
```

### 4. Activate the virtual environment which contains the necessary libraries and dependencies
```bash
# On macOS and Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 5. Start the Flask app
Navigate to the project folder and run the Flask server:
```bash
cd src/main
flask --app app run
```


## 📡 Available endpoints

Endpoint to create a bank:

```bash
curl -X POST "http://localhost:5000/api/banks" \
     -H "Content-Type: application/json" \
     -d '{"name": "TEB", "location": "Kosovo"}'
```

Endpoint to list all banks:

```bash
curl -X GET "http://localhost:5000/api/banks"
```

Endpoint to get bank details:

```bash
curl -X GET "http://localhost:5000/api/banks/<bank_id>" # <bank_id> should be a UUID
```

Endpoint to update a bank:

```bash
curl -X PUT "http://localhost:5000/api/banks/<bank_id>" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Bank Name", "location": "New Location"}'
```

Endpoint to delete a bank:

```bash
curl -X DELETE "http://localhost:5000/api/banks/<bank_id>"
```

## 📜 API client script
The project also contains a script `api_client.py` which interacts with the Bank API using HTTP requests to create, read, update, and delete 
bank records. 

The script can be run like this:
```bash
cd src
python api_client.py
```

## 🧪 Testing
Unit tests are located under `test` folder.

## 📚 Additional libraries used within the project

- Flask
- Flask-SQLAlchemy
- Pydantic
- Pytest
- python-dotenv
