def check_terms(word, word_separated, ordered_list):
    # check each ending
    maindict = {
        "iz": "verbal idea: to (do the action of) x \n noun: to make (something) x",
        "al": "pertaining to x",
        "genetic": "pertaining to the production of ",
        "ic": "pertaining to x",
        "ous": "pertaining to x",  # note not covering any latin endings here
        "ar": "pertaining to x",
        "an": "pertaining to x",
        "in": "pertaining to x",
        "ac": "pertaining to x",
        "oid": "something resembling x",  # used to be "pertaining to x"
        "ia": "an abnormal condition involving x",
        "ist": "verbal idea: one who (does the action of) \n noun: one who specializes in x",
        "in": "a substance (which does the action) of ",
        "it": "the inflammation of ",
        "rrhex": "the rupturing of ",
        "schis": "the splitting of ",
        "ias": "the abnormal presence of ",
        "clas": "the breaking of ",
        "os": "an abnormal condition involving x",
        "pathy": "a disease of ",
        "phag": "the ingestion of ",
        "poi": "the formation of ",
        "kin": "the movement of ",
        "algia": "Can x feel pain? pain in x\nElse: pain involving x",
        "dynia": "Can x feel pain? pain in x\nIf not: pain involving x",
        "pleg": "the paralysis of ",
        "pen": "a deficiency of ",
        "rrhag": "the rapid flowing of (something from) x",
        "malac": "the softening of ",
        "necros": "the death of ",
        "steno": "the narrowing of ",
        "scleros": "the hardening of ",
        "opto": "he downward displacement of ",
        "agr": "gouty pain in x",
        "rrhe": "the flowing of (something from) x",
        "edema": "the swelling of ",
        "cel": "the protrusion of (something through) x",
        "lith": "a calculus in(volving) x",
        "spasm": "a spasm of ",
        "ism": "a spasm of ",
        "ectop": "the displacement of ",
        "ectas": "the distention of ",
        "plas": "the formation of ",
        "dysplas": "the defective formation of ",
        "otroph": "the growth/nourishment of ",
        "dystroph": "the defective growth of ",
        "atroph": "the lack of growth of ",
        "asthen": "the lack of strength of ",
        "therap": "treatment by means of ",
        "iatr": "the healing of ",
        "stas": "the stopping of ",
        "plast": "the surgical repairing of ",
        "cent": "the surgical puncturing of ",
        "rrhaph": "the suturing of ",
        "tom": "the cutting of ",
        "ectom": "the cutting out of ",
        "stom": "the making of an opening in x",
        "ics": "the science of ",  # check if the 's' needs to be included or not
        "log": "the study of ",
        "scop": "the examination of ",
        "metr": "the measurement of ",
        "graphy": "the recording of ",
        "pex": "the adhesion of x [diagnostic] \n the fixation of x [therapeutic]",
        "ly": "the disintegration of x [diagnostic] \n the separation of the adhesions of x [therapeutic]",
        "otrop": "the tendency to preferentially affect x",
        "phage": "something which ingests x",
        "tome": "an instrument for cutting x",
        "ectome": "an instrument for cutting out x",
        "scope": "an instrument for examining x",
        "clast": "something which breaks x",
        "stat": "something which stops x",
        "gen": "a substance which produces x",
        "path": "one with a disease of ",
        "graph": "an instrument for recording x",
        "gram": "a record of ",
        "meter": "an instrument for measuring x",
        "genic": "producing x",
        "genous": "produced by x",
        "tropic": "preferentially affecting x",
        "anthrop": "man, human",
        "som": "body",
        "somat": "body",
        "derm": "skin",
        "dermat": "skin",
        "epiderm": "epidermis",
        "epidermat": "epidermis",
        "cyt": "cell",
        "ocyt": "a cell of ",
        "arthr": "(a) joint",
        "acr": "extremities",
        "mel": "limb",
        "cephal": "head",
        "trich": "hair",
        "blephar": "eyelid(s)",
        "ophthalm": "eye",
        "ot": "an abnormal condition involving x",
        "rhin": "nose",
        "pros": "face",
        "faci": "face",
        "cervic": "neck",
        "trachel": "neck",
        "om": "shoulder",
        "brachi": "arm",
        "ancon": "elbow",
        "cheir": "hand",
        "chir": "hand",
        "dactyl": "digit",
        "onych": "nail",
        "thorac": "chest",
        "steth": "chest",
        "mast": "breast",
        "mamm": "breast",
        "thel": "nipple",
        "omphal": "navel",
        "umbil": "navel",
        "umbilic": "navel",
        "glut": "buttock",
        "glute": "buttock",
        "gon": "knee",
        "gony": "knee",
        "pod": "foot",
        "ped": "foot",
        "oste": "bone",
        "ostos": "the ossification of ",
        "oss": "bone",
        "osse": "bone",
        "skelet": "skeleton",
        "crani": "skull",
        "cleid": "collar bone",
        "clavicul": "collar bone",
        "calv": "collar bone",
        "clavic": "collar bone",
        "acromi": "acromion",
        "corac": "coracoid process",
        "caracoid": "coracoid process",
        "humer": "humerus",
        "cubit": "elbow",
        "uln": "ulna",
        "radi": "radius",
        "carp": "wrist",
        "phalang": "phalanges",
        "scapul": "shoulder blade",
        "rachi": "spine",
        "rhachi": "spine",
        "spin": "spine",
        "myel": "spinal cord or bone marrow",
        "spondyl": "vertebra",
        "vertebr": "vertebra",
        "cost": "rib",
        "stern": "sternum",
        "xiph": "xiphoid process",
        "xiphoid": "xiphoid process",
        "cox": "hip",
        "pelv": "pelvis",
        "pelvi": "pelvis",
        "ili": "ilium",
        "ischi": "ischium",
        "pub": "pubis",
        "sacr": "sacrum",
        "coccyg": "coccyx",
        "acetabul": "acetabulum",
        "femor": "femur",
        "patell": "knee-cap",
        "tibi": "tibia",
        "fibul": "fibula",
        "tars": "tarsus",
        "calcane": "calcaneus",
        "tal": "talus",
        "astragal": "talus",
        "chondr": "cartilage",
        "cartilag": "cartilage",
        "cartilagin": "cartilage",
        "my": "muscle",
        "myos": "muscle",
        "muscul": "muscle",
        "ten": "tendon",
        "tenon": "tendon",
        "tenont": "tendon",
        "tend": "tendon",
        "tendin": "tendon",
        "desm": "ligament",
        "syndesm": "ligament",
        "syndesmos": "ligament",
        "ligament": "ligament",
        "aponeur": "aponeurosis",
        "aponeuros": "aponeurosis",
        "achill": "Achilles’ tendon",
        "encephal": "brain",
        "cerebr": "cerebrum; brain",
        "cerebell": "cerebellum",
        "membran": "membrane",
        "mening": "meninges",
        "ependym": "ependyma",
        "neur": "nerve",
        "nerv": "nerve",
        "gangli": "ganglion",
        "ganglion": "ganglion",
        "neuron": "nerve cell",
        "gli": "neuroglia",
        "neurogli": "neuroglia",
        "radicul": "radicle",
        "sympath": "sympathetic nerves",
        "sympathet": "sympathetic nerves",
        "sympathic": "sympathetic nerves",
        "vag": "vagus nerve",
        "opt": "eye",
        "optic": "eye",
        "ocul": "eye",
        "cor": "pupil",
        "core": "pupil",
        "pupill": "pupil",
        "ker": "cornea",
        "kerat": "cornea",
        "corne": "cornea",
        "scler": "sclera",
        "retin": "retina",
        "uve": "uvea",
        "ir": "iris",
        "irid": "iris",
        "cycl": "ciliary body",
        "cili": "ciliary body",
        "ciliar": "ciliary body",
        "choroid": "choroid",
        "chori": "choroid",
        "conjunctiv": "conjunctiva",
        "canth": "canthus",
        "phac": "lens",
        "dacry": "tear",
        "lacrim": "tear",
        "dacryocyst": "tear sac",
        "tympan": "middle ear",
        "malle": "hammer",
        "incud": "anvil",
        "stapedi": "stirrup",
        "staped": "stirrup",
        "myring": "tympanic membrane",
        "hemia": "the abnormal presence of blood in x",
        "emia": "the abnormal presence of blood in x",
        "hem": "blood",
        "hemat": "blood",
        "haem": "blood",
        "sanguin": "blood",
        "sangui": "blood",
        "hemoglobino": "hemoglobin",
        "plasm": "plasma",
        "plasmat": "plasma",
        "thromb": "clot",
        "thrombocyt": "platelet",
        "sphygm": "pulse",
        "card": "heart",
        "cardi": "heart",
        "aort": "aorta",
        "aortic": "aorta",
        "valv": "valve",
        "valvul": "valve",
        "ventricul": "ventricle",
        "pericard": "pericardium",
        "pericardi": "pericardium",
        "myocard": "myocardium",
        "myocardi": "myocardium",
        "angi": "vessel",
        "angei": "vessel",
        "vas": "vessel",
        "vascul": "vessel",
        "arter": "artery",
        "arteri": "artery",
        "phleb": "vein",
        "ven": "vein",
        "capillar": "capillary",
        "varic": "varix",
        "cirs": "varix",
        "lymph": "lymph",
        "lymphat": "lymph",
        "lymphangi": "lymph vessel",
        "lymphaden": "lymph node",
        "splen": "spleen",
        "lien": "spleen",
        "crin": "secretion",
        "endocrin": "secretion",
        "hormon": "hormone",
        "aden": "gland",
        "glandul": "gland",
        "pineal": "pineal gland",
        "hypophys": "pituitary gland",
        "hypophyse": "pituitary gland",
        "parotid": "parotid gland",
        "parot": "parotid gland",
        "thyroid": "thyroid gland",
        "thyr": "thyroid gland",
        "parathyroid": "parathyroid gland",
        "parathyr": "parathyroid gland",
        "thym": "thymus",
        "adren": "adrenal gland",
        "adrenal": "adrenal gland",
        "supraren": "adrenal gland",
        "suprarenal": "adrenal gland",
        "insul": "islets of Langerhans",
        "gonad": "gonad",
        "pathic": "pertaining to a disease of ",
        "icist": "one who specializes in the science of ",
        "optica": "p.t. the eye",
        "a": "Singular. vena = the vein for example"
    }
    mainlist = sorted(maindict.keys(), key=len, reverse=True)
    front = 0
    back = -1
    for i in mainlist:
        if i in word:
            if word.find(i) != front:#word is not at the beginning
                if word[word.find(i)+len(i)-1] != word[back]: #word is not at the end
                    word_segment = word[word.find(i)-1:word.find(i)+len(i)+1]
                    if word_segment[front] == "*" or word_segment[front] == " ": #check whether to worry about front
                        if word_segment[back] != "*" and word_segment[back] != " ":#check whether to worry about back
                            word_separated = word_separated.replace(i, i + "/")
                    else:#need to replace front
                        if word_segment[back] != "*" and word_segment[back] != " ":  # check whether to worry about back
                            word_separated = word_separated.replace(i,"/" + i + "/")
                        else:
                            word_separated = word_separated.replace(i, "/"+ i) #need to replace front only
                else: #word is at the end
                    word_segment = word[word.find(i) - 1] #grab front end of letter
                    if word_segment != "*" and word_segment != " ":
                        word_separated = word_separated.replace(i, "/"+i)  # add word to beginning
            else:#the word is at the beginning
                if word[word.find(i) + len(i)] != word[-1]:  # word is not at the end
                    word_segment = word[word.find(i) + len(i) + 1]
                    if word_segment != "*" and word_segment != " ":
                        word_separated = word_separated.replace(i, i + "/") #add word to ending


            ordered_list[word.find(i)] = maindict[i]
            word = word.replace(i, '*' * len(i))
    return word, word_separated, ordered_list


