import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Database, 
  Plus, 
  Trash2, 
  Edit, 
  Check, 
  X,
  Server
} from 'lucide-react';
import { useAppStore } from '../lib/store';

const ConnectionManager: React.FC = () => {
  const { connections, loadConnections, addConnection, deleteConnection, isLoading } = useAppStore();
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    connection_name: '',
    file_path: '',
  });

  React.useEffect(() => {
    loadConnections();
  }, [loadConnections]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const connectionData = {
      connection_name: formData.connection_name,
      file_path: formData.file_path,
    };

    if (editingId) {
      // TODO: Implement edit functionality
      setEditingId(null);
    } else {
      await addConnection(connectionData);
    }

    setShowForm(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      connection_name: '',
      file_path: '',
    });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja deletar esta conexão?')) {
      await deleteConnection(id);
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
            <Database className="w-6 h-6 text-black" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-aurora-text">Conexões de Banco</h2>
            <p className="text-sm text-aurora-text-muted">Gerencie suas conexões DuckDB</p>
          </div>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowForm(true)}
          className="aurora-button flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>Nova Conexão</span>
        </motion.button>
      </div>

      {/* Connection Form */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="aurora-card"
          >
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-aurora-text mb-2">
                    Nome da Conexão
                  </label>
                  <input
                    type="text"
                    value={formData.connection_name}
                    onChange={(e) => setFormData({ ...formData, connection_name: e.target.value })}
                    className="aurora-input w-full"
                    placeholder="Ex: Dados de Clientes"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-aurora-text mb-2">
                    Caminho do Arquivo
                  </label>
                  <input
                    type="text"
                    value={formData.file_path}
                    onChange={(e) => setFormData({ ...formData, file_path: e.target.value })}
                    className="aurora-input w-full"
                    placeholder="dados/clientes.duckdb"
                    required
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setShowForm(false);
                    resetForm();
                  }}
                  className="aurora-button-secondary flex items-center space-x-2"
                >
                  <X className="w-4 h-4" />
                  <span>Cancelar</span>
                </motion.button>
                
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={isLoading}
                  className="aurora-button flex items-center space-x-2"
                >
                  <Check className="w-4 h-4" />
                  <span>{isLoading ? 'Salvando...' : 'Salvar'}</span>
                </motion.button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Connections List */}
      <div className="space-y-3">
        <AnimatePresence>
          {connections.map((connection, index) => (
            <motion.div
              key={connection.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: index * 0.1, duration: 0.3 }}
              className="aurora-card flex items-center justify-between"
            >
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-aurora-glass rounded-lg flex items-center justify-center">
                  <Server className="w-5 h-5 text-aurora-accent" />
                </div>
                
                <div>
                  <h3 className="font-semibold text-aurora-text">{connection.connection_name}</h3>
                  <p className="text-sm text-aurora-text-muted">
                    {connection.file_path}
                  </p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-xs bg-aurora-success/20 text-aurora-success px-2 py-1 rounded">
                      DuckDB
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setEditingId(connection.id!)}
                  className="p-2 text-aurora-text hover:text-aurora-accent hover:bg-aurora-glass rounded-lg transition-colors"
                >
                  <Edit className="w-4 h-4" />
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => handleDelete(connection.id!)}
                  className="p-2 text-aurora-text hover:text-aurora-error hover:bg-aurora-glass rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {connections.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <Database className="w-16 h-16 text-aurora-text-muted mx-auto mb-4" />
            <p className="text-aurora-text-muted">Nenhuma conexão configurada</p>
            <p className="text-sm text-aurora-text-muted">Clique em "Nova Conexão" para começar</p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default ConnectionManager;