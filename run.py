from blog import app
#  parla proprio di "app variable"
import os

# aggiunti da tutorial per il push su jeroku
app.secret_key = os.urandom(24)
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)
# heroku ci fornisce una variabile ambintale che è la porta su cui facciamo girare la app


# tolto da tutorial per il push su jeroku
# app.run(debug=True)