#!/usr/bin/env python3
"""
🔌 API BATCH EXTENSION - Advanced DD-AI v2.1
============================================

Extensão para adicionar endpoints inteligentes de análise em lote
que se integram ao sql_api.py principal.

Endpoints:
- POST /api/smart-batch-analysis - Análise inteligente em lote
- POST /api/sql-to-smart-batch   - SQL query → análise automática
- POST /api/detect-data-type     - Detecta tipo de dados
"""

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import re

# Modelos para a API
class AnalysisStrategyAPI(str, Enum):
    AUTO_DETECT = "auto_detect"
    CNPJ_ONLY = "cnpj_only"
    COMPANY_NAME_ONLY = "company_name_only"
    HYBRID = "hybrid"

class SmartBatchRequestAPI(BaseModel):
    data_items: List[Union[str, Dict[str, str]]]
    analysis_strategy: AnalysisStrategyAPI = AnalysisStrategyAPI.AUTO_DETECT
    include_news: bool = True
    include_enrichment: bool = True
    max_concurrent: int = 5
    column_mapping: Optional[Dict[str, str]] = None

class SQLToSmartBatchRequest(BaseModel):
    connection: Dict[str, Any]  # ConnectionDetails
    query: str
    analysis_strategy: AnalysisStrategyAPI = AnalysisStrategyAPI.AUTO_DETECT
    include_news: bool = True
    include_enrichment: bool = True
    max_concurrent: int = 5
    column_mapping: Optional[Dict[str, str]] = None
    auto_detect_columns: bool = True

class DataTypeDetectionRequest(BaseModel):
    data_items: List[str]

class DataTypeDetectionResponse(BaseModel):
    detections: List[Dict[str, Any]]
    summary: Dict[str, int]
    recommendations: Dict[str, str]

