import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  Settings, 
  Calendar,
  Search,
  Database,
  Target,
  Zap
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import type { AnalysisPayload } from '../types';

const ExecutionPanel: React.FC = () => {
  const { 
    connections, 
    entities, 
    selectedConnection, 
    selectedEntities, 
    keywords, 
    dateRange,
    setSelectedConnection,
    setSelectedEntities,
    setKeywords,
    setDateRange
  } = useAppStore();

  const [localKeywords, setLocalKeywords] = useState(keywords.join(', '));
  const [isExecuting, setIsExecuting] = useState(false);

  React.useEffect(() => {
    setLocalKeywords(keywords.join(', '));
  }, [keywords]);

  const handleExecute = async () => {
    if (!selectedConnection || selectedEntities.length === 0) {
      alert('Selecione uma conexão e pelo menos uma entidade');
      return;
    }

    const keywordList = localKeywords
      .split(',')
      .map(k => k.trim())
      .filter(k => k.length > 0);

    setKeywords(keywordList);
    setIsExecuting(true);

    try {
      const payload: AnalysisPayload = {
        entities: selectedEntities,
        keywords: keywordList,
        start_date: dateRange.start,
        end_date: dateRange.end,
        connection_id: selectedConnection
      };

      // TODO: Implement analysis execution
      console.log('Executing analysis with payload:', payload);
      
      // Simulate execution
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      alert('Análise iniciada com sucesso!');
    } catch (error) {
      console.error('Erro ao executar análise:', error);
      alert('Erro ao executar análise');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleEntityToggle = (entityName: string) => {
    const newSelected = selectedEntities.includes(entityName)
      ? selectedEntities.filter(e => e !== entityName)
      : [...selectedEntities, entityName];
    setSelectedEntities(newSelected);
  };

  const handleSelectAllEntities = () => {
    const allEntityNames = entities.map(e => e.name);
    setSelectedEntities(allEntityNames);
  };

  const handleDeselectAllEntities = () => {
    setSelectedEntities([]);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-aurora-accent rounded-lg flex items-center justify-center">
            <Play className="w-6 h-6 text-black" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-aurora-text">Execução de Análise</h2>
            <p className="text-sm text-aurora-text-muted">Configure e execute a análise de due diligence</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column - Configuration */}
        <div className="space-y-6">
          {/* Connection Selection */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="aurora-card"
          >
            <div className="flex items-center space-x-2 mb-4">
              <Database className="w-5 h-5 text-aurora-accent" />
              <h3 className="text-lg font-semibold text-aurora-text">Conexão de Banco</h3>
            </div>
            
            <select
              value={selectedConnection || ''}
              onChange={(e) => setSelectedConnection(parseInt(e.target.value) || null)}
              className="aurora-input w-full"
            >
              <option value="">Selecione uma conexão</option>
              {connections.map((conn) => (
                <option key={conn.id} value={conn.id}>
                  {conn.connection_name} ({conn.server_address}:{conn.port})
                </option>
              ))}
            </select>
          </motion.div>

          {/* Entity Selection */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="aurora-card"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Target className="w-5 h-5 text-aurora-accent" />
                <h3 className="text-lg font-semibold text-aurora-text">Entidades Alvo</h3>
              </div>
              <div className="flex space-x-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSelectAllEntities}
                  className="aurora-button-secondary text-xs px-2 py-1"
                >
                  Todos
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleDeselectAllEntities}
                  className="aurora-button-secondary text-xs px-2 py-1"
                >
                  Nenhum
                </motion.button>
              </div>
            </div>
            
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {entities.map((entity) => (
                <label key={entity.id} className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedEntities.includes(entity.name)}
                    onChange={() => handleEntityToggle(entity.name)}
                    className="w-4 h-4 text-aurora-accent bg-aurora-glass border-aurora-border rounded focus:ring-aurora-accent"
                  />
                  <span className="text-aurora-text">{entity.name}</span>
                  <span className="text-xs text-aurora-text-muted">({entity.entity_type})</span>
                </label>
              ))}
            </div>
            
            {entities.length === 0 && (
              <p className="text-sm text-aurora-text-muted text-center py-4">
                Nenhuma entidade configurada
              </p>
            )}
          </motion.div>

          {/* Keywords */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="aurora-card"
          >
            <div className="flex items-center space-x-2 mb-4">
              <Search className="w-5 h-5 text-aurora-accent" />
              <h3 className="text-lg font-semibold text-aurora-text">Palavras-Chave</h3>
            </div>
            
            <textarea
              value={localKeywords}
              onChange={(e) => setLocalKeywords(e.target.value)}
              className="aurora-input w-full h-24 resize-none"
              placeholder="Digite palavras-chave separadas por vírgula (ex: fraude, corrupção, lavagem)"
            />
            <p className="text-xs text-aurora-text-muted mt-2">
              Separe múltiplas palavras-chave com vírgulas
            </p>
          </motion.div>
        </div>

        {/* Right Column - Date Range and Execution */}
        <div className="space-y-6">
          {/* Date Range */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="aurora-card"
          >
            <div className="flex items-center space-x-2 mb-4">
              <Calendar className="w-5 h-5 text-aurora-accent" />
              <h3 className="text-lg font-semibold text-aurora-text">Período de Análise</h3>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-aurora-text mb-2">
                  Data Inicial
                </label>
                <input
                  type="date"
                  value={dateRange.start}
                  onChange={(e) => setDateRange(e.target.value, dateRange.end)}
                  className="aurora-input w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-aurora-text mb-2">
                  Data Final
                </label>
                <input
                  type="date"
                  value={dateRange.end}
                  onChange={(e) => setDateRange(dateRange.start, e.target.value)}
                  className="aurora-input w-full"
                />
              </div>
            </div>
          </motion.div>

          {/* Quick Presets */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="aurora-card"
          >
            <h3 className="text-lg font-semibold text-aurora-text mb-4">Períodos Rápidos</h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: 'Últimos 7 dias', days: 7 },
                { label: 'Últimos 30 dias', days: 30 },
                { label: 'Últimos 90 dias', days: 90 },
                { label: 'Último ano', days: 365 }
              ].map((preset) => (
                <motion.button
                  key={preset.days}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    const end = new Date();
                    const start = new Date();
                    start.setDate(start.getDate() - preset.days);
                    setDateRange(
                      start.toISOString().split('T')[0],
                      end.toISOString().split('T')[0]
                    );
                  }}
                  className="aurora-button-secondary text-sm py-2"
                >
                  {preset.label}
                </motion.button>
              ))}
            </div>
          </motion.div>

          {/* Execution Summary */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="aurora-card"
          >
            <div className="flex items-center space-x-2 mb-4">
              <Settings className="w-5 h-5 text-aurora-accent" />
              <h3 className="text-lg font-semibold text-aurora-text">Resumo da Execução</h3>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-aurora-text-muted">Conexão:</span>
                <span className="text-aurora-text">
                  {connections.find(c => c.id === selectedConnection)?.connection_name || 'Não selecionada'}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-aurora-text-muted">Entidades:</span>
                <span className="text-aurora-text">{selectedEntities.length}</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-aurora-text-muted">Palavras-chave:</span>
                <span className="text-aurora-text">
                  {localKeywords.split(',').filter(k => k.trim().length > 0).length}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-aurora-text-muted">Período:</span>
                <span className="text-aurora-text">
                  {dateRange.start} a {dateRange.end}
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Execute Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="flex justify-center"
      >
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleExecute}
          disabled={isExecuting || !selectedConnection || selectedEntities.length === 0}
          className={`aurora-button flex items-center space-x-3 px-8 py-4 text-lg ${
            isExecuting || !selectedConnection || selectedEntities.length === 0
              ? 'opacity-50 cursor-not-allowed'
              : 'animate-aurora-glow'
          }`}
        >
          <Zap className="w-6 h-6" />
          <span>{isExecuting ? 'Executando...' : 'Executar Análise'}</span>
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

export default ExecutionPanel;
