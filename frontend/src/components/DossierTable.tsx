import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  Search, 
  Download, 
  Eye, 
  ExternalLink,
  AlertTriangle,
  Info,
  CheckCircle
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import type { Finding } from '../types';

const DossierTable: React.FC = () => {
  const { findings, loadFindings, isLoading } = useAppStore();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('data_coleta');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  React.useEffect(() => {
    loadFindings();
  }, [loadFindings]);

  const filteredFindings = findings
    .filter(finding => {
      const matchesSearch = 
        finding.entity_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        finding.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        finding.content.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesRisk = selectedRiskLevel === 'all' || finding.risk_level === selectedRiskLevel;
      
      return matchesSearch && matchesRisk;
    })
    .sort((a, b) => {
      let aValue: any = a[sortBy as keyof Finding];
      let bValue: any = b[sortBy as keyof Finding];
      
      if (sortBy === 'data_coleta') {
        aValue = new Date(aValue).getTime();
        bValue = new Date(bValue).getTime();
      }
      
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  const getRiskLevelIcon = (level: string) => {
    switch (level) {
      case 'ALTO':
        return <AlertTriangle className="w-4 h-4 text-aurora-error" />;
      case 'MÉDIO':
        return <Info className="w-4 h-4 text-aurora-warning" />;
      case 'BAIXO':
        return <CheckCircle className="w-4 h-4 text-aurora-success" />;
      default:
        return <Info className="w-4 h-4 text-aurora-text-muted" />;
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'ALTO':
        return 'bg-aurora-error/20 text-aurora-error border-aurora-error/30';
      case 'MÉDIO':
        return 'bg-aurora-warning/20 text-aurora-warning border-aurora-warning/30';
      case 'BAIXO':
        return 'bg-aurora-success/20 text-aurora-success border-aurora-success/30';
      default:
        return 'bg-aurora-text-muted/20 text-aurora-text-muted border-aurora-text-muted/30';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const truncateText = (text: string, maxLength: number) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
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
            <FileText className="w-6 h-6 text-black" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-aurora-text">Resultados da Análise</h2>
            <p className="text-sm text-aurora-text-muted">Dossiês e achados identificados</p>
          </div>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={loadFindings}
          disabled={isLoading}
          className="aurora-button-secondary flex items-center space-x-2"
        >
          <Search className="w-4 h-4" />
          <span>{isLoading ? 'Atualizando...' : 'Atualizar'}</span>
        </motion.button>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Total', value: findings.length, color: 'text-aurora-text' },
          { label: 'Alto Risco', value: findings.filter(f => f.risk_level === 'ALTO').length, color: 'text-aurora-error' },
          { label: 'Médio Risco', value: findings.filter(f => f.risk_level === 'MÉDIO').length, color: 'text-aurora-warning' },
          { label: 'Baixo Risco', value: findings.filter(f => f.risk_level === 'BAIXO').length, color: 'text-aurora-success' }
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="aurora-card text-center"
          >
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
            <div className="text-sm text-aurora-text-muted">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Filters */}
      <div className="aurora-card">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-aurora-text mb-2">
              Buscar
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-aurora-text-muted" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="aurora-input w-full pl-10"
                placeholder="Buscar por entidade, título ou conteúdo..."
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-aurora-text mb-2">
              Nível de Risco
            </label>
            <select
              value={selectedRiskLevel}
              onChange={(e) => setSelectedRiskLevel(e.target.value)}
              className="aurora-input"
            >
              <option value="all">Todos</option>
              <option value="ALTO">Alto</option>
              <option value="MÉDIO">Médio</option>
              <option value="BAIXO">Baixo</option>
            </select>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="aurora-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-aurora-border">
                <th className="text-left p-4 text-aurora-text-muted font-medium">
                  <button
                    onClick={() => handleSort('entity_name')}
                    className="flex items-center space-x-1 hover:text-aurora-accent transition-colors"
                  >
                    <span>Entidade</span>
                    {sortBy === 'entity_name' && (
                      <span className="text-aurora-accent">
                        {sortOrder === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </button>
                </th>
                <th className="text-left p-4 text-aurora-text-muted font-medium">
                  <button
                    onClick={() => handleSort('title')}
                    className="flex items-center space-x-1 hover:text-aurora-accent transition-colors"
                  >
                    <span>Título</span>
                    {sortBy === 'title' && (
                      <span className="text-aurora-accent">
                        {sortOrder === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </button>
                </th>
                <th className="text-left p-4 text-aurora-text-muted font-medium">
                  <button
                    onClick={() => handleSort('risk_level')}
                    className="flex items-center space-x-1 hover:text-aurora-accent transition-colors"
                  >
                    <span>Risco</span>
                    {sortBy === 'risk_level' && (
                      <span className="text-aurora-accent">
                        {sortOrder === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </button>
                </th>
                <th className="text-left p-4 text-aurora-text-muted font-medium">
                  <button
                    onClick={() => handleSort('data_coleta')}
                    className="flex items-center space-x-1 hover:text-aurora-accent transition-colors"
                  >
                    <span>Data</span>
                    {sortBy === 'data_coleta' && (
                      <span className="text-aurora-accent">
                        {sortOrder === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </button>
                </th>
                <th className="text-left p-4 text-aurora-text-muted font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence>
                {filteredFindings.map((finding, index) => (
                  <motion.tr
                    key={finding.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ delay: index * 0.05, duration: 0.3 }}
                    className="border-b border-aurora-border/50 hover:bg-aurora-glass/50 transition-colors"
                  >
                    <td className="p-4">
                      <div className="font-medium text-aurora-text">{finding.entity_name}</div>
                      <div className="text-sm text-aurora-text-muted">{finding.categoria}</div>
                    </td>
                    <td className="p-4">
                      <div className="font-medium text-aurora-text">{finding.title}</div>
                      <div className="text-sm text-aurora-text-muted">
                        {truncateText(finding.content, 100)}
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center space-x-2">
                        {getRiskLevelIcon(finding.risk_level)}
                        <span className={`text-xs px-2 py-1 rounded-full border ${getRiskLevelColor(finding.risk_level)}`}>
                          {finding.risk_level}
                        </span>
                      </div>
                      <div className="text-sm text-aurora-text-muted mt-1">
                        Score: {finding.risk_score}
                      </div>
                    </td>
                    <td className="p-4 text-sm text-aurora-text-muted">
                      {formatDate(finding.data_coleta)}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center space-x-2">
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 text-aurora-text hover:text-aurora-accent hover:bg-aurora-glass rounded-lg transition-colors"
                          title="Ver detalhes"
                        >
                          <Eye className="w-4 h-4" />
                        </motion.button>
                        
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 text-aurora-text hover:text-aurora-accent hover:bg-aurora-glass rounded-lg transition-colors"
                          title="Abrir fonte"
                          onClick={() => window.open(finding.source_url, '_blank')}
                        >
                          <ExternalLink className="w-4 h-4" />
                        </motion.button>
                        
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 text-aurora-text hover:text-aurora-success hover:bg-aurora-glass rounded-lg transition-colors"
                          title="Baixar relatório"
                        >
                          <Download className="w-4 h-4" />
                        </motion.button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            </tbody>
          </table>
        </div>
        
        {filteredFindings.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <FileText className="w-16 h-16 text-aurora-text-muted mx-auto mb-4" />
            <p className="text-aurora-text-muted">
              {findings.length === 0 ? 'Nenhum resultado encontrado' : 'Nenhum resultado corresponde aos filtros'}
            </p>
            <p className="text-sm text-aurora-text-muted">
              {findings.length === 0 ? 'Execute uma análise para ver os resultados' : 'Tente ajustar os filtros de busca'}
            </p>
          </motion.div>
        )}
      </div>

      {/* Export Options */}
      {filteredFindings.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="aurora-card"
        >
          <h3 className="text-lg font-semibold text-aurora-text mb-4">Exportar Resultados</h3>
          <div className="flex space-x-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="aurora-button-secondary flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Exportar CSV</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="aurora-button-secondary flex items-center space-x-2"
            >
              <FileText className="w-4 h-4" />
              <span>Relatório PDF</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="aurora-button-secondary flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Relatório Completo</span>
            </motion.button>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default DossierTable;
