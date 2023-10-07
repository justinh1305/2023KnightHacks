import React from 'react';
import { Text, View, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Audio } from 'expo-av';
import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';
import * as FileSystem from 'expo-file-system';

const WHISPER_KEY = process.env.WHISPER_KEY;

export default class MainScreen extends React.Component {
    recording = null;
    sound = null;
    state = {
        isRecording: false,
        isPlaying: false
    }

    startRecording = async () => {
        try {
            console.log('Requesting permissions..');
            await Audio.requestPermissionsAsync();
            await Audio.setAudioModeAsync({
                    allowsRecordingIOS: true,
                    playsInSilentModeIOS: true,

            }); 

            console.log('Starting recording..');
            const { recording } = await Audio.Recording.createAsync(
                Audio.RecordingOptionsPresets.HIGH_QUALITY
            );

            this.recording = recording;
            this.setState({ isRecording: true });
            console.log('Recording started');
        } catch (err) {
            console.error('Failed to start recording', err);
        }
    }

    stopRecording = async () => {
        console.log('Stopping recording..');
        await this.recording.stopAndUnloadAsync();
        this.setState({ isRecording: false });
        console.log('Recording stopped');
    
        const recordingURI = this.recording.getURI();
        console.log(recordingURI);
        const fileInfo = await FileSystem.getInfoAsync(recordingURI);
        console.log(`The file size is ${fileInfo.size}`);
    
        let fileUriParts = recordingURI.split(".");
        let fileType = fileUriParts[fileUriParts.length - 1];
    
    
        let formData = new FormData();
        formData.append('file', {
            uri: recordingURI,
            name: `audio.${fileType}`,
            type: `audio/${fileType}`
        });
        formData.append('model', 'whisper-1');
    
        try {
            let res = await fetch("https://api.openai.com/v1/audio/transcriptions", {
                method: 'POST',
                body: formData,
                headers: {
                    Authorization: "Bearer " + WHISPER_KEY,
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            let resJson = await res.json();
            console.log(resJson);
            return resJson;
        } catch (error) {
            console.log('Error: ', error);
        }
    }

    playRecording = async () => {
        try {
            console.log('Loading sound..');
            const { sound } = await this.recording.createNewLoadedSoundAsync();
            this.sound = sound;
            console.log('Playing sound..');
            await this.sound.playAsync();
            this.setState({ isPlaying: true });
            console.log('Sound played');
        } catch (err) {
            console.error('Failed to play sound', err);
        }
    }

    stopPlaying = async () => {
        console.log('Stopping sound..');
        await this.sound.stopAsync();
        this.setState({ isPlaying: false });
        console.log('Sound stopped');
    }

    render () {
        return (
            <SafeAreaView style={styles.container}>
                <Text style={styles.heading}>Plan Your Trip</Text>
                <View style={styles.circle}>
                     <Image source={require('./assets/stonks.png')} style={styles.image} />
                </View>
                <Button
                    containerStyle={styles.buttonContainer}
                    buttonStyle={styles.button}
                    onPress={ this.state.isRecording ? this.stopRecording : this.startRecording }
                    icon={
                        <Icon
                        name="microphone"
                        size={15}
                        color="white"
                        />
                    }
                    title={ this.state.isRecording ? ' Stop Recording ' : ' Start Recording '}
                />
                {this.recording && !this.state.isRecording && (
                    <Button
                        containerStyle={styles.buttonContainer}
                        buttonStyle={styles.button}
                        onPress={ this.state.isPlaying ? this.stopPlaying : this.playRecording }
                        icon={
                            <Icon
                            name="play"
                            size={15}
                            color="white"
                            />
                        }
                        title={ this.state.isPlaying ? ' Stop Playing ' : ' Play Recording '}
                    />
                )}
            </SafeAreaView>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    heading: {
        fontSize: 24,
        fontWeight: 'bold'
    },
    circle: {
        width: 200,
        height: 200,
        borderRadius: 200/2,
        backgroundColor: 'skyblue',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 30,
        marginBottom: 30
    },
    image: {
        width: '100%',
        height: '100%',
        borderRadius: 200/2,
        resizeMode: 'cover'
    },
    buttonContainer: {
        marginVertical: 10,
        marginHorizontal: 20,
        width: '80%',
        alignSelf: 'center'
    },
    button: {
        backgroundColor: 'skyblue',
        borderRadius: 20,
        paddingVertical: 10,
        paddingHorizontal: 20
    }
});