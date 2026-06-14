import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';

const features = [
  { emoji: '⚽', title: 'Mundial 2026', desc: 'Grupos, resultados y goleadores en vivo' },
  { emoji: '📰', title: 'Noticias', desc: 'Últimas noticias de tus equipos favoritos' },
  { emoji: '📊', title: 'Estadísticas', desc: 'Tablas de posiciones y estadísticas detalladas' },
];

export default function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>BotiFutbol ⚽</Text>
      <Text style={styles.subtitle}>Tu asistente personal de fútbol</Text>

      <View style={styles.features}>
        {features.map((f, i) => (
          <View key={i} style={styles.card}>
            <Text style={styles.emoji}>{f.emoji}</Text>
            <Text style={styles.cardTitle}>{f.title}</Text>
            <Text style={styles.cardDesc}>{f.desc}</Text>
          </View>
        ))}
      </View>

      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Mundial')}>
        <Text style={styles.buttonText}>Ver Mundial 2026</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', paddingTop: 60, paddingHorizontal: 16 },
  title: { fontSize: 32, fontWeight: 'bold', color: '#10B981', textAlign: 'center' },
  subtitle: { fontSize: 16, color: '#64748B', textAlign: 'center', marginBottom: 32, marginTop: 8 },
  features: { gap: 12, marginBottom: 24 },
  card: { backgroundColor: '#1E293B', borderRadius: 12, padding: 16, marginBottom: 12 },
  emoji: { fontSize: 28, marginBottom: 8 },
  cardTitle: { color: '#fff', fontSize: 18, fontWeight: 'bold', marginBottom: 4 },
  cardDesc: { color: '#94A3B8', fontSize: 14 },
  button: { backgroundColor: '#10B981', borderRadius: 12, padding: 16, alignItems: 'center', marginBottom: 40 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});
