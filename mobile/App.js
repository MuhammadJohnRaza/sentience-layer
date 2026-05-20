import React, { useState } from 'react';
import { View } from 'react-native';
import { useTheme } from './src/hooks/useTheme';

// Import Screens
import HomeScreen from './src/screens/HomeScreen';
import { ChatScreen } from './src/screens/ChatScreen';
import { DashboardScreen } from './src/screens/DashboardScreen';
import { SettingsScreen } from './src/screens/SettingsScreen';
import { ContentInputScreen } from './src/screens/ContentInputScreen';
import { ResultsScreen } from './src/screens/ResultsScreen';
import { SimulationScreen } from './src/screens/SimulationScreenNew';
import { BottomNav } from './src/components/BottomNav';

export default function App() {
  const theme = useTheme();
  const [activeRoute, setActiveRoute] = useState('Home');
  const [navigationParams, setNavigationParams] = useState({});

  // Enhanced navigation with params support
  const navigate = (route, params = {}) => {
    setActiveRoute(route);
    setNavigationParams(params);
  };

  const navigation = {
    navigate,
    goBack: () => setActiveRoute('Home'),
  };

  // Render screen based on active route
  const renderScreen = () => {
    const route = { params: navigationParams };

    switch (activeRoute) {
      case 'Home':
        return <HomeScreen navigation={navigation} />;
      case 'Chat':
        return <ChatScreen navigation={navigation} />;
      case 'Dashboard':
        return <DashboardScreen navigation={navigation} />;
      case 'Settings':
        return <SettingsScreen navigation={navigation} />;
      case 'ContentInput':
        return <ContentInputScreen navigation={navigation} route={route} />;
      case 'Results':
        return <ResultsScreen navigation={navigation} route={route} />;
      case 'Simulation':
        return <SimulationScreen navigation={navigation} route={route} />;
      default:
        return <HomeScreen navigation={navigation} />;
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: theme.colors.backgroundPrimary }}>
      {renderScreen()}
      <BottomNav activeRoute={activeRoute} onNavigate={navigate} />
    </View>
  );
}
