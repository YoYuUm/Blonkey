#!flask/bin/python
from app import app
import os
if os.environ['PORT'] is None:
    app.run(debug = True)    
else:
    app.run(debug = True, port = int(os.environ['PORT']) )
