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
      <Swiper style={styles.wrapper} showsButtons={false}>
        <View style={styles.slide}>
          <Text style={styles.header}>Welcome to</Text>
          <Image source={require('./assets/dameStatic.png')} style={styles.image}/>

          <Image source={require('./assets/dame_logo.png')} style={styles.image}/>
          <Text style={styles.text}>Your one stop shop for adventure</Text>

        </View>
        <View style={styles.slide}>
          <Text style={styles.header}>Dame is going to ask you some questions...</Text>
          <Image source={require('./assets/dame.gif')} style={styles.image}/>
        </View>
        <View style={styles.slide}>
          <Text style={styles.header}>When Dame is done talking...</Text>
          <Image source={require('./assets/dameStatic.png')} style={styles.image}/>
          <Text style={styles.footheader}>You will be prompted to speak! When you finish, press send</Text>
          <TouchableOpacity onPress={handlePress} style={styles.btnNav}>
            <Text style={{color:'#fff'}}> Click Here to start </Text>
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
    height: 150,
    marginBottom: 40,
  },
  header: {
    fontSize: 45,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 60,
  },
  footheader: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#000',
  },
  text: {
    color: '#000',
    fontSize: 20,
  },
  btnNav: {
    backgroundColor: '#000',
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
    color: '#fff',
  },
});
