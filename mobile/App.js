import React, { useEffect } from 'react';
import { Button, Text, View } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
import api, { loginWithGoogle } from './src/api';

WebBrowser.maybeCompleteAuthSession();

export default function App() {
  const [request, response, promptAsync] = Google.useIdTokenAuthRequest({
    clientId: '679068442306-unmqvo1o8c5hk855g68dqh1pcqqes85p.apps.googleusercontent.com'
  });

  useEffect(() => {
    if (response?.type === 'success') {
      const id_token = response.params.id_token;
      // Use centralized API client login helper
      loginWithGoogle(id_token).then(data => {
        console.log('Logged in via backend', data);
      }).catch(err => console.error('Login failed', err));
    }
  }, [response]);

  // Helper: get stored access token
  async function getAccessToken() {
    return await SecureStore.getItemAsync('accessToken');
  }

  async function getRefreshToken() {
    return await SecureStore.getItemAsync('refreshToken');
  }

  async function setTokens(access, refresh) {
    if (access) await SecureStore.setItemAsync('accessToken', access);
    if (refresh) await SecureStore.setItemAsync('refreshToken', refresh);
  }

  async function clearTokens() {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
  }

  useEffect(() => {
    // api.js already configures interceptors; no-op here
    return () => {};
  }, []);

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 18, marginBottom: 12 }}>StudyBuddy Mobile</Text>
      <Button
        disabled={!request}
        title="Sign in with Google"
        onPress={() => promptAsync()}
      />
    </View>
  );
}
