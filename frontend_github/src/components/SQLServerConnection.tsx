import React, { useState } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Input,
  Button,
  Select,
  Checkbox,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Divider,
  Badge,
  useToast,
  Spinner,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Textarea,
  Collapse,
} from '@chakra-ui/react';

interface ConnectionDetails {
  server: string;
  database: string;
  port: number;
  use_windows_auth: boolean;
  username?: string;
  password?: string;
}

interface ConnectionResult {
  success: boolean;
  message?: string;
  server_version?: string;
  database?: string;
}

interface QueryRequest {
  connection: ConnectionDetails;
  query: string;
}

interface QueryResult {
  success: boolean;
  columns?: string[];
  data?: any[];
  row_count?: number;
  message?: string;
}

interface TablesResult {
  success: boolean;
  tables?: string[];
  message?: string;
}

const SQLServerConnection: React.FC = () => {
  const [connectionData, setConnectionData] = useState<ConnectionDetails>({
    server: 'DESKTOP-T9HKFSQ\\SQLEXPRESS',
    database: 'Projeto_Dev',
    port: 1433,
    use_windows_auth: true,
    username: '',
    password: ''
  });
  
  const [connectionResult, setConnectionResult] = useState<ConnectionResult | null>(null);
  const [tablesResult, setTablesResult] = useState<TablesResult | null>(null);
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [customQuery, setCustomQuery] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showQueryPanel, setShowQueryPanel] = useState(false);
  const toast = useToast();

  const testConnection = async () => {
    setLoading(true);
    setConnectionResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8001/api/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(connectionData)
      });

      const data: ConnectionResult = await response.json();
      setConnectionResult(data);
      
      if (data.success) {
        toast({
          title: 'Conexão bem-sucedida!',
          description: data.message,
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
      } else {
        toast({
          title: 'Erro na conexão',
          description: data.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
      
    } catch (error) {
      const errorMessage = `Erro de rede: ${error}`;
      setConnectionResult({
        success: false,
        message: errorMessage
      });
      toast({
        title: 'Erro de conexão',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
    
    setLoading(false);
  };

  const listTables = async () => {
    setLoading(true);
    setTablesResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8001/api/tables', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(connectionData)
      });

      const data: TablesResult = await response.json();
      setTablesResult(data);
      
      if (data.success) {
        toast({
          title: 'Tabelas listadas!',
          description: `Encontradas ${data.tables?.length} tabelas`,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      }
      
    } catch (error) {
      setTablesResult({
        success: false,
        message: `Erro ao listar tabelas: ${error}`
      });
    }
    
    setLoading(false);
  };

  const executeQuery = async () => {
    if (!customQuery.trim()) {
      toast({
        title: 'Query vazia',
        description: 'Digite uma query para executar',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);
    setQueryResult(null);

    try {
      const queryRequest: QueryRequest = {
        connection: connectionData,
        query: customQuery
      };

      const response = await fetch('http://127.0.0.1:8001/api/execute-query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryRequest)
      });

      const data: QueryResult = await response.json();
      setQueryResult(data);
      
      if (data.success) {
        toast({
          title: 'Query executada!',
          description: data.message || `Retornou ${data.row_count} linhas`,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      }
      
    } catch (error) {
      setQueryResult({
        success: false,
        message: `Erro ao executar query: ${error}`
      });
    }
    
    setLoading(false);
  };

  return (
    <Box maxW="1200px" mx="auto" p={6}>
      <VStack spacing={8} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Text fontSize="3xl" fontWeight="bold" color="white" mb={2}>
            SQL Server Connection
          </Text>
          <Text color="gray.400">
            Conecte-se ao seu banco de dados SQL Server e execute queries
          </Text>
        </Box>

        {/* Connection Form */}
        <Box bg="auroraGlass.light" p={6} borderRadius="xl" border="1px solid" borderColor="auroraBorder.light">
          <Text fontSize="xl" fontWeight="bold" color="white" mb={4}>
            Configuração de Conexão
          </Text>
          
          <VStack spacing={4} align="stretch">
            <HStack spacing={4}>
              <Box flex={1}>
                <Text color="gray.300" mb={2}>Servidor:</Text>
                <Input
                  value={connectionData.server}
                  onChange={(e) => setConnectionData({...connectionData, server: e.target.value})}
                  placeholder="localhost\SQLEXPRESS"
                  bg="auroraGlass.medium"
                  borderColor="auroraBorder.medium"
                  color="white"
                  _placeholder={{ color: 'gray.500' }}
                />
              </Box>
              <Box flex={1}>
                <Text color="gray.300" mb={2}>Database:</Text>
                <Input
                  value={connectionData.database}
                  onChange={(e) => setConnectionData({...connectionData, database: e.target.value})}
                  placeholder="Nome do banco"
                  bg="auroraGlass.medium"
                  borderColor="auroraBorder.medium"
                  color="white"
                  _placeholder={{ color: 'gray.500' }}
                />
              </Box>
              <Box w="120px">
                <Text color="gray.300" mb={2}>Porta:</Text>
                <Input
                  type="number"
                  value={connectionData.port}
                  onChange={(e) => setConnectionData({...connectionData, port: parseInt(e.target.value)})}
                  bg="auroraGlass.medium"
                  borderColor="auroraBorder.medium"
                  color="white"
                />
              </Box>
            </HStack>

            <Checkbox
              isChecked={connectionData.use_windows_auth}
              onChange={(e) => setConnectionData({...connectionData, use_windows_auth: e.target.checked})}
              color="gray.300"
            >
              Usar Autenticação Windows
            </Checkbox>

            <Collapse in={!connectionData.use_windows_auth}>
              <HStack spacing={4}>
                <Box flex={1}>
                  <Text color="gray.300" mb={2}>Usuário:</Text>
                  <Input
                    value={connectionData.username || ''}
                    onChange={(e) => setConnectionData({...connectionData, username: e.target.value})}
                    placeholder="sa"
                    bg="auroraGlass.medium"
                    borderColor="auroraBorder.medium"
                    color="white"
                    _placeholder={{ color: 'gray.500' }}
                  />
                </Box>
                <Box flex={1}>
                  <Text color="gray.300" mb={2}>Senha:</Text>
                  <Input
                    type="password"
                    value={connectionData.password || ''}
                    onChange={(e) => setConnectionData({...connectionData, password: e.target.value})}
                    placeholder="******"
                    bg="auroraGlass.medium"
                    borderColor="auroraBorder.medium"
                    color="white"
                    _placeholder={{ color: 'gray.500' }}
                  />
                </Box>
              </HStack>
            </Collapse>

            <HStack spacing={4}>
              <Button
                onClick={testConnection}
                disabled={loading}
                bg="auroraAccent.primary"
                color="black"
                _hover={{ bg: 'auroraAccent.secondary' }}
                leftIcon={loading ? <Spinner size="sm" /> : undefined}
                flex={1}
              >
                {loading ? 'Testando...' : 'Testar Conexão'}
              </Button>
              
              <Button
                onClick={listTables}
                disabled={loading || !connectionResult?.success}
                bg="auroraAccent.secondary"
                color="black"
                _hover={{ bg: 'auroraAccent.tertiary' }}
                flex={1}
              >
                Listar Tabelas
              </Button>
            </HStack>
          </VStack>
        </Box>

        {/* Connection Result */}
        {connectionResult && (
          <Alert
            status={connectionResult.success ? 'success' : 'error'}
            borderRadius="lg"
            bg={connectionResult.success ? 'auroraAccent.success' : 'auroraAccent.error'}
            color="white"
          >
            <AlertIcon />
            <Box>
              <AlertTitle>
                {connectionResult.success ? '✅ Conexão Bem-sucedida!' : '❌ Erro na Conexão!'}
              </AlertTitle>
              <AlertDescription>
                {connectionResult.message}
                {connectionResult.success && connectionResult.server_version && (
                  <Text mt={2} fontSize="sm">
                    <strong>Servidor:</strong> {connectionResult.server_version}<br/>
                    <strong>Database:</strong> {connectionResult.database}
                  </Text>
                )}
              </AlertDescription>
            </Box>
          </Alert>
        )}

        {/* Tables Result */}
        {tablesResult && tablesResult.success && tablesResult.tables && (
          <Box bg="auroraGlass.light" p={6} borderRadius="xl" border="1px solid" borderColor="auroraBorder.light">
            <HStack justify="space-between" mb={4}>
              <Text fontSize="xl" fontWeight="bold" color="white">
                Tabelas Encontradas ({tablesResult.tables.length})
              </Text>
              <Button
                onClick={() => setShowQueryPanel(!showQueryPanel)}
                size="sm"
                bg="auroraAccent.primary"
                color="black"
              >
                {showQueryPanel ? 'Ocultar Query' : 'Executar Query'}
              </Button>
            </HStack>
            
            <Box maxH="300px" overflowY="auto">
              <VStack spacing={2} align="stretch">
                {tablesResult.tables.map((table, index) => (
                  <Box
                    key={index}
                    p={3}
                    bg="auroraGlass.medium"
                    borderRadius="md"
                    border="1px solid"
                    borderColor="auroraBorder.medium"
                  >
                    <Text color="white" fontFamily="monospace">{table}</Text>
                  </Box>
                ))}
              </VStack>
            </Box>
          </Box>
        )}

        {/* Query Panel */}
        <Collapse in={showQueryPanel}>
          <Box bg="auroraGlass.light" p={6} borderRadius="xl" border="1px solid" borderColor="auroraBorder.light">
            <Text fontSize="xl" fontWeight="bold" color="white" mb={4}>
              Executar Query SQL
            </Text>
            
            <VStack spacing={4} align="stretch">
              <Box>
                <Text color="gray.300" mb={2}>Query SQL:</Text>
                <Textarea
                  value={customQuery}
                  onChange={(e) => setCustomQuery(e.target.value)}
                  placeholder="SELECT TOP 10 * FROM sua_tabela"
                  rows={6}
                  bg="auroraGlass.medium"
                  borderColor="auroraBorder.medium"
                  color="white"
                  fontFamily="monospace"
                  _placeholder={{ color: 'gray.500' }}
                />
              </Box>
              
              <Button
                onClick={executeQuery}
                disabled={loading || !connectionResult?.success}
                bg="auroraAccent.primary"
                color="black"
                _hover={{ bg: 'auroraAccent.secondary' }}
                leftIcon={loading ? <Spinner size="sm" /> : undefined}
              >
                {loading ? 'Executando...' : 'Executar Query'}
              </Button>
            </VStack>
          </Box>
        </Collapse>

        {/* Query Result */}
        {queryResult && (
          <Box bg="auroraGlass.light" p={6} borderRadius="xl" border="1px solid" borderColor="auroraBorder.light">
            <Text fontSize="xl" fontWeight="bold" color="white" mb={4}>
              Resultado da Query
            </Text>
            
            {queryResult.success ? (
              <VStack spacing={4} align="stretch">
                <HStack justify="space-between">
                  <Text color="gray.300">
                    {queryResult.message || `Query executada com sucesso`}
                  </Text>
                  {queryResult.row_count !== undefined && (
                    <Badge colorScheme="green" variant="subtle">
                      {queryResult.row_count} linhas
                    </Badge>
                  )}
                </HStack>
                
                {queryResult.data && queryResult.data.length > 0 && (
                  <Box maxH="400px" overflowY="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          {queryResult.columns?.map((column, index) => (
                            <Th key={index} color="gray.300">{column}</Th>
                          ))}
                        </Tr>
                      </Thead>
                      <Tbody>
                        {queryResult.data.map((row, rowIndex) => (
                          <Tr key={rowIndex}>
                            {queryResult.columns?.map((column, colIndex) => (
                              <Td key={colIndex} color="white" fontFamily="monospace">
                                {String(row[column] || '')}
                              </Td>
                            ))}
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  </Box>
                )}
              </VStack>
            ) : (
              <Alert status="error" borderRadius="lg">
                <AlertIcon />
                <AlertDescription color="white">
                  {queryResult.message}
                </AlertDescription>
              </Alert>
            )}
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default SQLServerConnection;
