import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Import Screens
import HomeScreen from '../screens/HomeScreen';
import DashboardScreen from '../screens/DashboardScreen';
import InputScreen from '../screens/InputScreen';
import WorkflowScreen from '../screens/WorkflowScreen';
import SimulationScreen from '../screens/SimulationScreen';
import MemoryScreen from '../screens/MemoryScreen';
import DreamScreen from '../screens/DreamScreen';
import DoubtScreen from '../screens/DoubtScreen';
import CausalScreen from '../screens/CausalScreen';
import EconomyScreen from '../screens/EconomyScreen';
import ActionScreen from '../screens/ActionScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#0a0a1a',
            elevation: 0,
            shadowOpacity: 0,
            borderBottomWidth: 1,
            borderBottomColor: '#1a1a3e',
          },
          headerTintColor: '#e0e0ff',
          headerTitleStyle: {
            fontWeight: 'bold',
            letterSpacing: 1,
          },
          cardStyle: { backgroundColor: '#0a0a1a' },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ title: 'SENTIENCE CORE' }} 
        />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="Input" component={InputScreen} options={{ title: 'Comm Link' }} />
        <Stack.Screen name="Workflow" component={WorkflowScreen} options={{ title: 'Trace' }} />
        <Stack.Screen name="Simulation" component={SimulationScreen} options={{ title: 'Simulate' }} />
        <Stack.Screen name="Memory" component={MemoryScreen} />
        <Stack.Screen name="Dreamscape" component={DreamScreen} />
        <Stack.Screen name="Doubt" component={DoubtScreen} options={{ title: 'Doubt Room' }} />
        <Stack.Screen name="Causal" component={CausalScreen} options={{ title: 'Causal Graph' }} />
        <Stack.Screen name="Economy" component={EconomyScreen} options={{ title: 'Economic Model' }} />
        <Stack.Screen name="Action" component={ActionScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
