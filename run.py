from blog import app
#  parla proprio di "app variable"
import os

app.secret_key = os.urandom(24)
port = int(os.environ.get("PORT", 5000))
# heroku ci fornisce una variabile ambintale che è la porta su cui facciamo girare la app

app.run(host="0.0.0.0"), port=port)
# cambiat da tutorial per il push su jeroku
# app.run(debug=True)