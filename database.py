# ============================================================
# database.py — SQLite Database Setup and CRUD Functions
# Project: 2026 Iran War NLP News Dataset
# ============================================================
# This file handles:
# 1. Creating the SQLite database and table
# 2. All CRUD operations (Create, Read, Update, Delete)
# 3. Seeding initial data from the CSV dataset
# ============================================================

import sqlite3

# Database file name — SQLite stores everything in one file
DB_FILE = "war_news.db"


# ============================================================
# INIT — Create database and table
# ============================================================
def init_db():
    """
    Creates the database file and the news_events table.
    Runs only once when the server starts.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_events (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            date                TEXT NOT NULL,
            headline            TEXT NOT NULL,
            news_text           TEXT NOT NULL,
            source              TEXT NOT NULL,
            location            TEXT NOT NULL,
            casualties_reported TEXT DEFAULT 'Unknown',
            event_type          TEXT NOT NULL,
            sentiment           TEXT DEFAULT 'Negative'
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


# ============================================================
# HELPER — Convert a database row to a dictionary
# ============================================================
def row_to_dict(row):
    """
    Converts a database row (tuple) into a Python dictionary.
    This makes it easy to convert to JSON later.
    """
    return {
        "id":                  row[0],
        "date":                row[1],
        "headline":            row[2],
        "news_text":           row[3],
        "source":              row[4],
        "location":            row[5],
        "casualties_reported": row[6],
        "event_type":          row[7],
        "sentiment":           row[8]
    }


# ============================================================
# READ — Get all news events
# ============================================================
def get_all_news():
    """
    Returns all news events from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_events ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


# ============================================================
# READ ONE — Get a single news event by ID
# ============================================================
def get_news_by_id(news_id):
    """
    Returns one news event by its ID.
    Returns None if not found.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_events WHERE id = ?", (news_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_dict(row)
    return None


# ============================================================
# CREATE — Add a new news event
# ============================================================
def add_news(date, headline, news_text, source, location, casualties_reported, event_type, sentiment):
    """
    Inserts a new news event into the database.
    Returns the ID of the newly created record.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO news_events (date, headline, news_text, source, location, casualties_reported, event_type, sentiment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, headline, news_text, source, location, casualties_reported, event_type, sentiment))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


# ============================================================
# UPDATE — Edit an existing news event
# ============================================================
def update_news(news_id, date, headline, news_text, source, location, casualties_reported, event_type, sentiment):
    """
    Updates an existing news event in the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE news_events
        SET date = ?, headline = ?, news_text = ?, source = ?, location = ?,
            casualties_reported = ?, event_type = ?, sentiment = ?
        WHERE id = ?
    """, (date, headline, news_text, source, location, casualties_reported, event_type, sentiment, news_id))
    conn.commit()
    conn.close()


