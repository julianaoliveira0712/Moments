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
            "message": "Moment não existe ou usuário não existe"
        }
    }

    if(moment == None or moment["owner"] != headerRequest):
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )   
    else:
        db.moment.delete_one({ "_id" : ObjectId (id_moment)})
        response = {
            "success": True,
            "content": None,
            "erroData": None
        }
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

# Inserir comentário no moment
@app.route('/<id_moment>', methods = ['POST'])
def insertCommentMoment(id_moment):
    headerRequest =request.headers.get("user_id")
    bodyRequest = request.json
    db.comment.insert_one({
        "creationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "owner": headerRequest,
        "content": bodyRequest,
        "idMoment": id_moment,
        "answer":[]
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

# Responder comentário
@app.route('/<id_moment>/comment/<id_comment>', methods = ['POST'])
def answerCommentMoment(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    bodyRequest = request.json
    insert = db.comment.insert_one({
        "creationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "owner": headerRequest,
        "content": bodyRequest,
        "idMoment": id_moment,
        "answer":[]
    })   
    initialComment = db.comment.find_one({ "_id" : ObjectId (id_comment)})
    answer = initialComment["answer"]
    answer.append(insert["insertedId"])
    db.comment.update_one(
        {
             "_id" : ObjectId (id_comment)
        },
        {
            "$set": {
                "answer": answer
            }
        }
    )
    response = {
        "success": True,
        "content": None,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )

# Apagar um comentário
@app.route('/<id_moment>/comment/<id_comment>', methods = ['DELETE'])
def answerCommentMoment(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    comment = db.comment.find_one({ "_id" : ObjectId (id_comment)})
    response = {
        "success": False,
        "content": None,
        "erroData": {
            "typeError": "Unathourized",
            "message": "comentário não existe ou usuário inexistente"
        }
    }

    if(comment == None or comment["owner"] != headerRequest):
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )   
    else:
        db.comment.delete_one({ "_id" : ObjectId (id_comment)})
        response = {
            "success": True,
            "content": None,
            "erroData": None
        }
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )    

# Editar um comentário
@app.route('/<id_moment>/comment/<id_comment>', methods = ['PUT'])
def updateCommentMoment(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    bodyRequest = request.json
    initialComment = db.comment.find_one({ "_id" : ObjectId (id_comment)})
    content = initialComment["content"]
    db.comment.update_one(
        {
             "_id" : ObjectId (id_comment)
        },
        {
            "$set": {
                "content": bodyRequest
            }
        }
    )
    response = {
        "success": True,
        "content": None,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )

# Comentários de um moment
@app.route('/<id_moment>/comment/<id_comment>', methods = ['GET'])
def getCommentMoment(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    query = db.comment.find()
    response = {
        "success": True,
        "content": None,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )

# Pegar um comentário especifico de um moment
@app.route('/<id_moment>/comment/<id_comment>', methods = ['GET'])
def getSpecificCommentMoment(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    query = db.comment.find_one({ "_id" : ObjectId (id_comment)})
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