phrase = input("Type quit to exit the program.\nPlease enter a medical phrase: ")
phrase_separated = phrase
ordered_phrase_list = [""] * 63

while phrase != "quit":
    if phrase[:2] == "ot":
        phrase_separated = phrase_separated.replace("ot", "ot/")
        ordered_phrase_list[0] = "ear"
        phrase = "**" + phrase[2:]
    if phrase[-3:] == "oid":
        phrase_separated = phrase_separated.replace("oid", "/oid")
        ordered_phrase_list[-1] = "ear"
        phrase = phrase[:-3] + "***"
    phrase, phrase_separated, ordered_phrase_list = check_terms(phrase, phrase_separated, ordered_phrase_list)
    all_together_phrase = ""
    for i in range(1,64):
        if ordered_phrase_list[-i] != "":
            all_together_phrase = all_together_phrase + ordered_phrase_list[-i]
            all_together_phrase = all_together_phrase + " - "
    if all_together_phrase[-3:] == " - ":
        all_together_phrase = all_together_phrase[:-3]
    print(phrase_separated + ": " + all_together_phrase)

    print("\nNote to self:\n-Assume all nouns have a 'the' in front of them.")
    print("-possible connection words: something/a/the")
    phrase = input("\nType quit to exit the program.\nPlease enter a medical phrase: ")
    phrase_separated = phrase
    ordered_phrase_list = [""] * 63
