#!/usr/bin/env python3
# ai.py
# FHA GPT v1.0 - The Ultimate Mini-ChatGPT (Hausa Edition)
# - 800+ Semantic Relations.
# - 200+ Intent Keywords.
# - Question Evaluation (Mai Kyau/Mai Sauki).
# - Advice with Reasoning (Hujja).
# - Strict Word Limit (20 Words).

from flask import Flask, request, jsonify
from flask_cors import CORS
import re, random, math, os
from collections import Counter, defaultdict

app = Flask(__name__)
CORS(app)

BRAIN_FILE = "brain.txt"

# ==============================================================================
# 1. SEMANTIC DICTIONARY (800+ RELATIONS - THE KNOWLEDGE GRAPH)
# ==============================================================================
RELATIONS = {
    # --- SUFURI & MOTOCI ---
    "mota": ["abin hawa", "sufuri", "tuki", "injin", "fetur", "taya", "gareji", "direba", "hanya", "kwalta", "motoci", "bas", "taksi", "tanki", "birki", "stiyari", "gudu", "kaura", "tifa", "trela", "honda", "toyota", "benz", "ford", "kabukan", "nono", "mai", "gyara", "mekanike", "faka", "fakin", "key", "sitari", "bonet", "but", "lamba"],
    "keke": ["pedal", "sarka", "motsa jiki", "napep", "adaidaita", "keke", "taya biyu", "keken dinki", "babur", "okada", "achaba", "boxer", "jincheng", "hawa", "gudu", "shiga"],
    "jirgi": ["sama", "filin jirgi", "fuka-fuki", "tashi", "sauka", "pailot", "jirgin sama", "jirgin ruwa", "jirgin kasa", "tashar jirgi", "tikiti", "fasinja", "helikofta", "jet", "cargo", "muhun", "airport", "visa", "passport"],
    
    # --- KUDI & KASUWANCI ---
    "kudi": ["banki", "arziki", "kasuwa", "ciniki", "naira", "dala", "riba", "albashi", "bashi", "rance", "asusu", "pos", "transfer", "caji", "saye", "sayarwa", "j jari", "dukiya", "kudin shiga", "kasafin kudi", "canji", "dubai", "saudi", "fam", "yuro", "crypto", "bitcoin", "wallets", "alert"],
    "kasuwa": ["shago", "duka", "kantin", "baje koli", "farashi", "tsada", "araha", "cinko", "dilalai", "masu saye", "siyayya", "buhun", "awo", "mudu", "tiya", "kwano", "kasuwar kurmi", "kasuwar kwanar", "supermarket", "mall"],
    
    # --- RAYUWA & HALAYE ---
    "soyayya": ["aure", "masoyi", "kauna", "zuciya", "bege", "kishi", "anganci", "amarya", "saduwa", "fura", "tare", "zama", "rayuwa", "dadi", "budurwa", "saurayi", "kawa", "aboki", "rabin rai", "hasiya", "zuciyata", "masoyiya", "my love", "gwanata"],
    "hakuri": ["juriya", "dangana", "natsuwa", "sannu", "lallashi", "tawakkali", "karfin hali", "hakuri", "dauke kai", "kawasarwa", "shiru", "bari", "bacci", "addu'a"],
    "gaskiya": ["amana", "alkawari", "adalci", "yarda", "aminci", "tabbas", "hakika", "tsakani da Allah", "gaskiya", "ba karya", "gaskiya dokin karfe", "yarda", "tabbatarwa", "tsakani"],
    
    # --- ILIMI & KARATU ---
    "karatu": ["ilimi", "makaranta", "malami", "dalibi", "littafi", "alkalami", "jaro", "allo", "boko", "islamiyya", "jami'a", "digiri", "karatun", "bincike", "karatu", "rubutu", "had da", "tilawa", "nahawu", "sarfu", "luga", "adabi"],
    "rubutu": ["takarda", "haruffa", "kalmomi", "jumla", "waka", "zube", "labari", "tsari", "kuskure", "gyara", "marubuci", "biro", "fensir", "typewriter", "bugawa", "sako", "wasiqa"],
    
    # --- ABINCI & GIRKI ---
    "abinci": ["tuwo", "shinkafa", "yunwa", "ci", "kosai", "miya", "nama", "kifi", "koshi", "girki", "dafawa", "soyawa", "gasa", "abinci", "dan wake", "dambu", "alkubus", "fate", "brabusko", "taliya", "makaranta", "indomie", "spaghetti", "couscous"],
    "kayan miya": ["tumatir", "albasa", "tarugu", "tattasai", "maggi", "gishiri", "man ja", "man gyada", "curry", "thyme", "daddawa", "citta", "kaninfari", "masoro", "tafarnuwa", "yaji"],
    
    # --- GIDA & GINE-GINE ---
    "gida": ["daki", "iyali", "gini", "siminti", "kofa", "falo", "bandaki", "katanga", "soro", "rumfa", "tabarma", "gado", "kujera", "filin gida", "haya", "laka", "kwano", "ruf", "windo", "taga", "fan", "ac"],
    
    # --- FASAHA ---
    "waya": ["kira", "sako", "android", "iphone", "caji", "data", "kati", "network", "sim", "whatsapp", "facebook", "tiktok", "instagram", "twitter", "x", "telegram", "kira", "text", "message", "chat"],
    "kwamfuta": ["na'ura", "internet", "bugun", "allo", "maɓalli", "mouse", "laptop", "desktop", "software", "hardware", "coding", "programming", "python", "java", "html", "website", "ai", "gpt", "robot"],
    
    # --- LAFIYA ---
    "lafiya": ["asibiti", "magani", "likita", "jiki", "karfi", "allura", "ciwo", "zazzabi", "nas", "tiyata", "gwaji", "lab", "kwaya", "syrup", "drip", "bandej", "malaria", "typhoid", "sanyi", "mura", "ciwon kai"],
    
    # --- HALITTU & YANAYI ---
    "ruwa": ["kogi", "teku", "rijiya", "shaka", "wanka", "tsafta", "damina", "ruwan sama", "balar", "tap", "pampo", "pure water", "sachet", "kwalaba", "rijiyar burtsatse", "igi", "rafi"],
    "iska": ["numfashi", "rayuwa", "guguwa", "freshener", "sanyi", "busawa", "shaqa", "iska mai karfi", "fan", "ac", "oxygen", "carbon", "shuka", "iska mai dadi"],
    "kasa": ["noma", "tsirrai", "gona", "birni", "kauye", "jiha", "duniya", "turbaya", "yashi", "tsakuwa", "dutse", "yumbu", "taki", "filin", "Nigeria", "Arewa", "Kudu", "Yamma", "Gabas"],
    
    # --- DANGIN MATA DA DAWA ---
    "dabba": ["zaki", "giwa", "kura", "kare", "mage", "doki", "rakumi", "maciji", "kunama", "kada", "kurege", "zomo", "barewa", "dabbobi", "namun daji", "kada", "damisa", "bauna"],
    
    # --- ADDINI ---
    "addini": ["sallah", "azumi", "zakka", "hajji", "masallaci", "coci", "addu'a", "ibada", "imani", "sadaka", "liman", "fasto", "alkur'ani", "bible", "hadisi", "tauhidi", "fiqhu"],
    
    # --- SIYASA ---
    "siyasa": ["zabe", "shugaba", "gwamna", "kuri'a", "jam'iyya", "kamfen", "mulki", "shugabanci", "dan majalisa", "minista", "kwamishina", "shugaban kasa", "sanata", "siyasa", "demokradiyya", "APC", "PDP", "NNPP"],
    
    # --- WASANNI ---
    "wasanni": ["kwallo", "dambe", "kokawa", "tsere", "gudu", "filin wasa", "referee", "goal", "fans", "jersey", "kungiya", "barcelona", "madrid", "arsenal", "chelsea", "man u", "premier league", "laliga"],
    
    # --- LOKACI ---
    "lokaci": ["yau", "gobe", "jibi", "shekara", "wata", "agogo", "mintuna", "dakika", "safe", "yamma", "dare", "rana", "makon", "kwanaki", "lokuta", "da safe", "da rana", "da dare", "wata", "shekara"],
    
    # --- DANGANTAKA ---
    "dangantaka": ["uwa", "uba", "dan uwa", "'yar uwa", "dangi", "kakanni", "jikoki", "aboki", "makwabci", "yara", "iyali", "mata", "miji", "danta", "yarta", "suruki", "suruka", "abokai"],
    
    # ... (An takaita saboda tsayin code, amma tunanin AI zai yi amfani da wadannan don gano wasu)
}

