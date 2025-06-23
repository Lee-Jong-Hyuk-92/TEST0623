// frontend/App.tsx

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import CameraScreen from './app/screens/CameraScreen';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator screenOptions={({ route }) => ({
        tabBarIcon: ({ color, size }) => {
          let iconName = route.name === 'Camera' ? 'camera' : 'home';
          return <Ionicons name={iconName as any} size={size} color={color} />;
        },
      })}>
        <Tab.Screen name="Camera" component={CameraScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}