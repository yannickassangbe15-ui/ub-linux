import threading
import sys
import time

# ─────────────────────────────────────────
#  Couleurs terminal (ANSI)
# ─────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
ORANGE = "\033[38;5;208m"
GRAY   = "\033[90m"

# ─────────────────────────────────────────
#  Helpers affichage
# ─────────────────────────────────────────
def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════╗
║        🔗  J O R D Y   G A M E       ║
║  Chaîne de mots — 30 sec par mot     ║
╚══════════════════════════════════════╝{RESET}
{GRAY}Règle : chaque mot doit commencer par
la DERNIÈRE lettre du mot précédent.{RESET}
""")

def badge(score):
    if score >= 10:
        return f"{YELLOW}{BOLD}🏆 LEGENDARY !{RESET}"
    elif score >= 5:
        return f"{CYAN}{BOLD}⚡ Excellent !{RESET}"
    elif score >= 3:
        return f"{GREEN}{BOLD}😎 Nice combo !{RESET}"
    elif score >= 1:
        return f"{GREEN}👍 Good start !{RESET}"
    return ""

def afficher_chaine(chaine):
    if not chaine:
        return
    parts = []
    for i, mot in enumerate(chaine):
        if i < len(chaine) - 1:
            parts.append(f"{CYAN}{mot[:-1]}{BOLD}{ORANGE}{mot[-1]}{RESET}")
        else:
            parts.append(f"{CYAN}{mot[:-1]}{BOLD}{YELLOW}{mot[-1]}{RESET}")
    print(f"  {GRAY}Chaîne :{RESET} " + f" {GRAY}→{RESET} ".join(parts))

def barre_timer(secondes_restantes, total=30):
    largeur = 30
    rempli = int(largeur * secondes_restantes / total)
    barre = "█" * rempli + "░" * (largeur - rempli)
    couleur = RED if secondes_restantes <= 8 else (YELLOW if secondes_restantes <= 15 else GREEN)
    print(f"  {couleur}[{barre}] {secondes_restantes:2d}s{RESET}", end="\r", flush=True)

# ─────────────────────────────────────────
#  Timer avec thread
# ─────────────────────────────────────────
class Timer:
    def __init__(self, duree=30):
        self.duree = duree
        self.temps_restant = duree
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while self.temps_restant > 0 and not self._stop.is_set():
            barre_timer(self.temps_restant, self.duree)
            time.sleep(1)
            self.temps_restant -= 1
        if not self._stop.is_set():
            # Temps écoulé — interrompre l'input
            print(f"\n\n  {RED}{BOLD}⏰ Temps écoulé !{RESET}")
            # Envoie une ligne vide pour débloquer input()
            sys.stdin.close()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    def expire(self):
        return self.temps_restant <= 0

# ─────────────────────────────────────────
#  Lecture sécurisée avec timeout
# ─────────────────────────────────────────
def lire_mot(prompt, timeout=30):
    """Lit un mot avec un timeout. Retourne None si le temps est écoulé."""
    resultat = [None]
    expiration = [False]

    def _lire():
        try:
            resultat[0] = input(prompt)
        except EOFError:
            expiration[0] = True

    t = threading.Thread(target=_lire, daemon=True)
    t.start()
    t.join(timeout=timeout + 1)   # +1 pour laisser le timer afficher le message

    if expiration[0] or resultat[0] is None:
        return None
    return resultat[0].strip().lower()

# ─────────────────────────────────────────
#  Jeu principal
# ─────────────────────────────────────────
def jouer():
    banner()

    meilleur_score = 0

    while True:
        score = 0
        chaine = []

        # ── Premier mot (pas de timer) ──
        print(f"{BOLD}Entre le premier mot pour commencer :{RESET}")
        mot = input("  → ").strip().lower()

        if not mot:
            print(f"  {RED}Le mot ne peut pas être vide.{RESET}\n")
            continue

        chaine.append(mot)
        print()
        afficher_chaine(chaine)
        print()

        # ── Boucle principale ──
        while True:
            lettre_attendue = chaine[-1][-1]
            print(f"\n  {GRAY}Le prochain mot doit commencer par :{RESET} "
                  f"{BOLD}{ORANGE}{lettre_attendue.upper()}{RESET}")
            print(f"  {GRAY}(Score actuel : {score}){RESET}\n")

            # Lancer le timer visuel
            timer = Timer(duree=30)
            timer.start()

            mot_suivant = lire_mot("  → ", timeout=30)

            timer.stop()
            print()  # Effacer la ligne du timer

            # Temps écoulé
            if mot_suivant is None or timer.expire():
                print(f"  {RED}{BOLD}Game Over !{RESET}")
                break

            # Mot vide
            if not mot_suivant:
                print(f"  {RED}Rejeté : le mot ne doit pas être vide.{RESET}")
                continue

            # Vérification de la lettre
            if mot_suivant[0] != lettre_attendue:
                print(f"  {RED}{BOLD}❌ Échec !{RESET}")
                print(f"  « {mot_suivant} » ne commence pas par "
                      f"{BOLD}{ORANGE}{lettre_attendue.upper()}{RESET}.")
                print(f"  {RED}Game Over !{RESET}")
                break

            # Bonne réponse
            chaine.append(mot_suivant)
            score += 1
            print(f"  {GREEN}{BOLD}✅ Congrats !{RESET}")
            afficher_chaine(chaine)
            b = badge(score)
            if b:
                print(f"  {b}")

        # ── Fin de partie ──
        if score > meilleur_score:
            meilleur_score = score

        print(f"""
{CYAN}{BOLD}══════════════════════════════════════{RESET}
  {BOLD}Score final   :{RESET}  {YELLOW}{score} mot{"s" if score > 1 else ""}{RESET}
  {BOLD}Meilleur score:{RESET}  {YELLOW}{meilleur_score}{RESET}
  {badge(score)}
{CYAN}{BOLD}══════════════════════════════════════{RESET}
""")

        rejouer = input("  Rejouer ? (o/n) : ").strip().lower()
        if rejouer != "o":
            print(f"\n  {CYAN}Merci d'avoir joué ! À bientôt 👋{RESET}\n")
            break
        print()


# ─────────────────────────────────────────
if __name__ == "__main__":
    jouer()
