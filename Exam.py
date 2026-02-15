import time
import random
import re
from typing import List, Dict, Any, Optional

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from docx import Document

APP_TITLE = "מבחן תקשוב / CCNA - אינטראקטיבי"

# Whiteboard sizing
BOARD_W = 820
BOARD_H = 700

# -------------------------
# Fixed question bank (Hebrew exam you pasted earlier)
# difficulty: easy/medium/hard
# type: mcq/open
# -------------------------
BASE_QUESTIONS: List[Dict[str, Any]] = [
    # 1
    {
        "id": 1, "type": "mcq", "difficulty": "easy", "topic": "Media / Cabling",
        "question": "יש לחבר בין שני נתבים המרוחקים כ-80 מטר זה מזה, להעברת נתונים בקצב גבוה ככל האפשר. התשתית עוברת בסמוך לכבל חשמל.\nבאיזו מדיה פיזית מומלץ להשתמש בהנחה שיש את כל המשקיעים המתאימים?",
        "choices": {
            "א": "כבל נחושת בתצורת כבל-ישיר (Straight cable) בין שני הנתבים",
            "ב": "כבל נחושת בתצורת כבל-מוצלב (Cross cable) בין שני הנתבים",
            "ג": "כבל Coax לחיבור בין שני הנתבים",
            "ד": "סיב אופטי בין שני הנתבים",
        },
        "answer": "ד",
        "explain": "סיב אופטי מתאים למרחק, קצב גבוה, וחסין להפרעות EMI מכבל חשמל."
    },

    # 2
    {
        "id": 2, "type": "open", "difficulty": "easy", "topic": "IP Addressing",
        "question": "השלימו את טבלת ההמרות הבאה עבור הכתובת: 192.168.200.240\n\nעשרוני: 192 | 168 | 200 | 240\nבינארי:\nהקסדצימלי:",
        "explain": "כתוב את 4 האוקטטים בבינארי (8 ביט) ובהקס (2 ספרות)."
    },

    # 3
    {
        "id": 3, "type": "mcq", "difficulty": "easy", "topic": "Broadcast / Collision Domains",
        "question": "טופולוגיה: 3 כיתות, בכל כיתה המחשבים מחוברים ל-Hub. בין הכיתות מחבר מתג Switch0. כל המחשבים במתג Switch0 מוגדרים ל-VLAN1.\nאיזה מבין ההיגדים הבאים נכון?",
        "choices": {
            "א": "כל הכיתות מחוברות לאותו מתחם התנגשות (Collision Domain).",
            "ב": "כשמחשב PC0 משדר לכל (Broadcast) – ה-Broadcast יגיע לכל המחשבים בטופולוגיה.",
            "ג": "חייבים להוסיף נתב ולהגדיר ניתוב כדי שתהיה תקשורת בין הכיתות.",
            "ד": "חייבים להגדיר לכל כיתה כתובת IP מרשת אחרת כדי שהעברת הנתונים תגיע לכל המחשבים.",
        },
        "answer": "ב",
        "explain": "VLAN1 זה Broadcast Domain אחד; Hub לא חוסם Broadcast."
    },

    # 4
    {
        "id": 4, "type": "mcq", "difficulty": "medium", "topic": "ARP",
        "question": "שאלות 4–5 מתייחסות לטופולוגיה: PC0 ו-PC1 מחוברים ל-Switch0; Switch0 מחובר ל-Router0; Router0 מחובר ל-Router1; Router1 מחובר ל-Server0.\n\nנתון כי טבלת ה-ARP ב-PC0 ריקה. PC0 רוצה לשלוח הודעה ל-PC1 ולכן שולח ARP Request.\nמהי כתובת ה-MAC שאותה יבקש PC0 למצוא?",
        "choices": {
            "א": "הכתובת של PC1",
            "ב": "הכתובת של Router0",
            "ג": "הכתובת של Router1",
            "ד": "הכתובת של Server0",
        },
        "answer": "א",
        "explain": "PC1 באותה רשת מקומית – צריך MAC של היעד עצמו."
    },

    # 5
    {
        "id": 5, "type": "mcq", "difficulty": "medium", "topic": "ARP / Default Gateway",
        "question": "בטופולוגיה של שאלה 4: טבלת ARP של PC0 ריקה. PC0 רוצה לשלוח הודעה ל-Server0.\nאיזו כתובת MAC הוא יבקש למצוא ב-ARP Request?",
        "choices": {
            "א": "הכתובת של PC1",
            "ב": "הכתובת של Router0",
            "ג": "הכתובת של Router1",
            "ד": "הכתובת של Server0",
        },
        "answer": "ב",
        "explain": "יעד מרוחק -> צריך MAC של ה-Default Gateway (Router0) במקטע המקומי."
    },

    # 6
    {
        "id": 6, "type": "mcq", "difficulty": "easy", "topic": "L2 vs L3",
        "question": "PC0: 200.6.6.6 / 255.255.255.240\nPC1: 200.5.5.5 / 255.255.255.240\nמהו התקן הרשת שיחבר אותם בהתחשב בכתובות?",
        "choices": {
            "א": "נתב (Router)",
            "ב": "מתג שכבה 2 (Layer 2 Switch)",
            "ג": "רכזת (Hub)",
            "ד": "מגביר אות (Repeater)",
        },
        "answer": "א",
        "explain": "הם ברשתות שונות (Subnet שונות), צריך ניתוב (Router)."
    },

    # 7
    {
        "id": 7, "type": "mcq", "difficulty": "easy", "topic": "UDP",
        "question": "מה היתרון של UDP כאשר מדובר בשיחות וידאו בזמן אמת?",
        "choices": {
            "א": "מאבטח את הנתונים הנשלחים",
            "ב": "מבטיח שכל המנות יגיעו",
            "ג": "מבצע אימות עם שרת היעד שהוא מאזין לפורט",
            "ד": "מהיר ואינו יוצר השהיות במקרה של אובדן מנות",
        },
        "answer": "ד",
        "explain": "UDP נמנע מ-handshake ורה-שידור -> פחות Latency."
    },

    # 8a
    {
        "id": 8, "type": "mcq", "difficulty": "easy", "topic": "Ports / Telnet",
        "question": "בבדיקת אבטחה הסתבר שהנתב מאזין בפורט 23/TCP. באיזה פרוטוקול ניתן להתחבר לנתב?",
        "choices": {"א": "HTTPS", "ב": "Telnet", "ג": "SNMP", "ד": "SSH"},
        "answer": "ב",
        "explain": "23/TCP = Telnet."
    },

    # 8b
    {
        "id": 9, "type": "mcq", "difficulty": "easy", "topic": "Security / SSH",
        "question": "בהמשך לשאלה 8: איזו המלצה תינתן לשיפור האבטחה בנתב?",
        "choices": {
            "א": "לכבות את הנתב לגמרי",
            "ב": "להתקין ולהגדיר SSH כתקשורת בטוחה יותר",
            "ג": "להתחבר דרך דפדפן",
            "ד": "להתקין ולהגדיר TFTP כדרך תקשורת בטוחה יותר",
        },
        "answer": "ב",
        "explain": "SSH מוצפן ובטוח יותר מ-Telnet."
    },

    # 9 (subnet table)
    {
        "id": 10, "type": "open", "difficulty": "medium", "topic": "Subnetting",
        "question": "השלימו את החסר בטבלה:\n\n1) ________ | bits subnet: 2 | subnets: 4 | host bits: 6 | hosts: 62\n2) 255.255.255.248 | bits subnet: 5 | subnets: ________ | host bits: 3 | hosts: ________\n3) ________ | bits subnet: ________ | subnets: 16 | host bits: 4 | hosts: 14",
        "explain": "השתמש/י בנוסחאות: subnets=2^n, hosts=(2^h)-2."
    },

    # 10
    {
        "id": 11, "type": "mcq", "difficulty": "easy", "topic": "Routing Design",
        "question": "באיזה סוג ניתוב לא מומלץ להשתמש ברשתות גדולות ומורכבות מאוד?",
        "choices": {
            "א": "ניתוב סטטי (Static Routing)",
            "ב": "ניתוב דינמי (Dynamic Routing)",
            "ג": "Link State Routing",
            "ד": "Distance Vector Routing",
        },
        "answer": "א",
        "explain": "סטטי לא סקלבילי לרשת גדולה ושינויי טופולוגיה."
    },

    # 11 (OSPF commands)
    {
        "id": 12, "type": "open", "difficulty": "medium", "topic": "OSPF",
        "question": "השלימו את החסר (פקודות OSPF):\n\nRouter(config)# router ospf ____\nRouter(config-router)# network ____ ____ area ____\nRouter(config-router)# network ____ ____ area ____\nRouter(config-router)# passive-interface ____\nRouter(config-router)# end",
        "explain": "מזהה תהליך OSPF + network עם wildcard + area + passive-interface."
    },

    # 12 matching
    {
        "id": 13, "type": "open", "difficulty": "easy", "topic": "Basic Protocols",
        "question": "התאימו לכל פעולה את הפרוטוקול (DHCP / DNS / ARP / ICMP):\nא. המרת שם מתחם לכתובת IP: ________\nב. הקצאת כתובות IP אוטומטית: ________\nג. בדיקת תקשורת (Ping): ________\nד. המרת כתובת IP לכתובת MAC ברשת מקומית: ________",
        "explain": "DNS->IP, DHCP->הקצאה, ICMP->ping, ARP->IP->MAC."
    },

    # 13 true/false
    {
        "id": 14, "type": "open", "difficulty": "easy", "topic": "FTP / TFTP",
        "question": "סמנו נכון/לא נכון:\nא. FTP משתמש ב-TCP להעברת קבצים.\nב. TFTP משתמש ב-UDP ולכן אמין יותר מ-FTP.\nג. FTP תומך באימות משתמשים.\nד. TFTP מתאים להעברת קבצים פשוטה ללא אימות מורכב.",
        "explain": "TFTP ב-UDP, פשוט ולא אמין יותר; FTP עם TCP ואימות."
    },

    # 14 (Cisco config error) - open
    {
        "id": 15, "type": "open", "difficulty": "medium", "topic": "Cisco Config",
        "question": "לפניכם קטע קונפיגורציה (Cisco). מה הבעיה/השגיאה בקונפיגורציה? (כתוב/י מה לא תקין.)",
        "explain": "תאר/י את השגיאה הלוגית/תחבירית וההשפעה שלה."
    },

    # 15 IPv6 type
    {
        "id": 16, "type": "mcq", "difficulty": "medium", "topic": "IPv6",
        "question": "לאיזה סוג כתובת ב-IPv6 שייכת כתובת שעושה תקשורת בין תתי-רשתות, אך אינה ניתנת לניתוב באינטרנט?",
        "choices": {"א": "Global Unicast", "ב": "Link-Local", "ג": "Multicast", "ד": "Unique Local"},
        "answer": "ד",
        "explain": "Unique Local (fc00::/7) – פנימית, לא ניתוב באינטרנט."
    },

    # 16 misconfigured gateway/DNS
    {
        "id": 17, "type": "mcq", "difficulty": "medium", "topic": "IP Configuration",
        "question": "IPv4: 192.168.30.1, Mask: 255.255.255.0, GW: 192.168.60.254, DNS: 0.0.0.0\nסמנו את ההיגד הנכון:",
        "choices": {
            "א": "המחשב יכול לתקשר עם רשתות אחרות",
            "ב": "לא יכול לתקשר כי DNS לא חוקי",
            "ג": "לא יכול לתקשר כי אין התאמה בין IP ל-Default Gateway",
            "ד": "יכול לתקשר למרות הבעיה ב-DNS מול שער היציאה",
        },
        "answer": "ג",
        "explain": "Gateway חייב להיות באותה רשת של המחשב (192.168.30.0/24)."
    },

    # 17-18 refer topology/outputs - open + mcq
    {
        "id": 18, "type": "open", "difficulty": "medium", "topic": "Commands / Outputs",
        "question": "שאלות 17–18 מתייחסות לטופולוגיה ולפלטים.\n17)\nא. איזו פקודה יש להקליד ב-PC0 כדי לקבל את פלט 1?\nב. איזו פקודה יש להקליד ב-Switch0 כדי לקבל את פלט 2?",
        "explain": "תן/י פקודות נפוצות כמו ipconfig/ifconfig, show mac address-table וכו'."
    },
    {
        "id": 19, "type": "mcq", "difficulty": "medium", "topic": "Ping / Destination",
        "question": "18) PC0 שולח ping ל-192.168.1.3 – לאיזה מחשב תישלח ההודעה?",
        "choices": {"א": "PC0", "ב": "PC1", "ג": "PC2", "ד": "PC3"},
        "answer": "ג",
        "explain": "בהנחה שה-IP 192.168.1.3 משויך ל-PC2 בטופולוגיה."
    },

    # 19-20 IPv6 classify + compress
    {
        "id": 20, "type": "mcq", "difficulty": "easy", "topic": "IPv6 Link-Local",
        "question": "כתובת IPv6: fe80:0000:0000:0000:0f4b:ccfe:0000:d42f\nלאיזה סוג שייכת הכתובת?",
        "choices": {"א": "Link-Local", "ב": "Global Unicast", "ג": "Global Broadcast", "ד": "Loopback"},
        "answer": "א",
        "explain": "fe80::/10 = Link-Local."
    },
    {
        "id": 21, "type": "mcq", "difficulty": "medium", "topic": "IPv6 Compression",
        "question": "איזו כתובת היא קיצור חוקי ל:\nfe80:0000:0000:0000:0f4b:ccfe:0000:d42f",
        "choices": {
            "א": "fe80::0f4b:ccfe::d42f",
            "ב": "fe80::f4b:ccfe:0:d42f",
            "ג": "fe8::f4b:ccfe:0:d42f",
            "ד": "fe80:f4b:ccfe:d42f",
        },
        "answer": "ב",
        "explain": "מותר להחליף רצף אחד של 0000 ב-::, ולהשמיט אפסים מובילים בהקטטים."
    },

    # 21 port-security
    {
        "id": 22, "type": "open", "difficulty": "medium", "topic": "Port Security",
        "question": "במתג Switch1 הוגדר Port Security על Gig0/1 והממשק ננעל. לפי פלט (שאצלך בשאלה) מה הסיבה לנעילה?",
        "explain": "בד\"כ violation בגלל חריגה ממספר MACs מותר, או sticky+שינוי MAC."
    },

    # 22 routing source chosen (AD)
    {
        "id": 23, "type": "open", "difficulty": "medium", "topic": "Administrative Distance",
        "question": "בנתב פועלים EIGRP, OSPF וגם Static Route, וכולם מגיעים ל-192.168.50.0/24.\nבהנחה ברירות מחדל – איזה מקור ניתוב ייבחר? (כתוב באנגלית)",
        "explain": "Static AD=1 (ברירת מחדל) לרוב עדיף על OSPF(110) ו-EIGRP(90/170)."
    },

    # 23 statements static routing T/F
    {
        "id": 24, "type": "open", "difficulty": "medium", "topic": "Static Routing",
        "question": "קבעו נכון/לא נכון לכל היגד על Static Route:\nא. חבילה עוברת רק דרך מסלול שקבע מנהל רשת.\nב. סטטי מתאים עצמו לשינויים אוטומטית.\nג. סטטי מבטיח ניתוב חסר שגיאות.\nד. בסטטי תמיד נבחר המסלול הקצר ביותר.\nה. אפשר להגדיר סטטי כגיבוי למסלול דינמי באמצעות AD גבוה יותר.",
        "explain": "הדגשה: ב' ג' ד' בדרך כלל לא נכונים; ה' נכון (floating static)."
    },

    # 24 DHCP relay
    {
        "id": 25, "type": "mcq", "difficulty": "medium", "topic": "DHCP Relay",
        "question": "Laptop לא מצליח לקבל IPv4. בטופולוגיה יש Router עם פלט פקודות. מה הסיבה הסבירה?",
        "choices": {
            "א": "שרת DHCP חייב להיות באותה רשת של ה-Laptop",
            "ב": "DHCP חייב להיות מוגדר רק בנתב",
            "ג": "חייבים ip address dhcp בממשק G0/0/1",
            "ד": "הפקודה ip helper-address שהוגדרה לא מתאימה",
        },
        "answer": "ד",
        "explain": "ברשתות שונות צריך DHCP relay, ואם helper שגוי לא יעבוד."
    },

    # 25-26 multi-part (open)
    {
        "id": 26, "type": "open", "difficulty": "hard", "topic": "Addressing / Topology",
        "question": "שאלות 25–26 (ענה על 4 בלבד במקור).\n25) לפי טופולוגיה ופקודות:\nא. מה שם הנתב?\nב. הציעו כתובת IP חוקית ל-PC2.",
        "explain": "ענה לפי הטופולוגיה/הגדרות שקיימות אצלך בעמוד."
    },
    {
        "id": 27, "type": "open", "difficulty": "hard", "topic": "Addressing / Broadcast Domains",
        "question": "26) לפי טופולוגיה ופקודות:\nא. הציעו כתובת IP חוקית למדפסת PRINTER.\nב. מה Default Gateway של המדפסת?\nג. השלימו: מספר Broadcast Domains ___ ; מספר Collision Domains ___",
        "explain": "Broadcast Domain נקבע לפי VLAN/Router; Collision Domains לפי פורטים/Hub."
    },

    # 27 ACL
    {
        "id": 28, "type": "open", "difficulty": "hard", "topic": "ACL / SSH",
        "question": "נדרש למנוע ממחשב 172.16.1.33 להתחבר מרחוק ב-SSH, ולכל השאר לאפשר.\nהשלימו ACL:\naccess-list 120 ______ ______ 172.16.1.33 ______ any eq ______\naccess-list 120 ______ ip ______ ______",
        "explain": "בדרך כלל deny tcp host <ip> any eq 22 ואז permit ip any any."
    },

    # 28a Router-on-a-stick path
    {
        "id": 29, "type": "mcq", "difficulty": "hard", "topic": "VLAN / Router-on-a-stick",
        "question": "Router-on-a-stick מוגדר, VLANs תקין.\nא. PC0 שולח ל-PC4. מה המסלול?",
        "choices": {
            "א": "PC0 → Switch0 → Router1 → Switch0 → Switch1 → PC4",
            "ב": "PC0 → Switch0 → Switch1 → PC4",
            "ג": "PC0 → Switch0 → Router1 → Switch0 → Switch1 → Router1 → PC4",
            "ד": "ההודעה לא תעבור",
        },
        "answer": "א",
        "explain": "אם PC0 ו-PC4 ב-VLAN שונים -> חייבים לעבור דרך Router1."
    },

    # 28b
    {
        "id": 30, "type": "mcq", "difficulty": "hard", "topic": "VLAN / Router-on-a-stick",
        "question": "Router-on-a-stick מוגדר, VLANs תקין.\nב. PC0 שולח ל-PC5. מה המסלול?",
        "choices": {
            "א": "PC0 → Switch0 → Router1 → Switch0 → Switch1 → PC5",
            "ב": "PC0 → Switch0 → Switch1 → PC5",
            "ג": "PC0 → Switch0 → Router1 → Switch0 → Switch1 → Router1 → PC5",
            "ד": "ההודעה לא תעבור",
        },
        "answer": "א",
        "explain": "כמו 28א – בין VLANs -> Router1."
    },

    # 29 ACL blocks (open)
    {
        "id": 31, "type": "open", "difficulty": "hard", "topic": "ACL",
        "question": "להגדיר ACL כך שלכל המשתמשים ברשת 10.10.0.0/16 לא תתאפשר גישה לנתב Jerusalem.\n(בחר/י את בלוק הפקודות הנכון א/ב/ג/ד לפי מה שמופיע במבחן אצלך.)",
        "explain": "כאן צריך את בלוקי הפקודות המקוריים כדי לענות בדיוק."
    },

    # 30a NAT inbound
    {
        "id": 32, "type": "mcq", "difficulty": "hard", "topic": "NAT / Port Forwarding",
        "question": "WR0 מוגדר NAT Overload וכו'.\nא. לאפשר גישה מהאינטרנט לשרת TFTP פנימי – איזו תכונה תפעיל בנתב?",
        "choices": {
            "א": "Port forwarding של פורט 69 לכתובת השרת",
            "ב": "Port forwarding של פורט 22 לכתובת השרת",
            "ג": "חסימת MAC של שרת ה-TFTP ב-Firewall",
            "ד": "חסימת פורט TFTP",
        },
        "answer": "א",
        "explain": "TFTP משתמש ב-UDP/69, נדרש Port Forward."
    },

    # 30b NAT source IP
    {
        "id": 33, "type": "mcq", "difficulty": "hard", "topic": "NAT / Source IP",
        "question": "ב. Laptop0 שולח ל-HTTP server. איזו כתובת תופיע כ-Source IP כשהחבילה תגיע לשרת?",
        "choices": {
            "א": "192.168.0.101",
            "ב": "255.255.255.0",
            "ג": "48.117.231.25",
            "ד": "הכתובת של ה-Wireless Router",
        },
        "answer": "ג",
        "explain": "עם NAT Overload כלפי חוץ, השרת יראה את ה-Public IP (למשל 48.117.231.25)."
    },
]


