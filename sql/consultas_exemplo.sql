SELECT
    u.nome AS usuario,
    s.nome AS sala,
    r.inicio,
    r.fim
FROM reservas r
INNER JOIN usuarios u ON r.id_usuario = u.id
INNER JOIN salas s ON r.id_sala = s.id
ORDER BY r.inicio;

SELECT *
FROM reservas
WHERE id_sala = 1
  AND fim > '2026-10-15 10:30:00'
  AND inicio < '2026-10-15 11:30:00';