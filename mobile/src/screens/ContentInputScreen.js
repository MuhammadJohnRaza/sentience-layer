import React, { useState } from 'react';
import { StyleSheet, View, ScrollView, TextInput, TouchableOpacity, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';
import { ScreenWrapper } from '../components/ScreenWrapper';
import { TopBar } from '../components/TopBar';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Typography } from '../components/Typography';
import { useTheme } from '../hooks/useTheme';
import APIService from '../services/api';

export function ContentInputScreen({ navigation }) {
  const theme = useTheme();
  const [inputText, setInputText] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [processing, setProcessing] = useState(false);

  const handleTextSubmit = async () => {
    if (!inputText.trim()) {
      Alert.alert('Error', 'Please enter some text');
      return;
    }

    setProcessing(true);
    try {
      const result = await APIService.processQuery(inputText, {
        source: 'text_input',
        timestamp: new Date().toISOString(),
      });

      if (result.success) {
        navigation.navigate('Results', { data: result.data });
      } else {
        Alert.alert('Error', result.error || 'Processing failed');
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setProcessing(false);
    }
  };

  const handleDocumentPick = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'text/plain', 'text/markdown'],
        copyToCacheDirectory: true,
      });

      if (result.type === 'success') {
        setUploadedFile(result);
        Alert.alert('Success', `File selected: ${result.name}`);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick document');
    }
  };

  const handleImagePick = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert('Permission Required', 'Camera roll permission is required');
      return;
    }

    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
      });

      if (!result.canceled) {
        setUploadedFile(result.assets[0]);
        Alert.alert('Success', 'Image selected');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick image');
    }
  };

  const handleCameraCapture = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert('Permission Required', 'Camera permission is required');
      return;
    }

    try {
      const result = await ImagePicker.launchCameraAsync({
        quality: 0.8,
      });

      if (!result.canceled) {
        setUploadedFile(result.assets[0]);
        Alert.alert('Success', 'Photo captured');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to capture photo');
    }
  };

  const handleFileSubmit = async () => {
    if (!uploadedFile) {
      Alert.alert('Error', 'Please select a file first');
      return;
    }

    setProcessing(true);
    try {
      const uploadResult = await APIService.uploadDocument(uploadedFile, {
        source: 'mobile_upload',
        timestamp: new Date().toISOString(),
      });

      const result = await APIService.processQuery(
        `Analyze this document: ${uploadedFile.name || 'uploaded file'}`,
        {
          document_id: uploadResult.document_id,
          source: 'document_upload',
        }
      );

      if (result.success) {
        navigation.navigate('Results', { data: result.data });
      } else {
        Alert.alert('Error', result.error || 'Processing failed');
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <ScreenWrapper>
      <TopBar
        title="CONTENT INPUT"
        subtitle="📄 Multi-Modal Content Understanding"
        showStatus={true}
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        {/* Text Input Section */}
        <Card style={styles.section}>
          <Typography variant="h3" uppercase style={styles.sectionTitle}>
            Text Input
          </Typography>
          <Typography variant="body" style={styles.sectionDesc}>
            Enter text, reports, articles, or any unstructured content
          </Typography>

          <TextInput
            style={[styles.textInput, {
              color: theme.colors.textBody,
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              borderColor: theme.colors.border,
            }]}
            placeholder="Paste your content here..."
            placeholderTextColor={theme.colors.textMuted}
            value={inputText}
            onChangeText={setInputText}
            multiline
            numberOfLines={8}
          />

          <Button
            variant="primary"
            onPress={handleTextSubmit}
            disabled={processing || !inputText.trim()}
            style={styles.submitBtn}
          >
            <Typography variant="button">
              {processing ? 'PROCESSING...' : 'ANALYZE TEXT'}
            </Typography>
          </Button>
        </Card>

        {/* File Upload Section */}
        <Card style={styles.section}>
          <Typography variant="h3" uppercase style={styles.sectionTitle}>
            Document Upload
          </Typography>
          <Typography variant="body" style={styles.sectionDesc}>
            Upload PDF, images, or other documents
          </Typography>

          <View style={styles.uploadButtons}>
            <TouchableOpacity
              style={[styles.uploadBtn, { borderColor: theme.colors.border }]}
              onPress={handleDocumentPick}
            >
              <Typography style={styles.uploadIcon}>📄</Typography>
              <Typography variant="caption">Document</Typography>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.uploadBtn, { borderColor: theme.colors.border }]}
              onPress={handleImagePick}
            >
              <Typography style={styles.uploadIcon}>🖼️</Typography>
              <Typography variant="caption">Gallery</Typography>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.uploadBtn, { borderColor: theme.colors.border }]}
              onPress={handleCameraCapture}
            >
              <Typography style={styles.uploadIcon}>📷</Typography>
              <Typography variant="caption">Camera</Typography>
            </TouchableOpacity>
          </View>

          {uploadedFile && (
            <View style={[styles.filePreview, { borderColor: theme.colors.border }]}>
              <Typography variant="body" style={styles.fileName}>
                ✓ {uploadedFile.name || 'File selected'}
              </Typography>
            </View>
          )}

          <Button
            variant="secondary"
            onPress={handleFileSubmit}
            disabled={processing || !uploadedFile}
            style={styles.submitBtn}
          >
            <Typography variant="button">
              {processing ? 'UPLOADING...' : 'ANALYZE FILE'}
            </Typography>
          </Button>
        </Card>

        {/* Example Scenarios */}
        <Card style={styles.section}>
          <Typography variant="h3" uppercase style={styles.sectionTitle}>
            Example Scenarios
          </Typography>

          <TouchableOpacity
            style={styles.exampleBtn}
            onPress={() => setInputText('Sales report shows 25% decline in Lahore region this quarter. Customer complaints increased by 40%.')}
          >
            <Typography variant="body">📊 Business Report Analysis</Typography>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.exampleBtn}
            onPress={() => setInputText('Breaking: Fuel prices increased by 15% effective immediately. Transportation costs expected to rise.')}
          >
            <Typography variant="body">📰 News Article Impact</Typography>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.exampleBtn}
            onPress={() => setInputText('System logs show 500 errors spiking at 3 AM daily. Database connection timeouts detected.')}
          >
            <Typography variant="body">🔧 Technical Issue Detection</Typography>
          </TouchableOpacity>
        </Card>
      </ScrollView>
    </ScreenWrapper>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 100,
  },
  section: {
    marginBottom: 20,
    padding: 16,
  },
  sectionTitle: {
    marginBottom: 8,
  },
  sectionDesc: {
    marginBottom: 16,
    opacity: 0.7,
  },
  textInput: {
    fontSize: 14,
    fontWeight: '600',
    letterSpacing: 0.5,
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 16,
    minHeight: 150,
    textAlignVertical: 'top',
  },
  submitBtn: {
    marginTop: 8,
  },
  uploadButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  uploadBtn: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderStyle: 'dashed',
    width: '30%',
  },
  uploadIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  filePreview: {
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    marginBottom: 16,
    backgroundColor: 'rgba(124, 58, 237, 0.1)',
  },
  fileName: {
    textAlign: 'center',
  },
  exampleBtn: {
    padding: 12,
    marginBottom: 8,
    backgroundColor: 'rgba(124, 58, 237, 0.1)',
    borderRadius: 8,
  },
});