# -------------------------
# DOCX parser for "Networking Exam A.docx" style (Question 1 ... Answer: ...)
# Removes answers, keeps questions only.
# -------------------------
QUESTION_HDR = re.compile(r"^\s*Question\s+(\d+)\b", re.IGNORECASE)
BONUS_HDR = re.compile(r"^\s*⭐\s*Bonus\s+Question", re.IGNORECASE)

def parse_networking_exam_a_docx(docx_path: str, id_start: int = 2000) -> List[Dict[str, Any]]:
    doc = Document(docx_path)
    lines = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]

    out: List[Dict[str, Any]] = []
    cur_num: Optional[int] = None
    cur_lines: List[str] = []
    in_answer = False
    in_bonus = False

    def topic_from_text(t: str) -> str:
        u = t.lower()
        if "dhcp" in u: return "Wireshark / DHCP"
        if "arp" in u: return "Wireshark / ARP"
        if "icmp" in u: return "Wireshark / ICMP"
        if "dns" in u: return "Wireshark / DNS"
        if "tcp" in u: return "Wireshark / TCP"
        if "udp" in u: return "Wireshark / UDP"
        if "http" in u: return "Wireshark / HTTP"
        if "ethertype" in u or "ethernet" in u: return "Wireshark / Ethernet"
        if "filter" in u: return "Wireshark / Filters"
        return "Wireshark"

    def difficulty_for_q(n: int) -> str:
        # Practical Wireshark exam: mostly medium; some hard
        if n in (12, 13, 14, 20):
            return "hard"
        if n in (15, 16, 17):
            return "medium"
        return "medium"

    def flush_question():
        nonlocal cur_num, cur_lines, in_bonus, id_start
        if cur_num is None and not in_bonus:
            return
        text = "\n".join(cur_lines).strip()
        if not text:
            return
        if in_bonus:
            out.append({
                "id": id_start,
                "type": "open",
                "difficulty": "hard",
                "topic": "Wireshark / DHCP",
                "question": "⭐ Bonus Question\n" + text,
                "explain": "שאלה מעשית על תהליך DHCP ב-Wireshark."
            })
            id_start += 1
        else:
            out.append({
                "id": id_start,
                "type": "open",
                "difficulty": difficulty_for_q(cur_num),
                "topic": topic_from_text(text),
                "question": f"Question {cur_num}\n{text}",
                "explain": "שאלה מעשית – ענה/י לפי הקובץ NetworkingExam.pcap ב-Wireshark."
            })
            id_start += 1

    for line in lines:
        # detect start
        m = QUESTION_HDR.match(line)
        if m:
            # flush previous
            flush_question()
            cur_num = int(m.group(1))
            cur_lines = []
            in_answer = False
            in_bonus = False
            continue

        if BONUS_HDR.match(line):
            flush_question()
            cur_num = None
            cur_lines = []
            in_answer = False
            in_bonus = True
            continue

        # skip answer blocks
        if line.lower().startswith("answer:") or line.lower().startswith("anwer:"):
            in_answer = True
            continue

        # stop skipping answers when next question/bonus header arrives (handled above)
        if in_answer:
            continue

        # collect question lines only when inside question or bonus
        if cur_num is not None or in_bonus:
            cur_lines.append(line)

    flush_question()
    return out


