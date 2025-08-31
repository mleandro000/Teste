#!/usr/bin/env python3
"""
Versão simplificada do backend para teste
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import traceback

# Versão simplificada
app = FastAPI(title="DD-AI SQL Server API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ConnectionDetails(BaseModel):
    server: str
    database: str
    port: int = 1433
    use_windows_auth: bool = True
    username: Optional[str] = None
    password: Optional[str] = None

class QueryRequest(BaseModel):
    connection: ConnectionDetails
    query: str

def get_db_connection_string(connection: ConnectionDetails) -> str:
    """Gera string de conexão para SQL Server"""
    if connection.use_windows_auth:
        return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={connection.server};DATABASE={connection.database};Trusted_Connection=yes;"
    else:
        return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={connection.server};DATABASE={connection.database};UID={connection.username};PWD={connection.password};"

# Endpoint básico de teste
@app.get("/")
async def root():
    return {"message": "DD-AI SQL Server API v3.0.0 - Funcionando!"}

# Endpoint de teste de conexão
@app.post("/api/test-connection")
async def test_connection(connection: ConnectionDetails) -> Dict[str, Any]:
    """Testa conexão com SQL Server"""
    try:
        connection_string = get_db_connection_string(connection)
        cnx = pyodbc.connect(connection_string)
        cursor = cnx.cursor()
        
        # Teste simples
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()
        
        cursor.close()
        cnx.close()
        
        return {
            "success": True,
            "message": "Conexão estabelecida com sucesso!",
            "server_version": version[0] if version else "Desconhecida",
            "database": connection.database
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Erro na conexão: {str(e)}"
        }

# Endpoint de execução de query
@app.post("/api/execute-query")
async def execute_query(request: QueryRequest) -> Dict[str, Any]:
    """Executa query SQL"""
    try:
        connection_string = get_db_connection_string(request.connection)
        cnx = pyodbc.connect(connection_string)
        cursor = cnx.cursor()
        
        cursor.execute(request.query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        
        # Converter para lista de dicionários
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        
        cursor.close()
        cnx.close()
        
        return {
            "success": True,
            "message": f"Query executada com sucesso! Retornou {len(data)} linhas.",
            "columns": columns,
            "data": data,
            "row_count": len(data)
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Erro ao executar query: {str(e)}"
        }

# Endpoint de listagem de tabelas
@app.post("/api/tables")
async def list_tables(connection: ConnectionDetails) -> Dict[str, Any]:
    """Lista tabelas do banco de dados"""
    try:
        connection_string = get_db_connection_string(connection)
        cnx = pyodbc.connect(connection_string)
        cursor = cnx.cursor()
        
        # Query para listar tabelas
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """
        
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        cnx.close()
        
        return {
            "success": True,
            "message": f"Encontradas {len(tables)} tabelas",
            "tables": tables
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Erro ao listar tabelas: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 Iniciando DD-AI SQL Server API v3.0.0 (Versão Simplificada)")
    print("🌐 Endpoints disponíveis:")
    print("   - GET  / (Teste básico)")
    print("   - POST /api/test-connection")
    print("   - POST /api/execute-query")
    print("   - POST /api/tables")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
