



INSERT OR IGNORE INTO "user" ("email", "firstName", "password", "isAdmin", "profile_picture")
VALUES
  ('user1@gso.schule.koeln', 'Max', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user2@gso.schule.koeln', 'Anna', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user3@gso.schule.koeln', 'David', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user4@gso.schule.koeln', 'Sophie', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user5@gso.schule.koeln', 'Paul', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user6@gso.schule.koeln', 'Lena', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user7@gso.schule.koeln', 'Felix', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user8@gso.schule.koeln', 'Emma', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user9@gso.schule.koeln', 'Tim', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 0, ''),
  ('user10@gso.schule.koeln', 'Sarah', '$2a$10$TyB6RZYjz90cN9Zxt2k4D.YWQxW65SPmIV96IeFprvqps/19PNlum', 1, '');

INSERT INTO "group" ("ownerID", "title", "description", "maxUsers")
VALUES
  (101, 'Deutsch Lerngruppe 1', 'Eine Lerngruppe, um Deutsch zu lernen.', 10),
  (102, 'Deutsch Lerngruppe 2', 'Wir lernen gemeinsam Deutsch.', 8),
  (103, 'Studium Unterstützungsgruppe', 'Hilfe und Unterstützung für Studenten.', 15),
  (104, 'Deutsch Sprachaustausch', 'Deutsch-Englisch Sprachaustauschgruppe.', 12),
  (105, 'Lerngruppe für Grammatik', 'Wir üben gemeinsam Grammatik.', 10),
  (106, 'Deutsch Konversationsübung', 'Üben der mündlichen Kommunikation auf Deutsch.', 8),
  (107, 'Lesegruppe für deutsche Literatur', 'Wir lesen und diskutieren deutsche Literatur.', 10),
  (108, 'Prüfungsvorbereitung', 'Gemeinsame Vorbereitung auf Deutschprüfungen.', 12),
  (109, 'Deutsch Schreibwerkstatt', 'Wir verbessern gemeinsam unsere Schreibfertigkeiten auf Deutsch.', 8),
  (110, 'Deutsch für Anfänger', 'Lerngruppe für Personen, die gerade erst mit dem Deutschlernen begonnen haben.', 10);

INSERT OR IGNORE INTO "users_in_groups" ("userID", "groupID", "startingDate")
VALUES
  ((SELECT userID FROM "user" WHERE email = 'user1@gso.schule.koeln'), 1, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user2@gso.schule.koeln'), 2, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user3@gso.schule.koeln'), 3, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user4@gso.schule.koeln'), 4, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user5@gso.schule.koeln'), 5, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user6@gso.schule.koeln'), 6, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user7@gso.schule.koeln'), 7, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user8@gso.schule.koeln'), 8, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user9@gso.schule.koeln'), 9, '2024-03-10'),
  ((SELECT userID FROM "user" WHERE email = 'user10@gso.schule.koeln'), 10, '2024-03-10');

INSERT INTO "date" ("groupID", "date", "place", "maxUsers")
VALUES
  (1, '2024-03-12 15:00:00', 'Bibliothek', 15),
  (2, '2024-03-14 16:30:00', 'Café', 10),
  (3, '2024-03-16 18:00:00', 'Hörsaal A', 20),
  (4, '2024-03-18 17:00:00', 'Online', 15),
  (5, '2024-03-20 14:00:00', 'Klassenzimmer 101', 12),
  (6, '2024-03-22 19:00:00', 'Cafeteria', 10),
  (7, '2024-03-24 16:00:00', 'Bibliothek', 15),
  (8, '2024-03-26 15:30:00', 'Hörsaal B', 18),
  (9, '2024-03-28 17:30:00', 'Klassenzimmer 203', 10),
  (10, '2024-03-30 18:00:00', 'Online', 20);
