import React from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Icon,
  Flex,
  Badge,
  useColorModeValue,
} from '@chakra-ui/react';
import {
  Database,
  Target,
  Play,
  History,
  Shield,
  Clock,
  Activity,
  Settings,
  Wifi,
  WifiOff,
  Server,
} from 'lucide-react';
import { useAppStore } from '../lib/store';

const menuItems = [
  { id: 'connections', label: 'Conexões', icon: Database },
  { id: 'sqlserver', label: 'SQL Server', icon: Server },
  { id: 'targets', label: 'Alvos', icon: Target },
  { id: 'execution', label: 'Execução', icon: Play },
  { id: 'history', label: 'Histórico', icon: History },
  { id: 'policies', label: 'Políticas', icon: Shield },
  { id: 'monitoring', label: 'Monitorização', icon: Clock },
  { id: 'cache', label: 'Cache', icon: Activity },
  { id: 'settings', label: 'Configurações', icon: Settings },
];

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const { isConnected } = useAppStore();
  
  const bgColor = useColorModeValue('auroraGlass.light', 'auroraGlass.light');
  const borderColor = useColorModeValue('auroraBorder.light', 'auroraBorder.light');
  const activeBgColor = useColorModeValue('auroraGlass.medium', 'auroraGlass.medium');
  const activeBorderColor = useColorModeValue('auroraAccent.primary', 'auroraAccent.primary');

  return (
    <Box
      w="280px"
      h="100vh"
      bg={bgColor}
      borderRight="1px solid"
      borderColor={borderColor}
      backdropFilter="blur(10px)"
      position="fixed"
      left={0}
      top={0}
      zIndex={10}
      transition="all 0.3s ease"
    >
      <VStack spacing={6} p={6} align="stretch">
        {/* Header */}
        <Box textAlign="center" py={4}>
          <Text
            fontSize="2xl"
            fontWeight="bold"
            bgGradient="linear(to-r, auroraAccent.primary, auroraAccent.secondary)"
            bgClip="text"
            mb={2}
          >
            DD-AI
          </Text>
          <Text fontSize="sm" color="gray.400">
            Due Diligence AI
          </Text>
        </Box>

        {/* Connection Status */}
        <Box
          p={3}
          borderRadius="lg"
          bg={isConnected ? 'auroraAccent.success' : 'auroraAccent.error'}
          color="white"
          textAlign="center"
        >
          <HStack justify="center" spacing={2}>
            <Icon
              as={isConnected ? Wifi : WifiOff}
              boxSize={4}
            />
            <Text fontSize="sm" fontWeight="medium">
              {isConnected ? 'Conectado' : 'Desconectado'}
            </Text>
          </HStack>
        </Box>

        {/* Menu Items */}
        <VStack spacing={2} align="stretch">
          {menuItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <Box
                key={item.id}
                p={3}
                borderRadius="lg"
                cursor="pointer"
                bg={isActive ? activeBgColor : 'transparent'}
                border="1px solid"
                borderColor={isActive ? activeBorderColor : 'transparent'}
                _hover={{
                  bg: isActive ? activeBgColor : 'auroraGlass.medium',
                  borderColor: isActive ? activeBorderColor : 'auroraBorder.medium',
                  transform: 'translateX(4px)',
                }}
                transition="all 0.3s ease"
                onClick={() => onTabChange(item.id)}
              >
                <HStack spacing={3}>
                  <Icon
                    as={item.icon}
                    boxSize={5}
                    color={isActive ? 'auroraAccent.primary' : 'gray.400'}
                  />
                  <Text
                    fontSize="sm"
                    fontWeight="medium"
                    color={isActive ? 'white' : 'gray.300'}
                  >
                    {item.label}
                  </Text>
                  {isActive && (
                    <Box
                      w={2}
                      h={2}
                      borderRadius="full"
                      bg="auroraAccent.primary"
                      ml="auto"
                    />
                  )}
                </HStack>
              </Box>
            );
          })}
        </VStack>

        {/* Footer */}
        <Box mt="auto" pt={4} borderTop="1px solid" borderColor={borderColor}>
          <Text fontSize="xs" color="gray.500" textAlign="center">
            Aurora Interface v2.1
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};
