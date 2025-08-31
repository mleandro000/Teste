import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Target, 
  Plus, 
  Trash2, 
  Edit, 
  Check, 
  X,
  Building,
  Users,
  Briefcase
} from 'lucide-react';
import { useAppStore } from '../lib/store';

const TargetManager: React.FC = () => {
  const { entities, loadEntities, addEntity, deleteEntity, isLoading } = useAppStore();
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    entity_type: 'empresa'
  });

  React.useEffect(() => {
    loadEntities();
  }, [loadEntities]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (editingId) {
      // TODO: Implement edit functionality
      setEditingId(null);
    } else {
      await addEntity(formData);
    }

    setShowForm(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      name: '',
      entity_type: 'empresa'
    });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja deletar esta entidade?')) {
      await deleteEntity(id);
    }
  };

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'empresa':
        return <Building className="w-5 h-5 text-aurora-accent" />;
      case 'pessoa':
        return <Users className="w-5 h-5 text-aurora-accent" />;
      case 'fund':
        return <Briefcase className="w-5 h-5 text-aurora-accent" />;
      default:
        return <Target className="w-5 h-5 text-aurora-accent" />;
    }
  };

  const getEntityTypeLabel = (type: string) => {
    switch (type) {
      case 'empresa':
        return 'Empresa';
      case 'pessoa':
        return 'Pessoa';
      case 'fund':
        return 'Fundo';
      default:
        return type;
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
            <Target className="w-6 h-6 text-black" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-aurora-text">Entidades Monitoradas</h2>
            <p className="text-sm text-aurora-text-muted">Gerencie os alvos da análise</p>
          </div>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowForm(true)}
          className="aurora-button flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>Nova Entidade</span>
        </motion.button>
      </div>

      {/* Entity Form */}
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
              <div>
                <label className="block text-sm font-medium text-aurora-text mb-2">
                  Nome da Entidade
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="aurora-input w-full"
                  placeholder="Ex: Global Corp, João Silva"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-aurora-text mb-2">
                  Tipo de Entidade
                </label>
                <select
                  value={formData.entity_type}
                  onChange={(e) => setFormData({ ...formData, entity_type: e.target.value })}
                  className="aurora-input w-full"
                  required
                >
                  <option value="empresa">Empresa</option>
                  <option value="pessoa">Pessoa</option>
                  <option value="fund">Fundo</option>
                </select>
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

      {/* Entities List */}
      <div className="space-y-3">
        <AnimatePresence>
          {entities.map((entity, index) => (
            <motion.div
              key={entity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: index * 0.1, duration: 0.3 }}
              className="aurora-card flex items-center justify-between"
            >
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-aurora-glass rounded-lg flex items-center justify-center">
                  {getEntityIcon(entity.entity_type)}
                </div>
                
                <div>
                  <h3 className="font-semibold text-aurora-text">{entity.name}</h3>
                  <p className="text-sm text-aurora-text-muted">
                    {getEntityTypeLabel(entity.entity_type)}
                  </p>
                  {entity.created_at && (
                    <p className="text-xs text-aurora-text-muted">
                      Criado em: {new Date(entity.created_at).toLocaleDateString('pt-BR')}
                    </p>
                  )}
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setEditingId(entity.id!)}
                  className="p-2 text-aurora-text hover:text-aurora-accent hover:bg-aurora-glass rounded-lg transition-colors"
                >
                  <Edit className="w-4 h-4" />
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => handleDelete(entity.id!)}
                  className="p-2 text-aurora-text hover:text-aurora-error hover:bg-aurora-glass rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {entities.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <Target className="w-16 h-16 text-aurora-text-muted mx-auto mb-4" />
            <p className="text-aurora-text-muted">Nenhuma entidade configurada</p>
            <p className="text-sm text-aurora-text-muted">Clique em "Nova Entidade" para começar</p>
          </motion.div>
        )}
      </div>

      {/* Quick Add Suggestions */}
      {entities.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="aurora-card"
        >
          <h3 className="text-lg font-semibold text-aurora-text mb-4">Adicionar Rápido</h3>
          <div className="grid grid-cols-3 gap-3">
            {['Global Corp', 'Banco Próspero', 'Future Inc'].map((suggestion) => (
              <motion.button
                key={suggestion}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  setFormData({ name: suggestion, entity_type: 'empresa' });
                  setShowForm(true);
                }}
                className="aurora-button-secondary text-sm py-2"
              >
                {suggestion}
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default TargetManager;
