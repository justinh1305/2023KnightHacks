import React from 'react';
import { TouchableOpacity, View, Text, Image, StyleSheet, SafeAreaView } from 'react-native';
import Swiper from 'react-native-swiper';
import { router } from 'expo-router';

export default function NewScreen() {
  const handlePress = () => {
    router.replace('/home');
  };

  return (
    <SafeAreaView style={styles.container}>
      <Swiper style={styles.wrapper} showsButtons={true}>
        <View style={styles.slide}>
          <Image source={require('./assets/stonks.png')} style={styles.image} />
          <Text style={styles.header}>Step 1</Text>
          <Text style={styles.text}>This is the step 1 for the tutorial</Text>
        </View>
        <View style={styles.slide}>
          <Image source={require('./assets/stonks.png')} style={styles.image} />
          <Text style={styles.header}>Step 2</Text>
          <Text style={styles.text}>This is the step 2 for the tutorial</Text>
        </View>
        <View style={styles.slide}>
          <Image source={require('./assets/stonks.png')} style={styles.image} />
          <Text style={styles.header}>Step 3</Text>
          <Text style={styles.text}>This is the step 3 for the tutorial - nate</Text>
          <TouchableOpacity onPress={handlePress}>
            <Text>Go to Home Screen</Text>
          </TouchableOpacity>
        </View>
      </Swiper>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  wrapper: {},
  slide: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  image: {
    width: 300,
    height: 300,
    marginBottom: 40,
  },
  header: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 20,
  },
  text: {
    color: '#000',
    fontSize: 18,
  },
});
