from flask import Flask
from resoucers import *
from flask import json
from flask import request
from bson import json_util, ObjectId
from datetime import datetime
app = Flask(__name__)

# Apagar um moment de uma memoryLine
@app.route('/<id_moment>', methods = ['DELETE'])
def deleteMoment(id_moment):
    headerRequest = request.headers.get("user_id")
    moment = db.moment.find_one({ "_id" : ObjectId (id_moment)})
    response = {
        "success": False,
        "content": None,
        "erroData": {
            "typeError": "Unathourized",
            "Moment não existe ou usuário não existe"
        }
    }

    if(moment == None or moment["owner"] != headerRequest):
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )   



# inserir uma moment numa memorie line
@app.route('/<id_memory_line>', methods = ['POST'])
def insertmoment(id_memory_line):
    headerRequest = request.headers.get("user_id")
    bodyRequest = request.json
    db.moment.insert_one({
        "owner": headerRequest
        "type": bodyRequest["typeMoment"],  
        "urlBucket": bodyRequest["urlBucket"],
        "creationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "description": bodyRequest["description"]
    })
    response = {
        "success": True,
        "content": None,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )

# Reagir a um comentário


# Atualizar uma reação no comentário

# Apagar uma reação no comentário

# Reações de um moments

# Reações de um comentário

# Reagir a um moment

# Atualizar reação de um moment

# Apagar reação de um moment

# Inserir comentário no moment

# Responder comentário

# Apagar um comentário

# Editar um comentário

# Comentários de um moment






