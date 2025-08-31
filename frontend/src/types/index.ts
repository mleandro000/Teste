export interface DatabaseConnection {
  id?: number;
  connection_name: string;
  db_type: string;
  server_address: string;
  port: number;
  database_name: string;
  use_windows_auth: boolean;
  username?: string;
  encrypted_password?: string;
}

export interface MonitoredEntity {
  id?: number;
  name: string;
  entity_type: string;
  created_at?: string;
}

export interface ExecucaoJob {
  id?: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  tipo_gatilho: string;
  iniciado_em?: string;
  finalizado_em?: string;
  resultado?: string;
}

export interface AnalysisPayload {
  entities: string[];
  keywords: string[];
  start_date: string;
  end_date: string;
  connection_id: number;
}

export interface Finding {
  id: number;
  entity_name: string;
  source_url: string;
  title: string;
  content: string;
  risk_score: number;
  risk_level: 'BAIXO' | 'MÉDIO' | 'ALTO';
  data_coleta: string;
  categoria: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface CacheStats {
  total_entries: number;
  cache_hits: number;
  cache_misses: number;
  hit_rate: number;
  size_mb: number;
}

export interface RiskPolicy {
  id: string;
  name: string;
  category: string;
  keywords: string[];
  weight: number;
  auto_block: boolean;
  sources: string[];
}

export interface MonitoringJob {
  id: string;
  name: string;
  entities: string[];
  keywords: string[];
  schedule_type: 'daily' | 'weekly' | 'monthly';
  schedule_time: string;
  is_active: boolean;
  last_execution?: string;
  next_execution?: string;
}
