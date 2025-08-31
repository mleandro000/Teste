import { useState, useEffect } from 'react';
import {
  Box,
  Flex,
  Text,
  VStack,
  HStack,
  useToast,
  IconButton,
  Icon,
} from '@chakra-ui/react';
import { Sidebar } from './components/Sidebar';
import ConnectionManager from './components/ConnectionManager';
import SQLServerConnection from './components/SQLServerConnection';
import TargetManager from './components/TargetManager';
import ExecutionPanel from './components/ExecutionPanel';
import JobsHistory from './components/JobsHistory';
import { useAppStore } from './lib/store';
import { FileText } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('connections');
  const { error, setError } = useAppStore();
  const toast = useToast();

  // Show error toast
  useEffect(() => {
    if (error) {
      toast({
        title: 'Erro',
        description: error,
        status: 'error',
        duration: 5000,
        isClosable: true,
        position: 'top-right',
      });
      setError(null);
    }
  }, [error, setError, toast]);

  const renderContent = () => {
    switch (activeTab) {
      case 'connections':
        return <ConnectionManager />;
      case 'sqlserver':
        return <SQLServerConnection />;
      case 'targets':
        return <TargetManager />;
      case 'execution':
        return <ExecutionPanel />;
      case 'history':
        return <JobsHistory />;
      case 'policies':
        return (
          <VStack spacing={4} py={12} textAlign="center">
            <Text fontSize="xl" fontWeight="bold" color="white">
              Políticas de Risco
            </Text>
            <Text color="gray.400">Funcionalidade em desenvolvimento</Text>
          </VStack>
        );
      case 'monitoring':
        return (
          <VStack spacing={4} py={12} textAlign="center">
            <Text fontSize="xl" fontWeight="bold" color="white">
              Monitorização Contínua
            </Text>
            <Text color="gray.400">Funcionalidade em desenvolvimento</Text>
          </VStack>
        );
      case 'cache':
        return (
          <VStack spacing={4} py={12} textAlign="center">
            <Text fontSize="xl" fontWeight="bold" color="white">
              Cache Inteligente
            </Text>
            <Text color="gray.400">Funcionalidade em desenvolvimento</Text>
          </VStack>
        );
      case 'settings':
        return (
          <VStack spacing={4} py={12} textAlign="center">
            <Text fontSize="xl" fontWeight="bold" color="white">
              Configurações
            </Text>
            <Text color="gray.400">Funcionalidade em desenvolvimento</Text>
          </VStack>
        );
      default:
        return <ConnectionManager />;
    }
  };

  return (
    <Box minH="100vh" position="relative" overflow="hidden">
      {/* Animated Background Elements */}
      <Box position="absolute" inset={0} overflow="hidden" pointerEvents="none">
        <Box
          position="absolute"
          top={0}
          left="25%"
          w="96"
          h="96"
          bg="auroraAccent.primary"
          opacity={0.05}
          borderRadius="full"
          filter="blur(3xl)"
          animation="pulse 3s infinite"
        />
        <Box
          position="absolute"
          bottom={0}
          right="25%"
          w="96"
          h="96"
          bg="auroraAccent.primary"
          opacity={0.05}
          borderRadius="full"
          filter="blur(3xl)"
          animation="pulse 3s infinite"
          animationDelay="2s"
        />
        <Box
          position="absolute"
          top="50%"
          left="50%"
          transform="translate(-50%, -50%)"
          w="64"
          h="64"
          bg="auroraAccent.primary"
          opacity={0.03}
          borderRadius="full"
          filter="blur(2xl)"
          animation="pulse 3s infinite"
          animationDelay="4s"
        />
      </Box>

      <Flex h="100vh">
        {/* Sidebar */}
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        
        {/* Main Content */}
        <Box flex={1} overflow="auto" ml="280px">
          <Box p={8}>
            <Box
              key={activeTab}
              animation="fadeIn 0.3s ease-out"
            >
              {renderContent()}
            </Box>
          </Box>
        </Box>
      </Flex>

      {/* Floating Action Button for Results */}
      {activeTab !== 'history' && (
        <IconButton
          position="fixed"
          bottom={6}
          right={6}
          w="14"
          h="14"
          borderRadius="full"
          bg="auroraAccent.primary"
          color="black"
          fontSize="lg"
          fontWeight="bold"
          zIndex={40}
          boxShadow="aurora"
          _hover={{
            transform: 'scale(1.1)',
            boxShadow: 'auroraHover',
          }}
          _active={{
            transform: 'scale(0.9)',
          }}
          onClick={() => setActiveTab('history')}
          aria-label="Ver resultados"
          icon={<Icon as={FileText} boxSize={6} />}
        />
      )}
    </Box>
  );
}

export default App;