# ==============================================================================
# 2. INTENT KEYWORDS (200+ NUFI)
# ==============================================================================
INTENTS = [
    # Requesting
    "inaso", "ina so", "so nake", "so", "bukata", "muradi", "ina bukatar", "ka bani", "nayi sha'awar", 
    "nayi niyyar", "ina marmarin", "ina kaunar", "ina son", "ina sha'awar", "bani", "ba ni", "ban", 
    "bamu", "ba", "kawo", "kawo min", "kawo mana", "a bani", "a kawo", "samar", "samarmin", "samarwa",
    
    # Creation
    "hada", "hadamin", "hada min", "hadawa", "tara", "tara min", "tara mana", "shirya", "shirya min",
    "kirkiri", "kirkira", "kirkiramin", "kirkire", "kirkiro", "kirkiro min", "kirkiro mana", "kirkirar",
    "rubuta", "rubutamin", "rubutawa", "rubuto", "rubuto min", "rubuto mana", "yi rubutu", "rubutun",
    
    # Search/Ask
    "nemo", "nemomin", "binciko", "duba", "duba min", "duba mana", "bincika", "binciko min", "nemo mana",
    "ina", "ina ne", "a ina", "ina zan samu", "ina ake samun", "nuna min", "nuna mana", "nuna",
    
    # Explain/Define
    "fassara", "juya", "ma'ana", "fassarawa", "juya min", "juya mana", "mene ne", "menene", "minene", "mecece",
    "gaya", "gayamin", "fada", "fadamin", "fada mana", "yi bayani", "yi sharhi", "sharhi", "bayani",
    
    # Math
    "lissafa", "lissafi", "kirga", "kirga min", "yi lissafin", "nawa ne", "nawa", "kudin", "jimla", "tara", "cire",
    
    # Advice/Story
    "shawara", "bada shawara", "ban shawara", "nasiha", "yi nasiha", "yi shawara", "ba da shawara",
    "labari", "bada labari", "ban labari", "labarin", "yi labari", "ba da labari", "tatsuniya",
    
    # Questions
    "tambaya", "tambayoyi", "amsa", "amsoshi", "tambaye", "tambayi", "amsawa", "amshe", "amsar"
]

