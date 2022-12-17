from flask import Flask

app = Flask(name)

@app.route('/')

def hello_world():
  
  return 'UniqxDev'

if name == 'main':
  
  app.run()
  
