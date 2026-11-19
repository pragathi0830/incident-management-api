Incident Management REST API



A backend REST API built with Python, Flask and SQLite to manage IT incidents, similar to the incident module in ServiceNow.



Features

\- Create, list, view, update and delete incidents

\- Validation for priority and status values

\- Parameterized SQL queries to prevent SQL injection

\- Proper HTTP status codes (201, 400, 404)



Tech stack

Python 3.7, Flask, SQLite



How to run

1\. Create a virtual environment: python -m venv venv

2\. Activate it: venv\\Scripts\\activate

3\. Install libraries: pip install -r requirements.txt

4\. Start the server: python app.py

5\. The API runs at http://127.0.0.1:5000



Endpoints

POST   /incidents        Create an incident

GET    /incidents        List all incidents

GET    /incidents/<id>   Get one incident

PATCH  /incidents/<id>   Update an incident

DELETE /incidents/<id>   Delete an incident



Allowed values

Priority: Low, Medium, High, Critical

Status: New, In Progress, Resolved, Closed



Example request (Windows Command Prompt)

curl.exe -X POST http://127.0.0.1:5000/incidents -H "Content-Type: application/json" -d "{\\"title\\": \\"Printer offline\\", \\"priority\\": \\"Medium\\"}"