# -------------------------
# Helpers
# -------------------------
def fmt_time(seconds: int) -> str:
    seconds = max(0, int(seconds))
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def maybe_autorefresh(interval_ms: int, key: str):
    f = getattr(st, "autorefresh", None)
    if callable(f):
        f(interval=interval_ms, key=key)

def map_diff_en_to_he(diff_en: str) -> str:
    return {"easy": "קל", "medium": "בינוני", "hard": "קשה"}.get(diff_en, "—")

def build_question_pool(extra_questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged = list(BASE_QUESTIONS) + list(extra_questions)

    # Ensure unique IDs
    seen = set()
    fixed = []
    next_id = 1
    for q in merged:
        q2 = dict(q)
        if q2.get("id") in seen or q2.get("id") is None:
            while next_id in seen:
                next_id += 1
            q2["id"] = next_id
        seen.add(q2["id"])
        fixed.append(q2)
    return fixed

def grade_question(q, resp):
    if q["type"] == "mcq":
        if resp is None:
            return True, False, "לא נבחרה תשובה."
        ok = (resp == q.get("answer"))
        return True, ok, (q.get("explain") or "")
    return False, None, "שאלה לבדיקה ידנית."

def render_question(q):
    qid = q["id"]
    st.write(q["question"])

    if q["type"] == "mcq":
        choice_keys = list(q["choices"].keys())
        prev = st.session_state.responses.get(qid)
        idx = 0
        if prev in choice_keys:
            idx = choice_keys.index(prev)
        sel = st.radio(
            "בחר תשובה:",
            options=choice_keys,
            index=idx,
            format_func=lambda k: f"{k}) {q['choices'][k]}",
            key=f"mcq_{qid}",
        )
        return sel

    prev = st.session_state.responses.get(qid, "")
    ans = st.text_area("תשובה (פתוח):", value=prev, height=150, key=f"open_{qid}")
    return ans


# -------------------------
# State
# -------------------------
def init_state():
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    # Start menu fields (TEXT INPUTS)
    st.session_state.setdefault("cfg_num_questions_text", "20")
    st.session_state.setdefault("cfg_difficulty", "הכל")
    st.session_state.setdefault("cfg_timer_enabled", False)
    st.session_state.setdefault("cfg_timer_minutes_text", "25")

    # runtime
    st.session_state.setdefault("quiz_set", [])
    st.session_state.setdefault("q_idx", 0)
    st.session_state.setdefault("score", 0)
    st.session_state.setdefault("correct", 0)
    st.session_state.setdefault("wrong", 0)
    st.session_state.setdefault("answered", False)
    st.session_state.setdefault("feedback", None)
    st.session_state.setdefault("started_at", time.time())
    st.session_state.setdefault("end_time", None)
    st.session_state.setdefault("responses", {})

    # whiteboard
    st.session_state.setdefault("board_json", {"version": "4.4.0", "objects": []})
    st.session_state.setdefault("canvas_key", 0)

    # 3 color presets (RGB)
    st.session_state.setdefault("c1", "#000000")
    st.session_state.setdefault("c2", "#ff0000")
    st.session_state.setdefault("c3", "#0000ff")

def clear_board():
    st.session_state.board_json = {"version": "4.4.0", "objects": []}
    st.session_state.canvas_key += 1

def reset_to_menu():
    st.session_state.quiz_started = False
    st.session_state.quiz_set = []
    st.session_state.q_idx = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.responses = {}
    st.session_state.started_at = time.time()
    st.session_state.end_time = None

def start_quiz(question_pool: List[Dict[str, Any]]):
    # filter difficulty
    diff_map = {"קל": "easy", "בינוני": "medium", "קשה": "hard", "הכל": None}
    selected = diff_map.get(st.session_state.cfg_difficulty, None)
    pool = question_pool if not selected else [q for q in question_pool if q.get("difficulty") == selected]

    # parse num questions (text)
    try:
        n = int(st.session_state.cfg_num_questions_text.strip())
    except Exception:
        n = 10

    n = max(1, min(n, len(pool), 64))

    quiz_set = random.sample(pool, n)
    random.shuffle(quiz_set)

    st.session_state.quiz_set = quiz_set
    st.session_state.q_idx = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.responses = {}
    st.session_state.started_at = time.time()

    if st.session_state.cfg_timer_enabled:
        try:
            minutes = int(st.session_state.cfg_timer_minutes_text.strip())
        except Exception:
            minutes = 20
        minutes = max(1, min(minutes, 240))
        st.session_state.end_time = time.time() + minutes * 60
    else:
        st.session_state.end_time = None

    st.session_state.quiz_started = True


# -------------------------
# Load DOCX questions automatically (your uploaded file path)
# -------------------------
DOCX_PATH = r"/mnt/data/Networking Exam A.docx"
DOCX_QUESTIONS: List[Dict[str, Any]] = []
try:
    DOCX_QUESTIONS = parse_networking_exam_a_docx(DOCX_PATH, id_start=2000)
except Exception:
    DOCX_QUESTIONS = []

QUESTION_POOL = build_question_pool(DOCX_QUESTIONS)


# -------------------------
# APP
# -------------------------
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown(
    """
    <style>
      html, body, [class*="css"] { direction: rtl; text-align: right; }
      .block-container { padding-top: 1.0rem; max-width: 1700px; }
      section[data-testid="stSidebar"] { padding-top: 0.8rem; }
      .stRadio label { font-size: 0.98rem; }
    </style>
    """,
    unsafe_allow_html=True
)

init_state()

# -------------------------
# START MENU
# -------------------------
if not st.session_state.quiz_started:
    st.title(APP_TITLE)
    st.caption(f"מאגר נוכחי: {len(QUESTION_POOL)} שאלות | מקסימום במבחן: 64 | נוספו מה-DOCX: {len(DOCX_QUESTIONS)}")

    st.subheader("⚙️ מסך כניסה – הגדרות מבחן")

    c1, c2, c3 = st.columns([1.0, 1.0, 1.2], gap="large")
    with c1:
        st.markdown("**כמות שאלות (1–64):**")
        st.session_state.cfg_num_questions_text = st.text_input(
            "כמות שאלות", value=st.session_state.cfg_num_questions_text,
            label_visibility="collapsed", placeholder="למשל 20"
        )

    with c2:
        st.markdown("**רמת קושי:**")
        st.session_state.cfg_difficulty = st.selectbox(
            "רמת קושי", ["קל", "בינוני", "קשה", "הכל"],
            index=["קל", "בינוני", "קשה", "הכל"].index(st.session_state.cfg_difficulty),
            label_visibility="collapsed",
        )

    with c3:
        st.markdown("**טיימר:**")
        st.session_state.cfg_timer_enabled = st.toggle("להפעיל טיימר", value=st.session_state.cfg_timer_enabled)

    if st.session_state.cfg_timer_enabled:
        st.markdown("**כמה דקות?**")
        st.session_state.cfg_timer_minutes_text = st.text_input(
            "דקות טיימר", value=st.session_state.cfg_timer_minutes_text,
            label_visibility="collapsed", placeholder="למשל 30"
        )

    # validation / info
    diff_map = {"קל": "easy", "בינוני": "medium", "קשה": "hard", "הכל": None}
    selected = diff_map.get(st.session_state.cfg_difficulty, None)
    pool_filtered = QUESTION_POOL if not selected else [q for q in QUESTION_POOL if q.get("difficulty") == selected]

    try:
        n_req = int(st.session_state.cfg_num_questions_text.strip())
    except Exception:
        n_req = 0

    ok_num = 1 <= n_req <= 64
    ok_available = (n_req <= len(pool_filtered)) if ok_num else False

    if not ok_num:
        st.warning("כמות שאלות חייבת להיות מספר בין 1 ל-64.")
    elif not ok_available:
        st.warning(f"בקושי שבחרת יש רק {len(pool_filtered)} שאלות. תקטין כמות או בחר 'הכל'.")
    else:
        st.info(f"יצאו למבחן: {n_req} שאלות (מתוך {len(pool_filtered)} זמינות בקושי שנבחר).")

    if st.session_state.cfg_timer_enabled:
        try:
            mins = int(st.session_state.cfg_timer_minutes_text.strip())
        except Exception:
            mins = 0
        if mins < 1:
            st.warning("דקות טיימר חייב להיות מספר חיובי (למשל 20).")

    st.divider()
    if st.button("🚀 התחל מבחן", use_container_width=True, disabled=not (ok_num and ok_available)):
        start_quiz(QUESTION_POOL)
        st.rerun()

    st.stop()


# -------------------------
# SIDEBAR (LEFT)
# -------------------------
with st.sidebar:
    st.title("תפריט")
    total = len(st.session_state.quiz_set)
    elapsed = int(time.time() - st.session_state.started_at)

    st.subheader("📊 ניקוד")
    st.metric("Score", f"{st.session_state.score} / {total}")
    st.write(f"✅ Correct: **{st.session_state.correct}**")
    st.write(f"❌ Wrong: **{st.session_state.wrong}**")
    st.write(f"⏱️ Elapsed: **{fmt_time(elapsed)}**")

    if st.session_state.end_time is not None:
        remaining = int(st.session_state.end_time - time.time())
        st.write(f"⏳ Left: **{fmt_time(remaining)}**")
        maybe_autorefresh(1000, key="timer_refresh")

    st.divider()
    if st.button("🔙 חזרה למסך כניסה", use_container_width=True):
        reset_to_menu()
        st.rerun()

    if st.button("🧽 Clear Whiteboard", use_container_width=True):
        clear_board()
        st.rerun()


# -------------------------
# TIMER ENFORCEMENT
# -------------------------
if st.session_state.end_time is not None and time.time() >= st.session_state.end_time:
    st.error("⏰ הזמן נגמר! המבחן נסגר.")
    total = len(st.session_state.quiz_set)
    st.write(f"ציון: **{st.session_state.score} / {total}**")
    st.write(f"נכון: **{st.session_state.correct}** | לא נכון: **{st.session_state.wrong}**")
    if st.button("🔙 חזרה למסך כניסה", use_container_width=True):
        reset_to_menu()
        st.rerun()
    st.stop()


# -------------------------
# MAIN LAYOUT: Quiz left, Whiteboard right
# -------------------------
quiz_col, board_col = st.columns([1.35, 1.0], gap="large")


# -------------------------
# QUIZ
# -------------------------
with quiz_col:
    st.subheader("🧠 מבחן")

    total = len(st.session_state.quiz_set)
    if st.session_state.q_idx >= total:
        st.success("סיימת! 🎉")
        st.write(f"ציון: **{st.session_state.score} / {total}**")
        st.write(f"נכון: **{st.session_state.correct}** | לא נכון: **{st.session_state.wrong}**")
        if st.button("🔙 חזרה למסך כניסה", use_container_width=True):
            reset_to_menu()
            st.rerun()
    else:
        q = st.session_state.quiz_set[st.session_state.q_idx]
        st.write(
            f"**שאלה {st.session_state.q_idx + 1} מתוך {total}** | "
            f"נושא: **{q.get('topic','—')}** | "
            f"קושי: **{map_diff_en_to_he(q.get('difficulty','medium'))}**"
        )
        st.progress((st.session_state.q_idx + 1) / total)

        st.markdown("---")
        resp = render_question(q)
        st.session_state.responses[q["id"]] = resp

        b1, b2, b3 = st.columns([1.0, 1.0, 1.6])

        with b1:
            if st.button("בדוק", use_container_width=True, disabled=st.session_state.answered):
                graded, ok, explain = grade_question(q, resp)
                st.session_state.answered = True

                if graded:
                    if ok:
                        st.session_state.score += 1
                        st.session_state.correct += 1
                        st.session_state.feedback = ("✅ נכון!", "success", explain)
                    else:
                        st.session_state.wrong += 1
                        correct = q.get("answer")
                        if correct:
                            st.session_state.feedback = (f"❌ לא נכון. תשובה נכונה: **{correct}**", "error", explain)
                        else:
                            st.session_state.feedback = ("❌ לא נכון.", "error", explain)
                else:
                    st.session_state.feedback = ("📝 שאלה לבדיקה ידנית (נשמרה התשובה).", "info", explain)

                st.rerun()

        with b2:
            if st.button("הסבר", use_container_width=True):
                if q.get("explain"):
                    st.info(q["explain"])
                else:
                    st.info("אין הסבר זמין לשאלה הזו.")

        with b3:
            if st.button("הבא ➜", use_container_width=True, disabled=not st.session_state.answered):
                st.session_state.q_idx += 1
                st.session_state.answered = False
                st.session_state.feedback = None
                st.rerun()

        if st.session_state.feedback:
            msg, kind, expl = st.session_state.feedback
            getattr(st, kind)(msg)
            if expl:
                st.info(expl)


# -------------------------
# WHITEBOARD (RIGHT)
# -------------------------
with board_col:
    st.subheader("🧾 Whiteboard")

    # שורה 1: כלים קומפקטיים (בלי nesting)
    wb1, wb2, wb3 = st.columns([1.2, 0.9, 1.0], gap="small")
    with wb1:
        mode = st.selectbox("Tool", ["freedraw", "line", "rect", "circle", "transform"], label_visibility="collapsed")
    with wb2:
        stroke_width = st.slider("Stroke", 1, 28, 5, label_visibility="collapsed")
    with wb3:
        pick = st.selectbox("Color", ["C1", "C2", "C3"], label_visibility="collapsed")

    # שורה 2: 3 צבעים (באותה רמה, לא בתוך עמודה אחרת)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.session_state.c1 = st.color_picker("C1", st.session_state.c1)
    with c2:
        st.session_state.c2 = st.color_picker("C2", st.session_state.c2)
    with c3:
        st.session_state.c3 = st.color_picker("C3", st.session_state.c3)

    active_color = {"C1": st.session_state.c1, "C2": st.session_state.c2, "C3": st.session_state.c3}[pick]

    a1, a2 = st.columns([1, 1], gap="small")
    with a1:
        if st.button("🧽 Clear", use_container_width=True):
            clear_board()
            st.rerun()
    with a2:
        st.caption("בחר/י **transform** להזזה/שינוי גודל של צורות.")

    result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=active_color,
        background_color="#ffffff",
        height=BOARD_H,
        width=BOARD_W,
        drawing_mode=mode,
        initial_drawing=st.session_state.board_json,
        key=f"canvas_{st.session_state.canvas_key}",
        display_toolbar=True,
        update_streamlit=False,  # prevents blinking
    )

    if result is not None and result.json_data is not None:
        st.session_state.board_json = result.json_data
