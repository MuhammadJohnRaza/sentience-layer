import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Import Screens (matching exactly the newly created screens)
import { MissionControlScreen } from '../screens/MissionControlScreen';
import { DashboardScreen } from '../screens/DashboardScreen';
import { ChatScreen } from '../screens/ChatScreen';
import { TraceScreen } from '../screens/TraceScreen';
import { SimulationScreen } from '../screens/SimulationScreen';
import { MemoryScreen } from '../screens/MemoryScreen';
import { DreamscapeScreen } from '../screens/DreamscapeScreen';
import { DoubtRoomScreen } from '../screens/DoubtRoomScreen';
import { CausalExplorerScreen } from '../screens/CausalExplorerScreen';
import { EconomicModelScreen } from '../screens/EconomicModelScreen';
import { ActionScreen } from '../screens/ActionScreen';
import { PlaybookScreen } from '../screens/PlaybookScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { MirrorScreen } from '../screens/MirrorScreen';
import { VaultScreen } from '../screens/VaultScreen';
import { WinScreen } from '../screens/WinScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="MissionControl"
        screenOptions={{
          headerShown: false, // We use custom TopBar component inside each screen instead
          cardStyle: { backgroundColor: '#050505' },
        }}
      >
        <Stack.Screen name="MissionControl" component={MissionControlScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="Chat" component={ChatScreen} />
        <Stack.Screen name="Trace" component={TraceScreen} />
        <Stack.Screen name="Simulation" component={SimulationScreen} />
        <Stack.Screen name="Memory" component={MemoryScreen} />
        <Stack.Screen name="Dreamscape" component={DreamscapeScreen} />
        <Stack.Screen name="DoubtRoom" component={DoubtRoomScreen} />
        <Stack.Screen name="CausalExplorer" component={CausalExplorerScreen} />
        <Stack.Screen name="EconomicModel" component={EconomicModelScreen} />
        <Stack.Screen name="Action" component={ActionScreen} />
        <Stack.Screen name="Playbook" component={PlaybookScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
        <Stack.Screen name="Mirror" component={MirrorScreen} />
        <Stack.Screen name="Vault" component={VaultScreen} />
        <Stack.Screen name="Win" component={WinScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