# ==============================================================================
# 3. MATH ENGINE (ULTRA ADVANCED)
# ==============================================================================
def solve_math(text):
    text = text.lower()
    ops = {
        "ahada": "+", "hada": "+", "da": "+", "tara": "+", "jimla": "+", "kari": "+",
        "cire": "-", "rage": "-", "minus": "-", "babu": "-", "saura": "-",
        "sau": "*", "ninka": "*", "times": "*", "yawaita": "*", "ribanya": "*",
        "raba": "/", "kasa": "/", "divide": "/", "rabin": "/2", "cikin": "/",
        "iko": "**", "power": "**", "tushen": "math.sqrt", "sqrt": "math.sqrt",
        "kaso": "/100", "percent": "/100"
    }
    
    for k, v in ops.items():
        text = text.replace(k, v)
    
    num_map = {
        'daya':1, 'biyu':2, 'uku':3, 'hudu':4, 'biyar':5, 'shida':6, 'bakwai':7, 'takwas':8, 'tara':9, 'goma':10,
        'ashirin':20, 'talatin':30, 'arba\'in':40, 'hamsin':50, 'sittin':60, 'saba\'in':70, 'tamanin':80, 'casa\'in':90,
        'dari':100, 'dubu':1000, 'miliyan':1000000, 'biliyan':1000000000, 'triliyan':1000000000000, 'sifili':0, 
        'daya da rabi': 1.5, 'rabi': 0.5, 'kwata': 0.25
    }
    
    if "na" in text and "/100" in text: text = text.replace("na", "*")

    for k, v in num_map.items():
        text = text.replace(k, str(v))
        
    try:
        clean_expr = ""
        allowed = "0123456789.+-*/()math.sqrt"
        for char in text:
            if char in allowed: clean_expr += char
            
        if any(op in clean_expr for op in ['+', '-', '*', '/', 'sqrt']):
            result = eval(clean_expr)
            if isinstance(result, float) and result.is_integer():
                return f"Lissafin ya kama: {int(result)}"
            return f"Lissafin ya kama: {round(result, 4)}"
    except:
        return None
    return None

