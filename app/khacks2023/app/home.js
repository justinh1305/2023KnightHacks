import React from 'react';
import { Text, View, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Audio } from 'expo-av';
import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';
import * as FileSystem from 'expo-file-system';
import { router } from 'expo-router';


const WHISPER_KEY = process.env.WHISPER_KEY;

import where from './assets/where2.mp3';
import when from './assets/when2.mp3';
import ppl from './assets/ppl.mp3';
import trip_type from './assets/trip_type.mp3';
import budget_like from './assets/budget_like.mp3';

const QUESTIONS = [
    'Where are you going?',
    'When are you going & coming back?',
    'How many people are going?',
    'What type of trip is it?',
    'What is your budget like?',
];

const ASSETS = [
    where,
    when,
    ppl,
    trip_type,
    budget_like,
];

export default class MainScreen extends React.Component {

    recording = null;
    sound = null;
    state = {
        isRecording: false,
        isPlaying: false,
        currentAssetIndex: 0,
        whisperResponses: [],
    };


    async componentDidMount() {
        await Audio.requestPermissionsAsync();
        await Audio.setAudioModeAsync({
            allowsRecordingIOS: true,
            playsInSilentModeIOS: true,
        });
        this.playCurrentAsset();
    }

    async playCurrentAsset() {
        const asset = ASSETS[this.state.currentAssetIndex];
        const soundObject = new Audio.Sound();
        try {
            console.log(`Loading asset ${asset}..`);
            await soundObject.loadAsync(asset);
            await soundObject.setVolumeAsync(1);
            await soundObject.playAsync();
            soundObject.setOnPlaybackStatusUpdate((status) => {
                if (status.didJustFinish) {
                    this.stopPlaying();
                    this.startRecording();
                }
            });
            this.sound = soundObject;
            this.setState({ isPlaying: true });
            console.log(`Asset ${asset} played`);
        } catch (error) {
            console.error(`Failed to play asset ${asset}`, error);
        }
    }

    async startRecording() {
        try {
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

    async stopRecording(skipWhisper = false) {
        console.log('Stopping recording..');
        await this.recording.stopAndUnloadAsync();
        this.setState({ isRecording: false });
        console.log('Recording stopped');
        if (skipWhisper == true) {
            return;
        }
        const recordingURI = this.recording.getURI();
        console.log(recordingURI);
        const fileInfo = await FileSystem.getInfoAsync(recordingURI);
        console.log(`The file size is ${fileInfo.size}`);

        let fileUriParts = recordingURI.split('.');
        let fileType = fileUriParts[fileUriParts.length - 1];

        let formData = new FormData();
        formData.append('file', {
            uri: recordingURI,
            name: `audio.${fileType}`,
            type: `audio/${fileType}`,
        });
        formData.append('model', 'whisper-1');

        try {
            let res = await fetch('https://api.openai.com/v1/audio/transcriptions', {
                method: 'POST',
                body: formData,
                headers: {
                    Authorization: 'Bearer ' + WHISPER_KEY,
                    'Content-Type': 'multipart/form-data',
                },
            });

            let resJson = await res.json();
            console.log(resJson);
            this.handleWhisperOutput(resJson.text);
        } catch (error) {
            console.log('Error: ', error);
        }
    }

    handleWhisperOutput(text) {
        console.log(`Whisper output: ${text}`);
        const { currentAssetIndex, whisperResponses } = this.state;
        if (currentAssetIndex < ASSETS.length - 1) {
            this.setState({ currentAssetIndex: currentAssetIndex + 1, whisperResponses: [...whisperResponses, text] }, () => {
                this.playCurrentAsset();
            });
        } else {
            console.log('All assets played');
            this.setState({ whisperResponses: [...whisperResponses, text] });
            this.setState({ currentAssetIndex: 0 }); // reset currentAssetIndex to 0
            // Navigate to next screen and pass whisperResponses as props
            router.push({ pathname: '/results', params: { whisperResponses: whisperResponses } });
        }
    }

    async playRecording() {
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

    async stopPlaying() {
        console.log('Stopping sound..');
        await this.sound.stopAsync();
        this.setState({ isPlaying: false });
        console.log('Sound stopped');
    }

    render() {
        return (
            <SafeAreaView style={styles.container}>
                <Text style={styles.heading}>{QUESTIONS[this.state.currentAssetIndex]}</Text>
                <View style={styles.circle}>
                    <Image source={this.state.isPlaying ? require('./assets/dame.gif') : require('./assets/dameStatic.png')} style={styles.image} />
                </View>
                {this.state.isRecording && (
                    <Button
                        containerStyle={styles.buttonContainer}
                        buttonStyle={styles.button}
                        onPress={this.state.isRecording ? this.stopRecording.bind(this) : this.startRecording.bind(this)}
                        icon={
                            <Icon name="microphone" size={15} color="white" />
                        }
                        title={this.state.isRecording ? ' Stop Recording ' : ''}
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
        fontWeight: 'bold',
    },
    circle: {
        width: 200,
        height: 200,
        borderRadius: 200 / 2,
        backgroundColor: 'skyblue',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 30,
        marginBottom: 30,
    },
    image: {
        width: '100%',
        height: '100%',
        borderRadius: 200 / 2,
        resizeMode: 'cover',
    },
    buttonContainer: {
        marginVertical: 10,
        marginHorizontal: 20,
        width: '80%',
        alignSelf: 'center',
    },
    button: {
        backgroundColor: 'skyblue',
        borderRadius: 20,
        paddingVertical: 10,
        paddingHorizontal: 20,
    },
});