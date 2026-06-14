import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import { fetchStandings, fetchFixtures } from '../api/client';

export default function MundialScreen() {
  const [tab, setTab] = useState('groups');
  const [groups, setGroups] = useState([]);
  const [fixtures, setFixtures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchStandings(), fetchFixtures()])
      .then(([g, f]) => { setGroups(g); setFixtures(f); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <ActivityIndicator style={{ marginTop: 40 }} color="#10B981" size="large" />;

  const tabs = [
    { key: 'groups', label: 'Grupos' },
    { key: 'fixtures', label: 'Partidos' },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mundial 2026</Text>
      <View style={styles.tabBar}>
        {tabs.map(t => (
          <Text
            key={t.key}
            style={[styles.tab, tab === t.key && styles.tabActive]}
            onPress={() => setTab(t.key)}
          >
            {t.label}
          </Text>
        ))}
      </View>

      {tab === 'groups' && (
        <FlatList
          data={groups}
          keyExtractor={g => g.name}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.groupTitle}>{item.name}</Text>
              {item.teams.map(team => (
                <View key={team.team_id} style={styles.teamRow}>
                  <Text style={styles.pos}>{team.position}</Text>
                  <Text style={styles.flag}>{team.team_logo}</Text>
                  <Text style={styles.teamName}>{team.team_name}</Text>
                  <Text style={styles.stat}>{team.played}</Text>
                  <Text style={styles.statBold}>{team.points}</Text>
                </View>
              ))}
            </View>
          )}
        />
      )}

      {tab === 'fixtures' && (
        <FlatList
          data={fixtures}
          keyExtractor={f => String(f.id)}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.fixtureRow}>
                <Text style={styles.teamName}>{item.home.name}</Text>
                <View style={styles.score}>
                  {item.status === 'FT' ? (
                    <>
                      <Text style={styles.scoreText}>{item.goals.home ?? '-'}</Text>
                      <Text style={styles.vs}>vs</Text>
                      <Text style={styles.scoreText}>{item.goals.away ?? '-'}</Text>
                    </>
                  ) : (
                    <Text style={styles.scheduled}>{item.status}</Text>
                  )}
                </View>
                <Text style={[styles.teamName, styles.right]}>{item.away.name}</Text>
              </View>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', paddingTop: 50, paddingHorizontal: 12 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginBottom: 16, textAlign: 'center' },
  tabBar: { flexDirection: 'row', marginBottom: 16, gap: 12 },
  tab: { color: '#64748B', fontSize: 16, paddingBottom: 4, borderBottomWidth: 2, borderBottomColor: 'transparent' },
  tabActive: { color: '#10B981', borderBottomColor: '#10B981' },
  card: { backgroundColor: '#1E293B', borderRadius: 12, padding: 12, marginBottom: 12 },
  groupTitle: { color: '#10B981', fontWeight: 'bold', fontSize: 14, marginBottom: 8, textTransform: 'uppercase' },
  teamRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 4, gap: 8 },
  pos: { color: '#64748B', width: 20, textAlign: 'center' },
  flag: { fontSize: 16 },
  teamName: { color: '#fff', flex: 1, fontSize: 14 },
  right: { textAlign: 'right' },
  stat: { color: '#64748B', width: 24, textAlign: 'center' },
  statBold: { color: '#fff', fontWeight: 'bold', width: 24, textAlign: 'center' },
  fixtureRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  score: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  scoreText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  vs: { color: '#64748B', fontSize: 12 },
  scheduled: { color: '#FBBF24', fontSize: 12 },
});
