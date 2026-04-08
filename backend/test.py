import requests
import json

tickets = [
    {"title": "Payment gateway timeout", "description": "Users getting timeout on checkout", "priority": "High", "assignee": "Jane Smith", "category": "Bug"},
    {"title": "Dark mode not working", "description": "Dark mode toggle has no effect", "priority": "Low", "assignee": "John Doe", "category": "Bug"},
    {"title": "Export to CSV feature", "description": "Users need CSV export for reports", "priority": "Medium", "assignee": "Alice Wong", "category": "Feature"},
    {"title": "Mobile app crash on iOS 17", "description": "App crashes on launch for iOS 17 users", "priority": "High", "assignee": "Bob Lee", "category": "Bug"},
    {"title": "Email notifications delayed", "description": "Notification emails arriving 2 hours late", "priority": "Medium", "assignee": "Jane Smith", "category": "General"},
    {"title": "Dashboard loading slowly", "description": "Dashboard takes 10+ seconds to load", "priority": "High", "assignee": "Alice Wong", "category": "Bug"},
    {"title": "Add bulk ticket assignment", "description": "Allow assigning multiple tickets at once", "priority": "Low", "assignee": "John Doe", "category": "Feature"},
    {"title": "SSO integration with Okta", "description": "Enterprise clients need Okta SSO", "priority": "High", "assignee": "Bob Lee", "category": "Security"},
    {"title": "Password reset not sending email", "description": "Reset email never arrives", "priority": "Medium", "assignee": "Jane Smith", "category": "Bug"},
    {"title": "API rate limit documentation", "description": "Docs missing rate limit info", "priority": "Low", "assignee": "Alice Wong", "category": "General"},
]

for t in tickets:
    payload = json.dumps({"action": "create_ticket", **t})
    r = requests.post("http://localhost:8000/generate-ui", json={"query": payload})
    print(r.status_code, t["title"])