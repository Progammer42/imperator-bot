"""
KONFIGURATION - Die "Orders" fuer den Bot.
====================================================

Fuer jede Person gibt es zwei Orders:
- Eine fuer "timeout"
- Eine fuer "ban"

Wenn du eine neue Person hinzufuegen willst:
1. Kopiere einen der Bloecke unten
2. Aendere die Nummer (naechste freie Zahl, hier weiter mit 29)
3. Trage die neue user_id ein
4. Aendere "reason" auf den Namen der Person (nur zur Uebersicht fuer dich)

So findest du eine User-ID:
1. In Discord: Einstellungen -> Erweitert -> Entwicklermodus AKTIVIEREN
2. Rechtsklick auf die Person -> "ID kopieren"
"""

# Name der Rolle, die den Bot benutzen darf
ALLOWED_ROLE_NAME = "Der Imperator"

ORDERS = {
    # --- Alena ---
    1: {"user_id": 1333563674413109322, "action": "timeout", "timeout_minutes": 60, "reason": "Alena - Timeout"},
    2: {"user_id": 1333563674413109322, "action": "ban", "reason": "Alena - Ban"},

    # --- Noah ---
    3: {"user_id": 838431829773385773, "action": "timeout", "timeout_minutes": 60, "reason": "Noah - Timeout"},
    4: {"user_id": 838431829773385773, "action": "ban", "reason": "Noah - Ban"},

    # --- Emilia ---
    5: {"user_id": 1525968183197175849, "action": "timeout", "timeout_minutes": 60, "reason": "Emilia - Timeout"},
    6: {"user_id": 1525968183197175849, "action": "ban", "reason": "Emilia - Ban"},

    # --- Neo ---
    7: {"user_id": 944994110979330079, "action": "timeout", "timeout_minutes": 60, "reason": "Neo - Timeout"},
    8: {"user_id": 944994110979330079, "action": "ban", "reason": "Neo - Ban"},

    # --- Manuel ---
    9: {"user_id": 1237026561023016970, "action": "timeout", "timeout_minutes": 60, "reason": "Manuel - Timeout"},
    10: {"user_id": 1237026561023016970, "action": "ban", "reason": "Manuel - Ban"},

    # --- Maria ---
    11: {"user_id": 1549672223890079816, "action": "timeout", "timeout_minutes": 60, "reason": "Maria - Timeout"},
    12: {"user_id": 1549672223890079816, "action": "ban", "reason": "Maria - Ban"},

    # --- Matias ---
    13: {"user_id": 1443254817098170473, "action": "timeout", "timeout_minutes": 60, "reason": "Matias - Timeout"},
    14: {"user_id": 1443254817098170473, "action": "ban", "reason": "Matias - Ban"},

    # --- Ole ---
    15: {"user_id": 1345142671571681400, "action": "timeout", "timeout_minutes": 60, "reason": "Ole - Timeout"},
    16: {"user_id": 1345142671571681400, "action": "ban", "reason": "Ole - Ban"},

    # --- Patrick ---
    17: {"user_id": 1270096832474779803, "action": "timeout", "timeout_minutes": 60, "reason": "Patrick - Timeout"},
    18: {"user_id": 1270096832474779803, "action": "ban", "reason": "Patrick - Ban"},

    # --- Patrick der Zweite ---
    19: {"user_id": 1447160617071939755, "action": "timeout", "timeout_minutes": 60, "reason": "Patrick der Zweite - Timeout"},
    20: {"user_id": 1447160617071939755, "action": "ban", "reason": "Patrick der Zweite - Ban"},

    # --- Yousef ---
    21: {"user_id": 1158701964637511680, "action": "timeout", "timeout_minutes": 60, "reason": "Yousef - Timeout"},
    22: {"user_id": 1158701964637511680, "action": "ban", "reason": "Yousef - Ban"},

    # --- Lara ---
    23: {"user_id": 1463178018724909235, "action": "timeout", "timeout_minutes": 60, "reason": "Lara - Timeout"},
    24: {"user_id": 1463178018724909235, "action": "ban", "reason": "Lara - Ban"},

    # --- Luiess ---
    25: {"user_id": 1353740973397643368, "action": "timeout", "timeout_minutes": 60, "reason": "Luiess - Timeout"},
    26: {"user_id": 1353740973397643368, "action": "ban", "reason": "Luiess - Ban"},

    # --- Becki ---
    27: {"user_id": 1543660933153423435, "action": "timeout", "timeout_minutes": 60, "reason": "Becki - Timeout"},
    28: {"user_id": 1543660933153423435, "action": "ban", "reason": "Becki - Ban"},

    # --- Order 29 & 30: Alle mit der Rolle "..." bannen/timeouten ---
    # WICHTIG: role_name muss noch mit dem echten Rollennamen ersetzt werden!
    29: {"target": "role", "role_name": "Die Frauen", "action": "timeout", "timeout_minutes": 60, "reason": "Rollen-Order - Timeout"},
    30: {"target": "role", "role_name": "Die Frauen", "action": "ban", "reason": "Rollen-Order - Ban"},

    # --- Order 31: Statistik anzeigen (wie oft wurde welche Order ausgefuehrt) ---
    31: {"action": "stats", "reason": "Statistik"},

    # Naechste neue Order wuerde hier mit der Nummer 32 weitergehen.
}
