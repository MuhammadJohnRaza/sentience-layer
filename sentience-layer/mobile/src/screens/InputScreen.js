import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { useDispatch } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import VoiceRecorder from '../components/VoiceRecorder';
import CameraScanner from '../components/CameraScanner';
import { addInput } from '../store/workflowSlice';

const INPUT_TYPES = [
  { id: 'text', label: 'Text', icon: 'text' },
  { id: 'voice', label: 'Voice', icon: 'microphone' },
  { id: 'image', label: 'Scan', icon: 'camera' }
];

export default function InputScreen({ navigation }) {
  const dispatch = useDispatch();
  const [inputType, setInputType] = useState('text');
  const [textContent, setTextContent] = useState('');
  const [voiceUri, setVoiceUri] = useState(null);
  const [imageUri, setImageUri] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [priority, setPriority] = useState('normal');
  const inputRef = useRef(null);

  const handleSubmit = async () => {
    if (!textContent && !voiceUri && !imageUri) return;

    setIsProcessing(true);
    
    const inputData = {
      id: Date.now().toString(),
      type: inputType,
      content: textContent || (voiceUri ? 'Voice input' : 'Image input'),
      rawData: inputType === 'text' ? textContent : inputType === 'voice' ? voiceUri : imageUri,
      priority,
      timestamp: new Date().toISOString(),
      status: 'pending'
    };

    dispatch(addInput(inputData));
    
    setTimeout(() => {
      setIsProcessing(false);
      navigation.navigate('Workflow');
    }, 1500);
  };

  const renderInputArea = () => {
    switch (inputType) {
      case 'text':
        return (
          <TextInput
            ref={inputRef}
            style={styles.textInput}
            multiline
            placeholder="Describe your goal, problem, or idea..."
            placeholderTextColor="#4a4a6a"
            value={textContent}
            onChangeText={setTextContent}
            textAlignVertical="top"
          />
        );
      case 'voice':
        return <VoiceRecorder onRecordingComplete={setVoiceUri} />;
      case 'image':
        return <CameraScanner onCapture={setImageUri} />;
      default:
        return null;
    }
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView style={styles.scrollView} keyboardShouldPersistTaps="handled">
        <View style={styles.typeSelector}>
          {INPUT_TYPES.map(type => (
            <TouchableOpacity
              key={type.id}
              style={[
                styles.typeButton,
                inputType === type.id && styles.typeButtonActive
              ]}
              onPress={() => setInputType(type.id)}
            >
              <Icon 
                name={type.icon} 
                size={20} 
                color={inputType === type.id ? '#4f46e5' : '#6b6b8a'} 
              />
              <Text style={[
                styles.typeLabel,
                inputType === type.id && styles.typeLabelActive
              ]}>
                {type.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.inputContainer}>
          {renderInputArea()}
        </View>

        <View style={styles.priorityContainer}>
          <Text style={styles.sectionLabel}>Priority</Text>
          <View style={styles.priorityButtons}>
            {['low', 'normal', 'high', 'critical'].map(p => (
              <TouchableOpacity
                key={p}
                style={[
                  styles.priorityButton,
                  priority === p && styles.priorityButtonActive,
                  priority === p && { backgroundColor: 
                    p === 'low' ? '#10b98120' : 
                    p === 'normal' ? '#4f46e520' : 
                    p === 'high' ? '#f59e0b20' : '#ef444420' 
                  }
                ]}
                onPress={() => setPriority(p)}
              >
                <View style={[
                  styles.priorityDot,
                  { backgroundColor: 
                    p === 'low' ? '#10b981' : 
                    p === 'normal' ? '#4f46e5' : 
                    p === 'high' ? '#f59e0b' : '#ef4444' 
                  }
                ]} />
                <Text style={[
                  styles.priorityText,
                  priority === p && styles.priorityTextActive
                ]}>
                  {p.charAt(0).toUpperCase() + p.slice(1)}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.metadataContainer}>
          <Text style={styles.sectionLabel}>Context Tags</Text>
          <View style={styles.tagContainer}>
            {['Strategy', 'Operations', 'Finance', 'Product', 'Marketing', 'HR'].map(tag => (
              <TouchableOpacity key={tag} style={styles.tag}>
                <Text style={styles.tagText}>{tag}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={[
            styles.submitButton,
            (!textContent && !voiceUri && !imageUri) && styles.submitButtonDisabled
          ]}
          onPress={handleSubmit}
          disabled={(!textContent && !voiceUri && !imageUri) || isProcessing}
        >
          {isProcessing ? (
            <Text style={styles.submitButtonText}>Processing...</Text>
          ) : (
            <>
              <Icon name="send" size={20} color="#ffffff" />
              <Text style={styles.submitButtonText}>Submit to Sentience Kernel</Text>
            </>
          )}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a1a'
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20
  },
  typeSelector: {
    flexDirection: 'row',
    marginTop: 20,
    backgroundColor: '#1a1a3e',
    borderRadius: 12,
    padding: 4,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  typeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    borderRadius: 8,
    gap: 6
  },
  typeButtonActive: {
    backgroundColor: '#0f0f23'
  },
  typeLabel: {
    fontSize: 14,
    color: '#6b6b8a',
    fontWeight: '500'
  },
  typeLabelActive: {
    color: '#4f46e5',
    fontWeight: '600'
  },
  inputContainer: {
    marginTop: 20,
    minHeight: 200
  },
  textInput: {
    backgroundColor: '#1a1a3e',
    borderRadius: 16,
    padding: 16,
    color: '#e0e0ff',
    fontSize: 16,
    lineHeight: 24,
    borderWidth: 1,
    borderColor: '#2a2a4a',
    minHeight: 200,
    textAlignVertical: 'top'
  },
  priorityContainer: {
    marginTop: 24
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#e0e0ff',
    marginBottom: 12
  },
  priorityButtons: {
    flexDirection: 'row',
    gap: 8
  },
  priorityButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: '#1a1a3e',
    borderWidth: 1,
    borderColor: '#2a2a4a',
    gap: 6
  },
  priorityButtonActive: {
    borderColor: '#4f46e5'
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4
  },
  priorityText: {
    fontSize: 12,
    color: '#6b6b8a'
  },
  priorityTextActive: {
    color: '#e0e0ff',
    fontWeight: '600'
  },
  metadataContainer: {
    marginTop: 24,
    marginBottom: 20
  },
  tagContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8
  },
  tag: {
    backgroundColor: '#1a1a3e',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#2a2a4a'
  },
  tagText: {
    fontSize: 13,
    color: '#6b6b8a'
  },
  footer: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#0a0a1a',
    borderTopWidth: 1,
    borderTopColor: '#1a1a3e'
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4f46e5',
    paddingVertical: 16,
    borderRadius: 14,
    gap: 8
  },
  submitButtonDisabled: {
    backgroundColor: '#2a2a4a'
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600'
  }
});