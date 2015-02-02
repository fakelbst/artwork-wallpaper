#!/usr/bin/env python
from app import app

if __name__ == "__main__": 
    app.secret_key = 'e1d840e6dbbe79ceda0c8070f97a5808dc4890f2232f96dc'
    app.run(debug = True, host='0.0.0.0')
