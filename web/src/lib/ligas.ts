export const LIGAS = [
  { id: 1, nombre: 'Liga Profesional', pais: 'Argentina', code: 'AR' },
  { id: 3, nombre: 'Serie A', pais: 'Brasil', code: 'BR' },
  { id: 262, nombre: 'Liga MX', pais: 'México', code: 'MX' },
  { id: 140, nombre: 'La Liga', pais: 'España', code: 'ES' },
  { id: 39, nombre: 'Premier League', pais: 'Inglaterra', code: 'GB' },
  { id: 135, nombre: 'Serie A', pais: 'Italia', code: 'IT' },
  { id: 78, nombre: 'Bundesliga', pais: 'Alemania', code: 'DE' },
  { id: 61, nombre: 'Ligue 1', pais: 'Francia', code: 'FR' },
  { id: 94, nombre: 'Primeira Liga', pais: 'Portugal', code: 'PT' },
  { id: 88, nombre: 'Eredivisie', pais: 'Holanda', code: 'NL' },
  { id: 203, nombre: 'Süper Lig', pais: 'Turquía', code: 'TR' },
  { id: 307, nombre: 'Saudi Pro League', pais: 'Arabia Saudita', code: 'SA' },
  { id: 253, nombre: 'MLS', pais: 'USA', code: 'US' },
];

export function getLigaById(id: number) {
  return LIGAS.find(l => l.id === id);
}
