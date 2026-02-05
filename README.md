# Maritime Cloud Monitoring System 🚢☁️

## Περιγραφή Προβλήματος
Η σύγχρονη ναυτιλία διέπεται από αυστηρούς περιβαλλοντικούς κανονισμούς (όπως **EU MRV** και **IMO DCS**), οι οποίοι απαιτούν τη συνεχή και ακριβή παρακολούθηση της κατανάλωσης καυσίμων και των εκπομπών CO2.

Η παραδοσιακή μέθοδος καταγραφής (**Noon Reports**) είναι χειροκίνητη, επιρρεπής σε λάθη και δεν προσφέρει δεδομένα σε πραγματικό χρόνο. Το παρόν σύστημα αποτελεί μια **Cloud-Native λύση** που:
1. Συλλέγει **αυτοματοποιημένα** δεδομένα τηλεμετρίας.
2. Εντοπίζει **άμεσα** υπερβάσεις (Alerting).
3. **Αρχειοθετεί** με ασφάλεια τα περιστατικά για μελλοντικούς ελέγχους (Auditing).

---

## Αρχιτεκτονική Λύσης
Η εφαρμογή ακολουθεί αρχιτεκτονική **Microservices**, υλοποιημένη εξ ολοκλήρου με **Docker Containers**.

### Τα Υποσυστήματα:
| Υπηρεσία | Ρόλος & Λειτουργία |
| :--- | :--- |
| **Node-RED** | **IoT Edge & Simulation:** Λειτουργεί ως το Gateway του πλοίου. Προσομοιώνει αισθητήρες ροής καυσίμου και στέλνει δεδομένα μέσω MQTT. |
| **Thingsboard** | **IoT Platform:** Ο "εγκέφαλος". Υποδέχεται τα δεδομένα, τα οπτικοποιεί σε Dashboard και εκτελεί τους κανόνες ελέγχου (Rule Chains). |
| **RabbitMQ** | **Message Broker:** Εξασφαλίζει ασύγχρονη επικοινωνία. Διαχειρίζεται την ουρά των κρίσιμων συμβάντων (`critical_incidents`). |
| **Python Worker** | **Microservice:** Custom script που καταναλώνει μηνύματα από το RabbitMQ και δημιουργεί αναφορές (Reports). |
| **Minio** | **Object Storage:** Αποθηκεύει μόνιμα τα αρχεία καταγραφής (Logs) σε μορφή JSON (S3 compatible). |

---

## Ροή Δεδομένων (Data Pipeline)
Η διαδικασία από την παραγωγή δεδομένων μέχρι την αποθήκευση ακολουθεί τα εξής βήματα:

1. **Generation:** Το **Node-RED** παράγει δεδομένα κατανάλωσης (π.χ. 45 MT/day) κάθε 5 δευτερόλεπτα.
2. **Transmission:** Τα δεδομένα αποστέλλονται μέσω **MQTT** στο Thingsboard.
3. **Evaluation:** Το **Thingsboard** ελέγχει: *Είναι η κατανάλωση > 75;*
4. **Alerting:** Αν **ΝΑΙ**, το Thingsboard στέλνει μήνυμα στο **RabbitMQ** (Topic: `critical_incidents`).
5. **Processing:** Ο **Python Worker** λαμβάνει το μήνυμα και δημιουργεί δυναμικά ένα αρχείο JSON.
6. **Archiving:** Ο Worker ανεβάζει το αρχείο στο **Minio**.

---

## Τεχνολογίες & Εργαλεία
* **Containerization:** Docker & Docker Compose
* **Languages:** Python 3.9 (pika, minio libraries), JavaScript (Node-RED functions)
* **Protocols:** MQTT (Device -> Cloud), AMQP (Internal Messaging)
* **Storage:** PostgreSQL (Thingsboard DB), Minio (Object Storage)

---

## Οδηγίες Εγκατάστασης & Εκτέλεσης

### Προαπαιτούμενα
* Docker Desktop εγκατεστημένο.
* Git (προαιρετικά).

### Βήματα
1. Clone:
   ```bash
   git clone [https://github.com/natasa24/maritime-cloud-project.git](https://github.com/natasa24/maritime-cloud-project.git)
   cd maritime-cloud-project


