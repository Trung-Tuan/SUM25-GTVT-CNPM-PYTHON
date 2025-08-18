from flask import Blueprint, request, jsonify
from services.todo_service import TodoService
from infrastructure.repositories.todo_repository import TodoRepository
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session
from flask import Blueprint

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/', methods=['GET'])
def hello_world():
    """
    Hello World endpoint
    ---
    get:
      summary: Returns hello world
      responses:
        200:
          description: Success
          content:
            text/plain:
              schema:
                type: string
                example: hello world
    """
    return 'hello world'