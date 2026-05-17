import React, { useState, useEffect } from 'react';
import { StyleSheet, TouchableOpacity, View, Text, Animated } from 'react-native';
import { Mic, Square } from 'lucide-react-native';

const PRIMARY_NEON = '#7A2EFF';
const PRIMARY_GLOW = '#9B5CFF';
const BACKGROUND_SECONDARY = '#0B0B12';
const TEXT_HIGHLIGHT = '#F5F5F7';
const TEXT_MUTED = '#A7A7B5';

export function VoiceRecorder({ onRecordStart, onRecordStop }) {
  const [isRecording, setIsRecording] = useState(false);
  const [pulseAnim] = useState(new Animated.Value(1));

  useEffect(() => {
    let animation;
    if (isRecording) {
      animation = Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.5,
            duration: 800,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          })
        ])
      );
      animation.start();
    } else {
      pulseAnim.setValue(1);
    }
    return () => animation && animation.stop();
  }, [isRecording, pulseAnim]);

  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false);
      if (onRecordStop) onRecordStop();
    } else {
      setIsRecording(true);
      if (onRecordStart) onRecordStart();
    }
  };

  return (
    <View style={styles.container}>
      <Animated.View style={[
        styles.pulseCircle, 
        isRecording && { transform: [{ scale: pulseAnim }], opacity: 0.3 }
      ]} />
      <TouchableOpacity 
        style={[styles.recordButton, isRecording && styles.recordingActive]} 
        onPress={toggleRecording}
      >
        {isRecording ? (
          <Square color={TEXT_HIGHLIGHT} size={24} fill={TEXT_HIGHLIGHT} />
        ) : (
          <Mic color={TEXT_HIGHLIGHT} size={24} />
        )}
      </TouchableOpacity>
      {isRecording && <Text style={styles.recordingText}>Listening to environment...</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  pulseCircle: {
    position: 'absolute',
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: PRIMARY_GLOW,
    opacity: 0,
  },
  recordButton: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: 'rgba(122, 46, 255, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(122, 46, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: PRIMARY_GLOW,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 8,
  },
  recordingActive: {
    backgroundColor: 'rgba(255, 69, 58, 0.2)', // Danger red tint for recording
    borderColor: '#FF453A',
    shadowColor: '#FF453A',
  },
  recordingText: {
    color: '#FF453A',
    marginTop: 12,
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 1,
    textShadowColor: 'rgba(255, 69, 58, 0.5)',
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 5,
  }
});
