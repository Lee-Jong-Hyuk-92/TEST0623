// frontend/app/screens/CameraScreen.tsx

import React, { useState } from 'react';
import { View, Text, Button, Image, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';
import { SERVER_URL } from '../constants/server';

export default function CameraScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({ base64: false });
    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      uploadImage(uri);
    }
  };

  const uploadImage = async (uri: string) => {
    const formData = new FormData();
    formData.append('file', {
      uri,
      name: 'photo.jpg',
      type: 'image/jpeg',
    } as any);

    try {
      const res = await axios.post(`${SERVER_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log('✅ 업로드 성공:', res.data);
      setResultImage(`${SERVER_URL}/uploads/result.jpg`);
    } catch (error) {
      console.error('❌ 업로드 실패:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="사진 업로드" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={styles.image} />}
      {resultImage && (
        <>
          <Text style={styles.resultLabel}>예측 결과</Text>
          <Image source={{ uri: resultImage }} style={styles.image} />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 20 },
  image: { width: 300, height: 300, marginVertical: 10, resizeMode: 'contain' },
  resultLabel: { fontSize: 16, fontWeight: 'bold', marginTop: 20 },
});