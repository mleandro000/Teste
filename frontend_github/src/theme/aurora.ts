import { extendTheme, type ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'dark',
  useSystemColorMode: false,
};

const colors = {
  aurora: {
    50: '#e6f7ff',
    100: '#b3e0ff',
    200: '#80c9ff',
    300: '#4db2ff',
    400: '#1a9bff',
    500: '#0084ff',
    600: '#0066cc',
    700: '#004799',
    800: '#002966',
    900: '#000b33',
  },
  auroraBg: {
    start: '#0a0f1e',
    end: '#1a1a3d',
  },
  auroraAccent: {
    primary: '#00ffff',
    secondary: '#38bdf8',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
  },
  auroraGlass: {
    light: 'rgba(255, 255, 255, 0.05)',
    medium: 'rgba(255, 255, 255, 0.1)',
    dark: 'rgba(255, 255, 255, 0.15)',
  },
  auroraBorder: {
    light: 'rgba(255, 255, 255, 0.1)',
    medium: 'rgba(255, 255, 255, 0.2)',
    dark: 'rgba(255, 255, 255, 0.3)',
  },
};

const components = {
  Button: {
    baseStyle: {
      fontWeight: 'semibold',
      borderRadius: 'lg',
      _focus: {
        boxShadow: '0 0 0 3px rgba(0, 255, 255, 0.3)',
      },
    },
    variants: {
      aurora: {
        bg: 'auroraAccent.primary',
        color: 'black',
        _hover: {
          bg: 'auroraAccent.secondary',
          transform: 'translateY(-2px)',
          boxShadow: '0 10px 25px rgba(0, 255, 255, 0.3)',
        },
        _active: {
          transform: 'translateY(0)',
        },
        transition: 'all 0.3s ease',
      },
      auroraGlass: {
        bg: 'auroraGlass.light',
        color: 'white',
        border: '1px solid',
        borderColor: 'auroraBorder.light',
        backdropFilter: 'blur(10px)',
        _hover: {
          bg: 'auroraGlass.medium',
          borderColor: 'auroraBorder.medium',
          transform: 'translateY(-1px)',
        },
        transition: 'all 0.3s ease',
      },
    },
    defaultProps: {
      variant: 'aurora',
    },
  },
  Card: {
    baseStyle: {
      container: {
        bg: 'auroraGlass.light',
        border: '1px solid',
        borderColor: 'auroraBorder.light',
        borderRadius: '2xl',
        backdropFilter: 'blur(10px)',
        _hover: {
          bg: 'auroraGlass.medium',
          borderColor: 'auroraBorder.medium',
        },
        transition: 'all 0.3s ease',
      },
    },
  },
  Input: {
    baseStyle: {
      field: {
        bg: 'auroraGlass.light',
        border: '1px solid',
        borderColor: 'auroraBorder.light',
        borderRadius: 'lg',
        color: 'white',
        _placeholder: {
          color: 'gray.400',
        },
        _focus: {
          borderColor: 'auroraAccent.primary',
          boxShadow: '0 0 0 1px rgba(0, 255, 255, 0.3)',
        },
        _hover: {
          borderColor: 'auroraBorder.medium',
        },
        transition: 'all 0.3s ease',
      },
    },
  },
  Textarea: {
    baseStyle: {
      bg: 'auroraGlass.light',
      border: '1px solid',
      borderColor: 'auroraBorder.light',
      borderRadius: 'lg',
      color: 'white',
      _placeholder: {
        color: 'gray.400',
      },
      _focus: {
        borderColor: 'auroraAccent.primary',
        boxShadow: '0 0 0 1px rgba(0, 255, 255, 0.3)',
      },
      _hover: {
        borderColor: 'auroraBorder.medium',
      },
      transition: 'all 0.3s ease',
    },
  },
  Select: {
    baseStyle: {
      field: {
        bg: 'auroraGlass.light',
        border: '1px solid',
        borderColor: 'auroraBorder.light',
        borderRadius: 'lg',
        color: 'white',
        _focus: {
          borderColor: 'auroraAccent.primary',
          boxShadow: '0 0 0 1px rgba(0, 255, 255, 0.3)',
        },
        _hover: {
          borderColor: 'auroraBorder.medium',
        },
        transition: 'all 0.3s ease',
      },
    },
  },
  Table: {
    baseStyle: {
      table: {
        bg: 'auroraGlass.light',
        borderRadius: 'xl',
        overflow: 'hidden',
      },
      thead: {
        bg: 'auroraGlass.medium',
      },
      th: {
        color: 'white',
        fontWeight: 'semibold',
        borderBottom: '1px solid',
        borderColor: 'auroraBorder.light',
      },
      td: {
        color: 'gray.200',
        borderBottom: '1px solid',
        borderColor: 'auroraBorder.light',
      },
      tr: {
        _hover: {
          bg: 'auroraGlass.medium',
        },
        transition: 'background 0.2s ease',
      },
    },
  },
  Modal: {
    baseStyle: {
      dialog: {
        bg: 'auroraBg.start',
        border: '1px solid',
        borderColor: 'auroraBorder.medium',
        borderRadius: '2xl',
        backdropFilter: 'blur(20px)',
      },
      header: {
        color: 'white',
        fontWeight: 'bold',
      },
      body: {
        color: 'gray.200',
      },
    },
  },
  Drawer: {
    baseStyle: {
      dialog: {
        bg: 'auroraBg.start',
        borderRight: '1px solid',
        borderColor: 'auroraBorder.medium',
      },
    },
  },
  Menu: {
    baseStyle: {
      list: {
        bg: 'auroraGlass.medium',
        border: '1px solid',
        borderColor: 'auroraBorder.medium',
        borderRadius: 'xl',
        backdropFilter: 'blur(10px)',
      },
      item: {
        color: 'white',
        _hover: {
          bg: 'auroraGlass.dark',
        },
      },
    },
  },
};

const styles = {
  global: {
    body: {
      bg: 'linear-gradient(135deg, auroraBg.start 0%, auroraBg.end 100%)',
      color: 'white',
      minHeight: '100vh',
      overflowX: 'hidden',
    },
    '*': {
      boxSizing: 'border-box',
    },
    '::-webkit-scrollbar': {
      width: '8px',
    },
    '::-webkit-scrollbar-track': {
      background: 'auroraGlass.light',
      borderRadius: '4px',
    },
    '::-webkit-scrollbar-thumb': {
      background: 'auroraAccent.primary',
      borderRadius: '4px',
      opacity: 0.3,
    },
    '::-webkit-scrollbar-thumb:hover': {
      background: 'auroraAccent.primary',
      opacity: 0.5,
    },
  },
};

const theme = extendTheme({
  config,
  colors,
  components,
  styles,
  fonts: {
    heading: 'Inter, system-ui, sans-serif',
    body: 'Inter, system-ui, sans-serif',
  },
  shadows: {
    aurora: '0 0 20px rgba(0, 255, 255, 0.3)',
    auroraHover: '0 0 30px rgba(0, 255, 255, 0.6)',
  },
});

export default theme;