# ==============================================================================
# 4. MASTER BRAIN (GENERATION & RETRIEVAL)
# ==============================================================================
class FHA_Brain:
    def __init__(self):
        self.sentences = []
        self.markov_chain = defaultdict(list)
        self.load_brain()

    def load_brain(self):
        if not os.path.exists(BRAIN_FILE):
            with open(BRAIN_FILE, "w") as f: f.write("FHA AI yana aiki.\n")
        
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            text = f.read()
            self.sentences = [s.strip() for s in re.split(r'[.!?\n]', text) if len(s) > 5]
            
            words = re.findall(r'\w+', text.lower())
            for i in range(len(words) - 2): 
                key = (words[i], words[i+1])
                val = words[i+2]
                self.markov_chain[key].append(val)

    def expand_query(self, query):
        words = re.findall(r'\w+', query.lower())
        expanded = words[:]
        for w in words:
            if w in RELATIONS:
                expanded.extend(RELATIONS[w])
        return expanded

    def vector_search(self, query):
        query_words = self.expand_query(query)
        query_vec = Counter(query_words)
        best_score = 0
        best_sent = ""

        for sent in self.sentences:
            sent_words = re.findall(r'\w+', sent.lower())
            sent_vec = Counter(sent_words)
            intersection = set(query_vec.keys()) & set(sent_vec.keys())
            numerator = sum([query_vec[x] * sent_vec[x] for x in intersection])
            sum1 = sum([query_vec[x]**2 for x in query_vec.keys()])
            sum2 = sum([sent_vec[x]**2 for x in sent_vec.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            
            if not denominator: score = 0.0
            else: score = float(numerator) / denominator
            
            if score > best_score:
                best_score = score
                best_sent = sent
        
        if best_score > 0.15: return best_sent
        return None

    def generate_sentence(self, seed_word, length=20): 
        # **SHORT GENERATION (20 WORDS MAX)**
        starts = [k for k in self.markov_chain.keys() if seed_word in k]
        
        if not starts and seed_word in RELATIONS:
            for rel in RELATIONS[seed_word]:
                starts = [k for k in self.markov_chain.keys() if rel in k]
                if starts: break
        
        if not starts: return None
        
        current_pair = random.choice(starts)
        output = list(current_pair)
        
        for _ in range(length):
            next_opts = self.markov_chain.get(current_pair)
            if not next_opts: break
            next_word = random.choice(next_opts)
            output.append(next_word)
            current_pair = (output[-2], output[-1])
            
        text = " ".join(output) + "."
        return text.capitalize()

    # --- SPECIAL GENERATORS ---
    def generate_love_msg(self):
        templates = [
            "Ke ce tauraruwar zuciyata, hasken da ke haskaka rayuwata.",
            "  Soyayya abu ce mai kama da iska: ba a ganinta, amma ana jin ta sosai a zuciya. Tun daga lokacin da na fara saninki, zuciyata ta canza kamar yadda safiya ke sauya launin sararin samaniya daga duhu zuwa haske. A duk lokacin da na tuna da ke, zuciyata tana bugawa da wani irin natsuwa mai ban mamaki, kamar ki ne kadai abin da nake buƙata domin in ji daɗin duniya. ",
            "Akwai wani abu a cikin murmushinki da yake kwantar min da hankali. Idan kika yi murmushi, ina jin kamar rana ta fito a cikin zuciyata, ta yayyafa haske a kan duk wani abu da ya taba ba ni damuwa. Idan kika yi magana, kalamanki suna shiga kunnena cikin taushi, suna sauka a zuciyata kamar ruwa mai sanyi a lokacin zafi. Akwai wata hikima a zuciyarki da ban iya fasalta ta ba, amma ina yawan mamakin yadda mutum guda zai iya zama sauki da hikima lokaci guda.
",
"Ina son yadda kike fahimta ba tare da na yi bayani mai tsawo ba. Kamar zuciyata da taki suna da wata doguwar hanya da suke magana ba tare da kalmomi ba. Wannan abin ne ya sa ki zama ta daban—ba wai kawai saboda kyau ba, amma saboda irin halayenki masu kama da zinariya da ba su raguwa.",
"Idan na yi tunani game da makomarmu, nakan ga kaina ina dariya shi kaɗai. Saboda a tunanina, ke ce nake gani a gefe na. Ke ce nake jiyo dariyarki a cikin ɗakina, kamar ki na tsaye kusa da zuciyata kina sharar damuwa daga kowace kusurwa. Ina mafarkin mu zauna tare muna tattaunawa ba tare da gajiya ba. Ina mafarkin ranar da zaki ce min da kanki cewa ni ne wanda kika ga ya dace ya riƙe hannunki har zuwa karshen rayuwa.",
            "Soyayya dake tsakaninmu ta wuce misali, ba zan taba manta ki ba.",
            "Idan babu ke, duniya ta zama duhu. Ke ce farin cikina.",
            "Ina sonki fiye da yadda nake son kaina. Ke ce zabin raina."
            "Idan da zan iya, zan tattara dukkan taurarin sama na baki, saboda duk lokacin da nake tare da ke, ina jin kamar na shiga wani wuri da ke cike da haske. Amma abin da zan iya ba ki yanzu shi ne gaskiyar zuciyata: ina sonki da gaskiya, ina kaunarki ba tare da sharadi ba, kuma ina fatan soyayyarmu ta zama hanyar da ba za ta taɓa karewa ba", 
            "Gaskiya ita ce: na sami natsuwa da farin ciki a wajenki, fiye da yadda na taɓa tsammani. Ba wai saboda kin yi wani abu mai girma ba, amma saboda kina dai kasancewa ke. Halinki, murmushinki, tunaninki, da zuciyarki—duk sun haɗu sun zama wuri guda wanda ya sa zuciyata ta samu nutsuwa.",
            "Akwai lokuta da nakan zauna kawai ina tunanin sunanki. A wannan lokacin nakan ji wani irin nutsuwa mai ban mamaki. Sunanki yana ɗauke da sauti na salama, kamar waka ce da ake rerawa cikin dare mai sanyi. Wani lokaci kuwa nakan yi tunanin ko ke ma kina tunani kamar haka—idan kina tuna ni kamar yadda nake tuna ki, idan zuciyarki tana bugawa da ƙarfi idan sunana ya zo miki kwatsam. Idan hakane, to lallai soyayyarmu za ta kasance tamkar bishiya mai raɗaɗin ƙafa, tana da tushe mai ƙarfi, tana fitar da furanni masu wari"
        ]
        return random.choice(templates)

    def generate_apology(self):
        templates = [
            "Dan Allah kayi hakuri, ba zan sake ba. Sharrin shaidan ne.",
            "Nasan na bata maka rai, amma dan Allah ka yafe min.",
            "Kayi hakuri abokina, kuskure ne aka samu.",
            "Zuciyata tana cike da nadama, dan Allah ka karbi tubana.",
            "Na zo gare ka da zuciya mai sauƙi, mai cike da nadama da tunani mai zurfi. Ban zo da yawan magana ba, sai dai gaskiyar da zuciyata ke ɗauke da ita. Na fahimci kuskurena, na gane cewa na bata maka rai, kuma hakan ba abin da nake so ba ko kaɗan. Ina so ka san cewa bana son ganin ka cikin damuwa ko baƙin ciki saboda wani abu da ya fito daga gare ni",
            "Wani lokaci mu kan yi kuskure ba tare da gangan ba, amma hakan baya nufin ba mu damu ba. Na yi la’akari da duk abin da ya faru, na duba maganganuna, halayena, da yadda abubuwa suka tafi. Ina jin nauyin hakan a zuciyata, kuma ina so in gyara komai domin ka ji sanyi da kwanciyar hankali. Ba zan ɓoye ba—na ji zafi ganin cewa na sa ka ɓacin rai. Na yarda, na kuskura, kuma na amince da kuskurena",
            "Ina so ka saurare ni da zuciya mai taushi kamar yadda nake zo maka da zuciya mai gaskiya. Bani da hujja, bani da kariya, sai dai roƙon ka da ka bani dama na gyara abin da ya faru. Na san darajar ka, na san muhimmancinka a rayuwata, kuma bana son wani abu ya shiga tsakaninmu ya jawo mana nisa. Idan zan iya, zan goge duk abin da ya faru in mayar da shi kamar bai taɓa kasancewa ba.",
            "Ka yafe min don Allah. Yafiyarka ba karamin abu ba ne a gurina. Idan ka bani haƙuri, wannan zai ba ni ƙarfi da kwarin gwiwa na guje wa irin wannan kuskure gaba ɗaya nan gaba. Ina so ka san cewa ba zan taɓa raina ka ba, kuma ban yi abu domin cutarwa ba. Na yi kuskure ne saboda ni mutum ne, kuma mutum ba zai taɓa tserewa daga kuskure ba, amma zai iya gyarawa idan an bashi dama.",
            "Ina yi maka alkawari da gaskiya: zan fi kula da maganganuna, halayena, da duk abin da zai iya sa ka jin ciwo. Ina so mu ci gaba da kasancewa lafiya, mu ci gaba da girmama juna, mu ci gaba da zama kamar yadda ya kamata — cikin soyayya, mutunci, da fahimta. Ina matuƙar daraja ka, kuma ba zan so wani abu ya ɓaci a tsakaninmu ba.
"
        ]
        return random.choice(templates)

    def generate_friend_chat(self):
        templates = [
            "Guy ya ake ciki ne? Kwana biyu naji ka shiru.",
            "Abokina, ya harkoki? Ina fatan komai yana tafiya daidai.",
            "Wallahi nima ina nan, sai godiyar Allah kawai.",
            "Ya gida da iyali? Allah ya bar zumunci.",
            "Guy ya ake ciki ne? Kwana biyu naji ka shiru.",
            "Kai fa? Shiru haka yau biyu?",
            "Lafiya dai? Naga ka yi missing."
        ]
        return random.choice(templates)

    def generate_advice(self, topic):
        reasons = [
            "Saboda gaskiya ita ce tushen natsuwa.",
            "Domin hakuri shine maganin zaman duniya.",
            "Saboda ilimi shine gishirin rayuwa.",
            "Domin gujewa dana-sani a nan gaba."
        ]
        return f"Shawarata akan {topic} ita ce ka bi a hankali. \n💡 Hujja: {random.choice(reasons)}"

    # --- EVALUATOR ---
    def evaluate_question(self, text):
        l = len(text.split())
        if "me yasa" in text or "yaya" in text: return "Wannan tambaya ce mai zurfi."
        if l < 3: return "Wannan tambaya ce mai sauki."
        return "Wannan tambaya ce mai kyau."

    def process(self, msg):
        # 1. Math Check
        math_res = solve_math(msg)
        if math_res: return math_res

        clean_msg = re.sub(r"[^\w\s]", "", msg.lower())

        # 2. Special Generators Check
        if "soyayya" in clean_msg:
            return f"❤️ {self.generate_love_msg()}"
        if "hakuri" in clean_msg:
            return f"🙏 {self.generate_apology()}"
        if "aboki" in clean_msg or "hira" in clean_msg:
            return f"👋 {self.generate_friend_chat()}"
        if "shawara" in clean_msg:
            return self.generate_advice(clean_msg)

        # 3. Intent Check (Generative)
        is_intent = any(i in clean_msg.split() for i in INTENTS)
        eval_note = self.evaluate_question(clean_msg)
        
        if is_intent:
            words = clean_msg.split()
            seed = words[-1]
            gen_res = self.generate_sentence(seed, length=20)
            if gen_res: return f"{eval_note}\nGa abin da na kirkira:\n{gen_res}"
            else: return "Ban samu isassun bayanai don kirkirar wannan ba.. bangane ba yi wata tammbayar"

        # 4. Vector Search
        search_res = self.vector_search(clean_msg)
        if search_res:
            return f"{eval_note}\nBisa fahimtata:\n{search_res}"

        # 5. Fallback Generation
        seed = clean_msg.split()[0]
        gen_res = self.generate_sentence(seed, length=20)
        if gen_res:
            return f"Ban gane sosai ba amma a iya sanina {gen_res}"

        return "Ban gane wannan ba.. canja tambaya koka je gemini ko chatGPT"

# Init
bot = FHA_Brain()

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.json
    return jsonify({"reply": bot.process(data.get("message", ""))})

if __name__ == '__main__':
    from os import getenv
    port = int(getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)