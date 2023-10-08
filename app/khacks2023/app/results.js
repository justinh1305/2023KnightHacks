import React, { useState, useEffect } from 'react';
import { TouchableOpacity, View, Text, Image, StyleSheet, SafeAreaView, ActivityIndicator } from 'react-native';
import axios from 'axios';
import { useLocalSearchParams } from 'expo-router';
import { ScrollView } from 'react-native';

const itineraryData = [
    {
        day: 'Day 1',
        items: [
            {
                name: 'Museum of Modern Art',
                location: 'New York, NY',
                price: '$$',
            },
            {
                name: 'Central Park',
                location: 'New York, NY',
                price: '$',
            },
            {
                name: 'Statue of Liberty',
                location: 'New York, NY',
                price: '$$$',
            },
        ]
    },
    {
        day: 'Day 2',
        items: [
            {
                name: 'Empire State Building',
                location: 'New York, NY',
                price: '$$',
            },
            {
                name: 'Brooklyn Bridge',
                location: 'New York, NY',
                price: '$',
            },
            {
                name: 'Times Square',
                location: 'New York, NY',
                price: '$',
            },
        ]
    },
];

export default function ResultsScreen() {
    const [loading, setLoading] = useState(true);
    const [itineraryData, setItineraryData] = useState([]);
    const item = useLocalSearchParams();

    useEffect(() => {
        const sendWhisperResponse = async () => {
            try {
                const res = await axios.post('http://a3ed-132-170-212-13.ngrok-free.app/initiate-plan', { "input_str": item.whisperResponse });
                console.log(res.data);
                const results = res.data.results;
                const itinerary = [];
                results.forEach((day, index) => {
                    const dayData = {
                        day: `Day ${index + 1}`,
                        items: day.map(destination => ({
                            name: destination.name,
                            location: `${destination.lat}, ${destination.lng}`,
                            price: destination.price_level === 1 ? '$' : destination.price_level === 2 ? '$$' : '$$$',
                        }))
                    };
                    itinerary.push(dayData);
                });
                setItineraryData(itinerary);
                setLoading(false);
            } catch (error) {
                console.error(error);
                setLoading(false);
            }
        };
        sendWhisperResponse();
    }, []);

    const renderItineraryItem = (item, index) => {
        return (
            <TouchableOpacity key={index} style={styles.itineraryItem}>
                <View style={styles.itineraryItemInfo}>
                    <Text style={styles.itineraryItemTitle}>{item.name}</Text>
                    <Text style={styles.itineraryItemSubtitle}>{item.location}</Text>
                </View>
                <Text style={styles.itineraryItemPrice}>{item.price}</Text>
            </TouchableOpacity>
        );
    };

    const renderItineraryDay = (day) => {
        return (
            <View key={day.day} style={styles.itineraryDay}>
                <Text style={styles.itineraryDayTitle}>{day.day}</Text>
                {day.items.map((item, index) => renderItineraryItem(item, index))}
            </View>
        );
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Itinerary</Text>
            </View>
            {loading ? (
                <View style={styles.loadingContainer}>
                    <ActivityIndicator size="large" color="#0000ff" />
                </View>
            ) : (
                <ScrollView style={styles.itineraryList}>
                    {itineraryData.map((day) => renderItineraryDay(day))}
                </ScrollView>
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        height: 60,
        backgroundColor: '#fff',
        justifyContent: 'center',
        alignItems: 'center',
        borderBottomWidth: 1,
        borderBottomColor: '#ddd',
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    itineraryList: {
        flex: 1,
        backgroundColor: '#f5f5f5',
        padding: 20,
    },
    itineraryDay: {
        marginBottom: 20,
    },
    itineraryDayTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    itineraryItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#fff',
        borderRadius: 10,
        padding: 20,
        marginBottom: 10,
    },
    itineraryItemInfo: {
        flex: 1,
    },
    itineraryItemTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    itineraryItemSubtitle: {
        fontSize: 16,
        color: '#666',
    },
    itineraryItemPrice: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    button: {
        backgroundColor: '#2196F3',
        padding: 10,
        borderRadius: 5,
        margin: 20,
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});