def add_smart_batch_endpoints(app, get_db_connection_string_func):
    """
    Adiciona endpoints inteligentes à aplicação FastAPI
    """
    
    @app.post("/api/detect-data-type", response_model=DataTypeDetectionResponse)
    async def detect_data_type(request: DataTypeDetectionRequest):
        """
        Detecta automaticamente o tipo de dados (CNPJ vs Nome da Empresa)
        """
        try:
            from smart_batch_analyzer import SmartBatchAnalyzer
            
            analyzer = SmartBatchAnalyzer()
            detections = []
            type_counts = {"CNPJ": 0, "COMPANY_NAME": 0, "UNKNOWN": 0}
            
            for item in request.data_items:
                data_type, confidence = analyzer.detect_data_type(item)
                
                detection = {
                    "original_value": item,
                    "detected_type": data_type.value,
                    "confidence": confidence,
                    "explanation": _get_detection_explanation(item, data_type, confidence)
                }
                
                detections.append(detection)
                type_counts[data_type.value.upper()] += 1
            
            # Gerar recomendações
            recommendations = _generate_strategy_recommendations(type_counts, len(request.data_items))
            
            return DataTypeDetectionResponse(
                detections=detections,
                summary=type_counts,
                recommendations=recommendations
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na detecção: {str(e)}")
    
    @app.post("/api/smart-batch-analysis")
    async def smart_batch_analysis(request: SmartBatchRequestAPI):
        """
        Análise inteligente em lote que escolhe automaticamente a melhor estratégia
        """
        try:
            print(f"🧠 Iniciando análise inteligente de {len(request.data_items)} items...")
            
            from smart_batch_analyzer import SmartBatchAnalyzer, SmartBatchRequest, AnalysisStrategy
            
            # Converter enum da API para enum interno
            strategy_mapping = {
                AnalysisStrategyAPI.AUTO_DETECT: AnalysisStrategy.AUTO_DETECT,
                AnalysisStrategyAPI.CNPJ_ONLY: AnalysisStrategy.CNPJ_ONLY,
                AnalysisStrategyAPI.COMPANY_NAME_ONLY: AnalysisStrategy.COMPANY_NAME_ONLY,
                AnalysisStrategyAPI.HYBRID: AnalysisStrategy.HYBRID
            }
            
            analyzer = SmartBatchAnalyzer()
            
            # Criar requisição interna
            smart_request = SmartBatchRequest(
                data_items=request.data_items,
                analysis_strategy=strategy_mapping[request.analysis_strategy],
                include_news=request.include_news,
                include_enrichment=request.include_enrichment,
                max_concurrent=request.max_concurrent,
                column_mapping=request.column_mapping
            )
            
            # Executar análise
            results = analyzer.process_smart_batch(smart_request)
            
            print(f"✅ Análise concluída: {results['summary']['companies_analyzed']} items processados")
            
            return results
            
        except Exception as e:
            print(f"❌ Erro na análise inteligente: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")
    
    @app.post("/api/sql-to-smart-batch")
    async def sql_to_smart_batch(request: SQLToSmartBatchRequest):
        """
        Executa query SQL e aplica análise inteligente automaticamente
        """
        try:
            import pyodbc
            
            print(f"🔍 Executando query SQL para análise inteligente...")
            
            # 1. Executar query SQL
            conn_str = get_db_connection_string_func(request.connection)
            
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(request.query)
                
                # Obter colunas e dados
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                
                # Converter para lista de dicionários
                sql_results = []
                for row in rows:
                    sql_results.append(dict(zip(columns, row)))
                
                print(f"✅ Query executada: {len(sql_results)} registros")
            
            # 2. Detectar colunas automaticamente ou usar mapeamento
            if request.auto_detect_columns:
                detected_mapping = _auto_detect_columns(columns, sql_results)
                column_mapping = detected_mapping
                print(f"🔍 Colunas detectadas: {column_mapping}")
            else:
                column_mapping = request.column_mapping or {}
            
            # 3. Preparar dados para análise inteligente
            data_items = []
            
            for row in sql_results:
                # Criar item com todas as colunas relevantes
                if column_mapping:
                    item_data = {}
                    for api_col, sql_col in column_mapping.items():
                        if sql_col in row:
                            item_data[api_col] = row[sql_col]
                    
                    if item_data:
                        data_items.append(item_data)
                else:
                    # Fallback: tentar detectar automaticamente
                    potential_cnpj = None
                    potential_name = None
                    
                    for key, value in row.items():
                        if isinstance(value, str):
                            # Verificar se é CNPJ
                            if re.match(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}', value):
                                potential_cnpj = value
                            # Verificar se pode ser nome de empresa
                            elif len(value) > 10 and any(word in value.lower() for word in ['ltda', 'sa', 'eireli', 'fundo']):
                                potential_name = value
                    
                    if potential_cnpj or potential_name:
                        item_data = {}
                        if potential_cnpj:
                            item_data['cnpj'] = potential_cnpj
                        if potential_name:
                            item_data['razao_social'] = potential_name
                        data_items.append(item_data)
            
            print(f"📊 Preparados {len(data_items)} items para análise")
            
            # 4. Executar análise inteligente
            from smart_batch_analyzer import SmartBatchAnalyzer, SmartBatchRequest, AnalysisStrategy
            
            strategy_mapping = {
                AnalysisStrategyAPI.AUTO_DETECT: AnalysisStrategy.AUTO_DETECT,
                AnalysisStrategyAPI.CNPJ_ONLY: AnalysisStrategy.CNPJ_ONLY,
                AnalysisStrategyAPI.COMPANY_NAME_ONLY: AnalysisStrategy.COMPANY_NAME_ONLY,
                AnalysisStrategyAPI.HYBRID: AnalysisStrategy.HYBRID
            }
            
            analyzer = SmartBatchAnalyzer()
            
            smart_request = SmartBatchRequest(
                data_items=data_items,
                analysis_strategy=strategy_mapping[request.analysis_strategy],
                include_news=request.include_news,
                include_enrichment=request.include_enrichment,
                max_concurrent=request.max_concurrent,
                column_mapping={'cnpj_col': 'cnpj', 'name_col': 'razao_social'}
            )
            
            results = analyzer.process_smart_batch(smart_request)
            
            # 5. Adicionar metadados da query SQL
            results['sql_metadata'] = {
                'query': request.query,
                'total_sql_records': len(sql_results),
                'columns_detected': column_mapping,
                'items_processed': len(data_items)
            }
            
            print(f"✅ Análise SQL→IA concluída: {results['summary']['companies_analyzed']} empresas")
            
            return results
            
        except Exception as e:
            print(f"❌ Erro na análise SQL→IA: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

def _get_detection_explanation(value: str, data_type, confidence: float) -> str:
    """Gera explicação para a detecção"""
    if data_type.value == "cnpj":
        return f"Detectado padrão de CNPJ (confiança: {confidence:.1%})"
    elif data_type.value == "company_name":
        return f"Detectado nome de empresa (confiança: {confidence:.1%})"
    else:
        return f"Tipo não identificado (confiança: {confidence:.1%})"

def _generate_strategy_recommendations(type_counts: Dict, total_items: int) -> Dict[str, str]:
    """Gera recomendações de estratégia baseadas na distribuição dos tipos"""
    cnpj_ratio = type_counts["CNPJ"] / total_items
    name_ratio = type_counts["COMPANY_NAME"] / total_items
    
    recommendations = {}
    
    if cnpj_ratio > 0.8:
        recommendations["primary"] = "cnpj_only"
        recommendations["reason"] = "Maioria dos dados são CNPJs - use enriquecimento via API Brasil"
    elif name_ratio > 0.8:
        recommendations["primary"] = "company_name_only"
        recommendations["reason"] = "Maioria dos dados são nomes - use busca direta por notícias"
    elif cnpj_ratio > 0.3 and name_ratio > 0.3:
        recommendations["primary"] = "hybrid"
        recommendations["reason"] = "Dados mistos - use estratégia híbrida"
    else:
        recommendations["primary"] = "auto_detect"
        recommendations["reason"] = "Dados variados - deixe o sistema escolher automaticamente"
    
    recommendations["cnpj_percentage"] = f"{cnpj_ratio:.1%}"
    recommendations["name_percentage"] = f"{name_ratio:.1%}"
    
    return recommendations

def _auto_detect_columns(columns: List[str], sample_data: List[Dict]) -> Dict[str, str]:
    """Detecta automaticamente colunas de CNPJ e nome"""
    mapping = {}
    
    # Padrões para detectar colunas
    cnpj_patterns = ['cnpj', 'id_unico', 'documento', 'cpf_cnpj']
    name_patterns = ['razao_social', 'nome', 'empresa', 'denominacao', 'social']
    
    # Buscar por padrões nos nomes das colunas
    for col in columns:
        col_lower = col.lower()
        
        # Detectar coluna de CNPJ
        if any(pattern in col_lower for pattern in cnpj_patterns):
            mapping['cnpj_col'] = col
        
        # Detectar coluna de nome
        if any(pattern in col_lower for pattern in name_patterns):
            mapping['name_col'] = col
    
    # Se não encontrou por nome, analisar conteúdo de algumas linhas
    if not mapping and sample_data:
        for col in columns:
            sample_values = [row.get(col, '') for row in sample_data[:5] if row.get(col)]
            
            if sample_values:
                # Verificar se contém CNPJs
                cnpj_count = sum(1 for val in sample_values 
                               if isinstance(val, str) and re.match(r'\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}', val))
                
                # Verificar se contém nomes de empresas
                name_indicators = ['ltda', 'sa', 's.a.', 'eireli', 'fundo', 'gestora']
                name_count = sum(1 for val in sample_values 
                               if isinstance(val, str) and any(ind in val.lower() for ind in name_indicators))
                
                if cnpj_count >= len(sample_values) * 0.6:  # 60% são CNPJs
                    mapping['cnpj_col'] = col
                elif name_count >= len(sample_values) * 0.4:  # 40% têm indicadores de empresa
                    mapping['name_col'] = col
    
    return mapping
