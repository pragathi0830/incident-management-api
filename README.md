Incident Management API



This is a small project I made to learn backend development with Python. It is a REST API for managing IT incidents, a bit like the incident module in ServiceNow, which I have worked with before.



I used Python, Flask and SQLite. The data is stored in a file called incidents.db, and the app creates this file by itself when it starts.



What it can do



You can create an incident, see all the incidents, see one incident, change an incident and delete an incident.



Every incident has a title, a description, a priority, a status and the time it was created.



Priority can be Low, Medium, High or Critical. Status can be New, In Progress, Resolved or Closed. If someone sends any other value, the API sends back an error message with status code 400. If the incident id does not exist, it sends back 404.



I wrote the SQL queries with question marks instead of joining the user input into the query text, so it is safe from SQL injection.



How to run it



I used Windows and Python 3.7. Open Command Prompt in the project folder and run these one by one:



&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\activate

&#x20;   pip install -r requirements.txt

&#x20;   python app.py



After that the API runs at http://127.0.0.1:5000



Endpoints



&#x20;   POST    /incidents

&#x20;   GET     /incidents

&#x20;   GET     /incidents/<id>

&#x20;   PATCH   /incidents/<id>

&#x20;   DELETE  /incidents/<id>



Examples



To create an incident:



&#x20;   curl.exe -X POST http://127.0.0.1:5000/incidents -H "Content-Type: application/json" -d "{\\"title\\": \\"Printer offline\\", \\"priority\\": \\"Medium\\"}"



To change the status of incident 1:



&#x20;   curl.exe -X PATCH http://127.0.0.1:5000/incidents/1 -H "Content-Type: application/json" -d "{\\"status\\": \\"In Progress\\"}"



To see all incidents:



&#x20;   curl.exe http://127.0.0.1:5000/incidents

