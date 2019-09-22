from flask import Flask
from resoucers import *
from flask import json
from flask import request
from bson import json_util, ObjectId
from datetime import datetime
from enum import Enum
app = Flask(__name__)

class TypeReactions(Enum):
    AMEI = 0
    SAUDADES = 1
    NOSTALGICO = 2
    TRISTE = 3
    HAHA = 4
    NEM_LEMBRO = 5

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
@app.route('/<id_moment>/comment', methods = ['POST'])
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
def deleteCommentMoment(id_moment,id_comment):
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
@app.route('/<id_moment>/comment/', methods = ['GET'])
def getCommentMoment(id_moment):
    headerRequest =request.headers.get("user_id")
    comments = db.comment.find({"idMoment": id_moment})
    commentsResponse = []
    for row in comments:
        commentsResponse.append({
            "idComment": row['_id'],
            "content": row['content'],
            "owner": row['owner'],
            "creationDate": row['creationDate'],
            "answers": len(row['answer']),
            "idMoment": row['idMoment']
        })
    response = {
        "success": True,
        "content": commentsResponse,
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
    comment = {
            "idComment": query['_id'],
            "content": query['content'],
            "owner": query['owner'],
            "creationDate": query['creationDate'],
            "answers": len(query['answer']),
            "idMoment": query['idMoment']
        }
    response = {
        "success": True,
        "content": comment,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )

# Reagir a um alvo (moments ou comments)
@app.route('<id_target>/reactions', methods = ['POST'])
def insertReactTarget(id_target):
    headerRequest =request.headers.get("user_id")
    bodyRequest = request.json
    react = db.reaction.insert_one({
       "typeReaction": bodyRequest['type'],
       "idTarget": id_target,
        "owner": headerRequest,
       "target": bodyRequest['target']
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

# Atualizar uma reação em um alvo (moments ou comments)
@app.route('<id_target>/reactions', methods = ['PUT'])
def updateReactTarget(id_target):
    headerRequest =request.headers.get("user_id")
    bodyRequest = request.json
    db.reaction.update_one(
        {
             "_id" : ObjectId (id_target)
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

# Apagar uma reação em um alvo (moments ou comments)
@app.route('<id_target>/reactions', methods = ['DELETE'])
def deleteReactTarget(id_moment,id_comment):
    headerRequest =request.headers.get("user_id")
    react = db.reaction.find_one({ "_id" : ObjectId (id_comment)})
    response = {
        "success": False,
        "content": None,
        "erroData": {
            "typeError": "Unathourized",
            "message": "reação ou usuário inexistente"
        }
    }

    if(react == None or react["owner"] != headerRequest):
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )   
    else:
        db.reation.delete_one({ "_id" : ObjectId (id_comment)})
        response = {
            "success": True,
            "content": None,
            "erroData": None
        }
        return app.response_class(
            response = json.dumps(response, default = json_util.default),
            mimetype="application/json"
        )  

# Reações de um alvo ( moments ou comments)
@app.route('<id_target>/reactions', methods = ['GET'])
def getReactTarget(id_target):
    headerRequest = request.headers.get("user_id")
    reactions = db.react.find({"idTarget": id_target})
    reactionsResponse = []
    for reaction in TypeReactions:
        reactionsResponse.append(0)

    for row in reactions:
       for i, reaction in enumerate(TypeReactions):
           if("TypeReactions." + row['typeReaction'] == reaction):
                reactionsResponse[i] = reactionsResponse[i] + 1 
                break

    reactionsObjects = []
    
    for i, reaction in enumerate(reactionsResponse):
        reactionsObjects.append({
            "type": TypeReactions(i),
            "quantity": reactionsResponse[i]
        })

    response = {
        "success": True,
        "content": reactionsObjects,
        "erroData": None
    }
    return app.response_class(
        response = json.dumps(response, default = json_util.default),
        mimetype="application/json"
    )