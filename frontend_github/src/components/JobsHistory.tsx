import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  History, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Loader, 
  AlertCircle,
  Eye,
  Download
} from 'lucide-react';
import { useAppStore } from '../lib/store';

const JobsHistory: React.FC = () => {
  const { jobs, loadJobs, isLoading } = useAppStore();

  React.useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-aurora-success" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-aurora-error" />;
      case 'running':
        return <Loader className="w-5 h-5 text-aurora-accent animate-spin" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-aurora-warning" />;
      default:
        return <AlertCircle className="w-5 h-5 text-aurora-text-muted" />;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Concluído';
      case 'failed':
        return 'Falhou';
      case 'running':
        return 'Executando';
      case 'pending':
        return 'Pendente';
      default:
        return status;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-aurora-success/20 text-aurora-success';
      case 'failed':
        return 'bg-aurora-error/20 text-aurora-error';
      case 'running':
        return 'bg-aurora-accent/20 text-aurora-accent';
      case 'pending':
        return 'bg-aurora-warning/20 text-aurora-warning';
      default:
        return 'bg-aurora-text-muted/20 text-aurora-text-muted';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getDuration = (startDate: string, endDate?: string) => {
    const start = new Date(startDate);
    const end = endDate ? new Date(endDate) : new Date();
    const diff = end.getTime() - start.getTime();
    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
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
            <History className="w-6 h-6 text-black" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-aurora-text">Histórico de Execuções</h2>
            <p className="text-sm text-aurora-text-muted">Acompanhe o progresso das análises</p>
          </div>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={loadJobs}
          disabled={isLoading}
          className="aurora-button-secondary flex items-center space-x-2"
        >
          <Clock className="w-4 h-4" />
          <span>{isLoading ? 'Atualizando...' : 'Atualizar'}</span>
        </motion.button>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Total', value: jobs.length, color: 'text-aurora-text' },
          { label: 'Concluídos', value: jobs.filter(j => j.status === 'completed').length, color: 'text-aurora-success' },
          { label: 'Executando', value: jobs.filter(j => j.status === 'running').length, color: 'text-aurora-accent' },
          { label: 'Falharam', value: jobs.filter(j => j.status === 'failed').length, color: 'text-aurora-error' }
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

      {/* Jobs List */}
      <div className="space-y-3">
        <AnimatePresence>
          {jobs.map((job, index) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: index * 0.1, duration: 0.3 }}
              className="aurora-card"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(job.status)}
                    <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(job.status)}`}>
                      {getStatusLabel(job.status)}
                    </span>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold text-aurora-text">
                      Análise #{job.id} - {job.tipo_gatilho}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-aurora-text-muted">
                      <span>Iniciado: {job.iniciado_em ? formatDate(job.iniciado_em) : 'N/A'}</span>
                      {job.iniciado_em && (
                        <span>Duração: {getDuration(job.iniciado_em, job.finalizado_em)}</span>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="p-2 text-aurora-text hover:text-aurora-accent hover:bg-aurora-glass rounded-lg transition-colors"
                    title="Ver detalhes"
                  >
                    <Eye className="w-4 h-4" />
                  </motion.button>
                  
                  {job.status === 'completed' && (
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      className="p-2 text-aurora-text hover:text-aurora-success hover:bg-aurora-glass rounded-lg transition-colors"
                      title="Baixar relatório"
                    >
                      <Download className="w-4 h-4" />
                    </motion.button>
                  )}
                </div>
              </div>
              
              {job.resultado && (
                <div className="mt-3 pt-3 border-t border-aurora-border">
                  <p className="text-sm text-aurora-text-muted">
                    <strong>Resultado:</strong> {job.resultado}
                  </p>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {jobs.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <History className="w-16 h-16 text-aurora-text-muted mx-auto mb-4" />
            <p className="text-aurora-text-muted">Nenhuma execução encontrada</p>
            <p className="text-sm text-aurora-text-muted">Execute uma análise para ver o histórico</p>
          </motion.div>
        )}
      </div>

      {/* Recent Activity */}
      {jobs.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="aurora-card"
        >
          <h3 className="text-lg font-semibold text-aurora-text mb-4">Atividade Recente</h3>
          <div className="space-y-3">
                         {jobs.slice(0, 5).map((job) => (
              <div key={job.id} className="flex items-center space-x-3">
                <div className="w-2 h-2 rounded-full bg-aurora-accent" />
                <span className="text-sm text-aurora-text">
                  Análise #{job.id} {getStatusLabel(job.status).toLowerCase()}
                </span>
                <span className="text-xs text-aurora-text-muted">
                  {job.iniciado_em ? formatDate(job.iniciado_em) : 'N/A'}
                </span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default JobsHistory;