# ============================================================
# DELETE — Remove a news event
# ============================================================
def delete_news(news_id):
    """
    Deletes a news event from the database by ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news_events WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()


# ============================================================
# SEED — Add initial data if database is empty
# ============================================================
def seed_data():
    """
    Adds the initial 51 war news events to the database.
    Only runs if the database is empty.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM news_events")
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        print(f"✅ Database already has {count} records. Skipping seed.")
        return

    # Initial dataset — 51 war news events
    initial_data = [
        ("2/28/2026", "US and Israel launch surprise strikes on Iran", "The United States and Israel launched surprise airstrikes on multiple sites and cities across Iran killing Supreme Leader Ali Khamenei and several other Iranian officials. The Israeli Air Force struck 500 military targets using about 200 fighter jets in the largest combat sortie in its history.", "Al Jazeera", "Iran", "Unknown", "Airstrike", "Negative"),
        ("3/1/2026", "Iran announces death of Supreme Leader Khamenei", "Iranian state media announced that Supreme Leader Ali Khamenei had been killed in the US-Israeli strikes. Iran vowed to retaliate with full force against Israel and US military bases in the region.", "Al Jazeera", "Iran", "High", "Political", "Negative"),
        ("3/2/2026", "Iran launches drone and missile strikes on Israel", "Iran retaliated by launching hundreds of drones and ballistic missiles at targets in Israel and at US military bases in Bahrain Jordan Kuwait Qatar Saudi Arabia Turkey and the United Arab Emirates.", "Al Jazeera", "Israel", "Multiple injured", "Missile Strike", "Negative"),
        ("3/3/2026", "Strait of Hormuz threatened as war escalates", "Iran threatened to close the Strait of Hormuz indefinitely as the war between the US Israel and Iran escalated. Oil prices surged globally as fears of supply disruption grew.", "CNN", "Strait of Hormuz", "None reported", "Economic", "Negative"),
        ("3/4/2026", "Iran fires over 500 ballistic missiles since war began", "A military source told Fars News Agency that Iran had fired over 500 ballistic and naval missiles and almost 2000 drones since February 28. Almost 40 percent were aimed at Israel and 60 percent at US targets.", "Al Jazeera", "Iran", "Unknown", "Missile Strike", "Negative"),
        ("3/5/2026", "US drops 5000 pound bombs on Iranian coastal facility", "Admiral Brad Cooper commander of US Central Command said the US military dropped multiple 5000 pound bombs on an underground facility along Iran's coast used to store antiship cruise missiles and mobile missile launchers.", "CNN", "Iran Coast", "Unknown", "Airstrike", "Negative"),
        ("3/6/2026", "Hezbollah fires rockets at Israeli soldiers in Lebanon", "Hezbollah said it fired a barrage of rockets at Israeli soldiers patrolling in southern Lebanon. Two Israeli reservists were wounded in a Hezbollah mortar attack in northern Israel.", "Al Jazeera", "Lebanon", "2 injured", "Rocket Attack", "Negative"),
        ("3/7/2026", "Iran attacks US bases across Iraq and Middle East", "The Islamic Resistance in Iraq said it carried out 21 attacks against US bases across the country and the region. Three drones were intercepted near Erbil airport resulting in a fire in the vicinity.", "Al Jazeera", "Iraq", "4 injured", "Drone Attack", "Negative"),
        ("3/8/2026", "Global oil prices surge amid Middle East war", "Oil prices surged globally with Brent crude hitting over 100 dollars per barrel as the ongoing conflict in the Middle East disrupted shipping through the Strait of Hormuz and threatened regional energy supplies.", "CNN", "Global", "None", "Economic", "Negative"),
        ("3/9/2026", "UK France Germany condemn Iranian attacks on ships", "The UAE Bahrain the United Kingdom France and Germany issued a joint statement condemning what they described as Iran attacks on commercial vessels and civilian infrastructure in the Gulf region.", "Al Jazeera", "Gulf Region", "None", "Diplomatic", "Negative"),
        ("3/10/2026", "Iran shoots down Israeli fighter jet in its airspace", "The Islamic Revolutionary Guard Corps claimed its air defences shot down an Israeli fighter in Iranian airspace the third such incident reported during the war. Israel did not confirm this report.", "Al Jazeera", "Iran", "Unknown", "Air Defense", "Negative"),
        ("3/11/2026", "US F-35 makes emergency landing after Iran mission", "A US F-35 fighter jet made an emergency landing at a Middle East airbase after a combat mission over Iran. The aircraft landed safely and the pilot is stable while officials investigate if it was struck by Iranian fire.", "Al Jazeera", "Middle East", "Pilot safe", "Air Incident", "Negative"),
        ("3/12/2026", "Iran strikes Natanz nuclear site attacked by Israel", "Iran Atomic Energy Organisation said Israel and the US targeted the country Natanz nuclear site in criminal attacks. Tehran informed the International Atomic Energy Agency which confirmed no unusual radiation leak.", "Al Jazeera", "Iran", "None reported", "Nuclear Site Attack", "Negative"),
        ("3/13/2026", "Netanyahu says Iran decimated as war continues", "Israeli Prime Minister Benjamin Netanyahu said he saw this war ending a lot faster than people think. We are winning and Iran is being decimated. Netanyahu reiterated goals of dismantling Iran nuclear programme.", "Al Jazeera", "Israel", "None", "Political", "Negative"),
        ("3/14/2026", "3000 to 4000 Iranian soldiers killed since war began", "The Israeli military estimated that between 3000 and 4000 Iranian soldiers and commanders had been killed since the war began on February 28. Iran disputed these numbers.", "Al Jazeera", "Iran", "3000-4000 soldiers", "Military", "Negative"),
        ("3/15/2026", "Iran warns zero restraint if energy facilities attacked", "Iran warned it will show zero restraint if its energy facilities are attacked again a day after Israel struck the South Pars gasfield and Tehran attacked energy sites across the Gulf.", "Al Jazeera", "Iran", "None", "Political", "Negative"),
        ("3/16/2026", "Israel strikes South Pars gasfield in Iran", "Israel struck Iran South Pars gasfield one of the most important energy facilities in the Middle East. Tehran responded by hitting targets in Haifa Israel and Ras Laffan Qatar.", "Al Jazeera", "Iran", "Unknown", "Airstrike", "Negative"),
        ("3/17/2026", "Iran kills thousands of protesters before war began", "In January 2026 Iranian security forces killed thousands of protesters during the largest protests since the Iranian Revolution. US President Trump responded by threatening military action against Iran.", "Wikipedia", "Iran", "Thousands", "Civil Unrest", "Negative"),
        ("3/18/2026", "Ali Larijani assassinated by Israel", "Israel assassinated Ali Larijani secretary of Iran Supreme National Security Council in a targeted strike. This was one of several high profile assassinations carried out since the war began.", "Al Jazeera", "Iran", "1 killed", "Assassination", "Negative"),
        ("3/19/2026", "UN warns 3 million Iranians displaced by attacks", "The United Nations warned that 3 million Iranians have been displaced by Israeli and US attacks since the war began on February 28. The humanitarian crisis continues to worsen as attacks on civilian areas intensify.", "Al Jazeera", "Iran", "3 million displaced", "Humanitarian", "Negative"),
        ("3/19/2026", "Kuwait refinery hit by Iranian drones", "Two waves of Iranian drones hit Kuwait Mina al-Ahmadi refinery early Friday sparking a fire at one of the Middle East largest facilities capable of processing approximately 730000 barrels of oil per day.", "Al Jazeera", "Kuwait", "None reported", "Drone Attack", "Negative"),
        ("3/20/2026", "Trump threatens to obliterate Iran power plants", "US President Donald Trump threatened to obliterate Iran power plants if Tehran does not fully reopen the Strait of Hormuz within two days. Iran military declared it is ready to close the Strait indefinitely in response.", "CNN", "USA", "None", "Political", "Negative"),
        ("3/20/2026", "Gas prices hit nearly 4 dollars per gallon in USA", "Gas prices soared to an average of 3.94 dollars nationwide as of Friday up 96 cents from February 28 when the US-Israeli conflict with Iran began. Analysts warned prices may hit 4 dollars per gallon soon.", "CNN", "USA", "None", "Economic", "Negative"),
        ("3/21/2026", "Iranian missiles strike near Israel Dimona nuclear facility", "Iranian missile attacks broke through Israeli defences making direct impacts in the cities of Dimona and Arad near Israel main nuclear facility wounding some 100 people. Netanyahu called it a very difficult evening.", "Al Jazeera", "Israel", "180 injured", "Missile Strike", "Negative"),
        ("3/21/2026", "Israel strikes research facility at Tehran university", "The Israeli military announced it struck a research and development facility at Tehran Malek Ashtar University which it said had been used to develop components for nuclear weapons and ballistic missiles.", "Al Jazeera", "Iran", "Unknown", "Airstrike", "Negative"),
        ("3/22/2026", "Iran death toll tops 1500 including 200 children", "Iranian state media reported that the death toll from US-Israeli attacks topped 1500 including at least 200 children and at least 20984 people were injured with seven hospitals evacuated and 36 ambulances damaged.", "Al Jazeera", "Iran", "1500 killed", "Humanitarian", "Negative"),
        ("3/22/2026", "Brent crude hits 114 dollars as Hormuz threatened", "Oil prices rose after Iran threatened to shut down the Strait of Hormuz indefinitely. Brent crude the global benchmark climbed to about 114 dollars a barrel. Goldman Sachs said elevated prices could persist through 2027.", "CNN", "Global", "None", "Economic", "Negative"),
        ("3/22/2026", "Iran President calls on BRICS to halt aggression", "Iran President Masoud Pezeshkian called on the BRICS alliance currently chaired by India to play an independent role in halting aggressions against Iran. He also proposed a regional security framework.", "Al Jazeera", "Iran", "None", "Diplomatic", "Negative"),
        ("3/22/2026", "Israel 4292 people hospitalized since war began", "Israel Ministry of Health said at least 4292 injured people have been brought to hospitals since the start of the war between the US Israel and Iran that began on February 28 2026.", "Al Jazeera", "Israel", "4292 hospitalized", "Humanitarian", "Negative"),
        ("3/23/2026", "Trump says US weeks ahead of schedule in Iran war", "Trump claimed that the US is weeks ahead of schedule in its war on Iran and reiterated that Washington is not looking to make a deal with Iran because their leadership is gone their navy and air force are dead.", "CNN", "USA", "None", "Political", "Negative"),
        ("3/4/2026", "US submarine torpedoes Iranian warship in Indian Ocean", "US Navy submarine USS Charlotte torpedoed Iranian frigate IRIS Dena in the Indian Ocean killing 104 Iranian sailors. This was the first ship sunk by a submarine in active combat since the Falklands War.", "Reuters", "Indian Ocean", "104 killed", "Naval Attack", "Negative"),
        ("3/3/2026", "Israel launches ground invasion of Lebanon", "Israel authorized a ground invasion of Lebanon to establish a security layer against Hezbollah along the border. IDF forces from the 91st Division entered southern Lebanon targeting Hezbollah infrastructure.", "Reuters", "Lebanon", "Unknown", "Ground Invasion", "Negative"),
        ("3/8/2026", "Mojtaba Khamenei elected as new Supreme Leader", "Mojtaba Khamenei son of the assassinated Supreme Leader Ali Khamenei was elected as Iran new supreme leader on March 8. The IRGC and top Iranian leaders pledged allegiance to him.", "Al Jazeera", "Iran", "None", "Political", "Negative"),
        ("3/4/2026", "Qatar shoots down two Iranian Su-24 bombers", "Qatar shot down two Iranian Su-24 bombers making it the first nation to shoot down an Iranian aircraft in the conflict. Qatar also arrested ten individuals for operating as an IRGC cell collecting data on military infrastructure.", "CNN", "Qatar", "None", "Air Defense", "Negative"),
        ("3/5/2026", "Amazon data centers in UAE damaged by Iranian drones", "Three Amazon Web Services data centers in the United Arab Emirates were struck and damaged by drone strikes leading to major outages of web infrastructure including S3 storage EC2 compute and DynamoDB databases.", "404 Media", "UAE", "None", "Cyber Attack", "Negative"),
        ("3/2/2026", "Golestan Palace UNESCO heritage site damaged in Tehran", "A strike on Arg Square damaged nearby Golestan Palace a UNESCO World Heritage Site prompting UNESCO to issue a statement that damaging UNESCO property is against international law.", "UNESCO", "Iran", "None", "Cultural Damage", "Negative"),
        ("3/11/2026", "Six US airmen killed in KC-135 crash in Iraq", "Six American military airmen were killed when their KC-135 aerial refueling aircraft crashed in western Iraq while supporting US military operations. CENTCOM said the crash was not the result of hostile action.", "CENTCOM", "Iraq", "6 killed", "Military Accident", "Negative"),
        ("3/8/2026", "Tehran fuel depots bombed causing toxic black rain", "Israeli strikes hit oil storage facilities near Tehran causing a river of fire to pour through surrounding streets. The city became engulfed in thick black smoke causing toxic acidic black rain to fall in the area.", "Al Jazeera", "Iran", "4 killed", "Airstrike", "Negative"),
        ("3/13/2026", "Iran targets Gulf nations with missiles and drones as oil rises", "Iran again targeted Gulf countries with missiles and drones causing oil prices to rise. Bahrain reported attacks on fuel tanks. Two people were injured when a hostile drone struck a residential building in Kuwait.", "Al Jazeera", "Gulf Region", "Multiple injured", "Missile Strike", "Negative"),
        ("3/14/2026", "US bombs Kharg Island Iran oil export hub", "The US conducted a large-scale bombing raid on Kharg Island home to 90 percent of Iran oil exports. Over 90 military sites were targeted while the oil infrastructure was not targeted according to Trump.", "Reuters", "Iran", "Unknown", "Airstrike", "Negative"),
        ("3/17/2026", "Israel launches ground invasion of southern Lebanon", "Israel launched a ground invasion of southern Lebanon with forces crossing the border in a major escalation of the conflict. Lebanese civilians began fleeing as Israeli tanks and troops advanced.", "Al Jazeera", "Lebanon", "Unknown", "Ground Invasion", "Negative"),
        ("3/18/2026", "Israel kills Iran intelligence chief Esmaeil Khatib", "Israel said it killed Iranian intelligence minister Esmaeil Khatib in an overnight airstrike. Iranian President Pezeshkian confirmed Khatib killing making him one of the most senior officials killed in the war.", "NPR", "Iran", "1 killed", "Assassination", "Negative"),
        ("3/21/2026", "Iran fires ballistic missiles at Diego Garcia US-UK base", "Iran attempted to strike the joint US-UK military base at Diego Garcia on the Chagos Islands using ballistic missiles. One missile broke apart mid-flight and another was intercepted by a US warship.", "BBC", "Indian Ocean", "None", "Missile Strike", "Negative"),
        ("3/23/2026", "Iran threatens to mine all communication lines in Persian Gulf", "Iran National Defence Council warned that any attempt to attack the Iranian coast or islands will cause all communication lines in the Persian Gulf to be mined as Trump 48 hour deadline expires.", "Al Jazeera", "Persian Gulf", "None", "Political", "Negative"),
        ("3/9/2026", "Iran internet blackout enters day 11 most severe ever", "A nationwide internet blackout imposed by Iranian authorities entered day 11 passing the 240 hour mark making it one of the most severe internet shutdowns ever registered in any country according to NetBlocks.", "NetBlocks", "Iran", "None", "Cyber Warfare", "Negative"),
        ("3/12/2026", "USS Gerald R Ford aircraft carrier damaged by fire", "The USS Gerald R Ford the largest aircraft carrier in the theatre was damaged by a fire that broke out in a laundry area injuring multiple sailors. The fire was not combat related but the carrier later withdrew for repairs.", "US Navy", "Middle East", "Multiple injured", "Military Incident", "Negative"),
        ("3/21/2026", "Russia condemns strikes on Natanz as violation of international law", "Russia condemned the US-Israeli strikes on Natanz as a blatant violation of international law while the IAEA urged military restraint to avoid any risk of a nuclear accident after bunker buster bombs were used.", "Reuters", "Iran", "None", "Diplomatic", "Negative"),
        ("3/16/2026", "NATO allies reject Trump call to help reopen Strait of Hormuz", "US aligned NATO nations in Europe rejected Trump call to provide military support to reopen the Strait of Hormuz. Trump rebuked his NATO allies calling their decision a very foolish mistake.", "NBC News", "Europe", "None", "Diplomatic", "Negative"),
        ("3/13/2026", "US temporarily lifts restrictions on Russian oil sales", "To help deal with the economic costs of the war the US temporarily lifted restrictions on the sale of Russian oil. However oil prices were barely affected by this measure as the Hormuz closure dominated global markets.", "Reuters", "Global", "None", "Economic", "Negative"),
        ("3/5/2026", "Azerbaijan reports Iranian drone strikes on Nakhchivan airport", "The government of Azerbaijan said two drones from Iran struck its Nakhchivan exclave damaging an airport and injuring two civilians. Azerbaijan described the attacks as Iranian terrorist activity.", "Reuters", "Azerbaijan", "2 injured", "Drone Attack", "Negative"),
        ("3/10/2026", "UNICEF reports over 1100 children killed or injured in war", "UNICEF reported that more than 1100 children were injured or killed in the war with 200 reportedly killed in Iran 91 in Lebanon 4 in Israel and 1 in Kuwait. Hundreds of thousands were also displaced.", "UNICEF", "Middle East", "1100 children", "Humanitarian", "Negative"),
    ]

    for row in initial_data:
        add_news(*row)

    print(f"✅ Seeded {len(initial_data)} news events into database!")
