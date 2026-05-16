import React from 'react';
import { BaseScreen } from './src/components/BaseScreen';
import { Typography } from './src/components/Typography';
import { ActionCard } from './src/components/ActionCard';
import { ScrollView, View } from 'react-native';

export default function App() {
  return (
    <BaseScreen>
      <ScrollView>
        <Typography variant="h1">Sentience Layer</Typography>
        <Typography variant="body" style={{ marginBottom: 24 }}>
          A Cognitive Operating System where AI agents reason, simulate, and act.
        </Typography>

        <Typography variant="h2">Active Operations</Typography>
        <ActionCard 
          title="Market Analysis" 
          description="Analyzing real-time market trends and competitor behavior."
          status="active"
          onPress={() => console.log('Action pressed')}
        />
        <ActionCard 
          title="Strategic Simulation" 
          description="Running Monte Carlo simulations on project outcomes."
          status="active"
          onPress={() => console.log('Action pressed')}
        />
        <ActionCard 
          title="Risk Assessment" 
          description="Evaluating potential system failures and recovery paths."
          status="pending"
          onPress={() => console.log('Action pressed')}
        />
      </ScrollView>
    </BaseScreen>
  );
}
