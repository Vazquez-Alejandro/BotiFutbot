import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import { fetchStandings, fetchFixtures, fetchTopScorers } from '../api/client';

export default function MundialScreen() {
  const [tab, setTab] = useState('groups');
  const [groups, setGroups] = useState([]);
  const [fixtures, setFixtures] = useState([]);
  const [scorers, setScorers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchStandings(), fetchFixtures(), fetchTopScorers()])
      .then(([g, f, s]) => { setGroups(g); setFixtures(f); setScorers(s); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <ActivityIndicator style={{ marginTop: 40 }} color="#10B981" size="large" />;

  const tabs = [
    { key: 'groups', label: 'Grupos' },
    { key: 'fixtures', label: 'Partidos' },
    { key: 'scorers', label: 'Goleadores' },
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
                  <Text style={styles.teamName}>{team.team_name}</Text>
                  <View style={styles.stats}>
                    <Text style={styles.stat}>{team.played}</Text>
                    <Text style={[styles.stat, { width: 32 }]}>{team.goal_difference > 0 ? '+' : ''}{team.goal_difference}</Text>
                    <Text style={styles.statBold}>{team.points}</Text>
                  </View>
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
          renderItem={({ item }) => {
            const isFinished = item.status === 'FT';
            const isLive = item.status === 'LIVE';
            return (
              <View style={styles.card}>
                <View style={styles.fixtureRow}>
                  <View style={styles.teamSide}>
                    <Text style={styles.fixtureTeamName}>{item.home.name}</Text>
                  </View>
                  <View style={styles.scoreCol}>
                    {isLive && <View style={styles.liveDot} />}
                    {isFinished ? (
                      <View style={styles.scoreRow}>
                        <Text style={styles.scoreText}>{item.goals.home ?? '-'}</Text>
                        <Text style={styles.scoreSep}>-</Text>
                        <Text style={styles.scoreText}>{item.goals.away ?? '-'}</Text>
                      </View>
                    ) : (
                      <Text style={styles.scheduled}>
                        {new Date(item.date).toLocaleDateString('es', { day: 'numeric', month: 'short' })}
                      </Text>
                    )}
                  </View>
                  <View style={styles.teamSideRight}>
                    <Text style={styles.fixtureTeamName}>{item.away.name}</Text>
                  </View>
                </View>
              </View>
            );
          }}
        />
      )}

      {tab === 'scorers' && (
        <FlatList
          data={scorers}
          keyExtractor={s => s.team_code}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyTitle}>Sin datos de goleadores</Text>
              <Text style={styles.emptySub}>Disponible con API key de datos en vivo</Text>
            </View>
          }
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.scorerRow}>
                <Text style={styles.scorerPos}>{item.position}</Text>
                <View style={styles.scorerInfo}>
                  <Text style={styles.scorerTeam}>{item.team_name}</Text>
                  <Text style={styles.scorerMeta}>{item.matches} PJ</Text>
                </View>
                <View style={styles.scorerGoalsCol}>
                  <Text style={styles.scorerGoals}>{item.goals}</Text>
                  <Text style={styles.scorerAvg}>{item.avg}/p</Text>
                </View>
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
  teamRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 4 },
  pos: { color: '#64748B', width: 24, fontSize: 14 },
  teamName: { color: '#fff', flex: 1, fontSize: 14 },
  stats: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  stat: { color: '#64748B', width: 24, textAlign: 'center', fontSize: 13 },
  statBold: { color: '#fff', fontWeight: 'bold', width: 28, textAlign: 'center', fontSize: 14 },
  fixtureRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  teamSide: { flex: 1, alignItems: 'flex-start' },
  teamSideRight: { flex: 1, alignItems: 'flex-end' },
  fixtureTeamName: { color: '#fff', fontSize: 13, fontWeight: '500' },
  scoreCol: { alignItems: 'center', marginHorizontal: 12, minWidth: 60 },
  liveDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#10B981', marginBottom: 4 },
  scoreRow: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  scoreText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  scoreSep: { color: '#64748B', fontSize: 14 },
  scheduled: { color: '#FBBF24', fontSize: 11, textAlign: 'center' },
  empty: { alignItems: 'center', paddingVertical: 40 },
  emptyTitle: { color: '#64748B', fontSize: 16, marginBottom: 4 },
  emptySub: { color: '#475569', fontSize: 12 },
  scorerRow: { flexDirection: 'row', alignItems: 'center' },
  scorerPos: { color: '#64748B', width: 28, fontSize: 14, fontWeight: 'bold' },
  scorerInfo: { flex: 1 },
  scorerTeam: { color: '#fff', fontSize: 14, fontWeight: '500' },
  scorerMeta: { color: '#64748B', fontSize: 11, marginTop: 2 },
  scorerGoalsCol: { alignItems: 'center' },
  scorerGoals: { color: '#FBBF24', fontSize: 22, fontWeight: 'bold' },
  scorerAvg: { color: '#64748B', fontSize: 10 },
});
