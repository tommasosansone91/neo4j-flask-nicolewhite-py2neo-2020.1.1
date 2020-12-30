from blog import app
#  parla proprio di "app variable"
import os

#   enable to use on heroku, disable otherwise

app.secret_key = os.urandom(24)
port = int(os.environ.get("PORT", 5000))

app.run(host="0.0.0.0", port=port, debug=True)
#   heroku ci fornisce una variabile ambintale che è la porta su cui facciamo girare la app


#   enable to use locally, disable otherwise
# app.run(debug=True)