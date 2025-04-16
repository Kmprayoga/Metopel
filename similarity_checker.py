def jaccard_similarity(vec1, vec2):
    intersection = sum([1 for i in range(len(vec1)) if vec1[i] == vec2[i] == 1])
    union = sum([1 for i in range(len(vec1)) if vec1[i] == 1 or vec2[i] == 1])
    return intersection / union if union != 0 else 0

# sub-fitur
sub_features = [
    "Suhu:demam", "Suhu:menurun", "Suhu:meningkat", "Suhu:tinggi", "Suhu:panas",
    "Nafsu:hilang", "Nafsu:menurun", "Nafsu:tidak ada", "Nafsu:turun",
    "AirLiur:darah", "AirLiur:berlebihan", "AirLiur:terus menerus",
    "Tubuh:pembengkakan", "Tubuh:ada benjolan", "Tubuh:paha gemetar", "Tubuh:ambruk",
    "Mulut:keluar darah", "Mulut:melepu", "Mata:kebiruan", "Mata:tidak peka cahaya",
    "Telinga:keluar darah",
    "AirSusu:berubah", "AirSusu:mengandung kuman", "AirSusu:kuning/kemerahan",
    "Gelisah", "BeratBadan:menurun drastis",
    "Nafas:sulit", "Leher:membengkak", "Leher:melipat", "Leher:bergetar/kejang"
]

# Basis kasus 
basis_kasus = {
    "Antraks":                  ["Suhu:demam", "AirLiur:darah", "Tubuh:pembengkakan", "Mulut:keluar darah", "Telinga:keluar darah"],
    "PMK":                      ["Suhu:menurun", "Nafsu:menurun", "AirLiur:berlebihan", "Mulut:melepu"],
    "Ngorok/SE":                ["Suhu:demam", "Nafas:sulit", "Leher:membengkak"],
    "Foot Rot":                 ["Tubuh:ada benjolan"],
    "Myasis":                   ["Nafsu:menurun", "AirLiur:terus menerus", "Gelisah", "BeratBadan:menurun drastis"],
    "Anthrax (lain)":           ["Suhu:demam", "Nafsu:hilang", "Tubuh:paha gemetar", "Mulut:keluar darah", "Telinga:keluar darah", "Tubuh:pembengkakan"],
    "Dysplasia Abomasum":       ["Nafsu:tidak ada"],
    "Sapi Gila":                ["AirLiur:terus menerus", "Tubuh:ambruk", "Leher:bergetar/kejang"],
    "Mastitis":                 ["Suhu:panas", "AirSusu:berubah"],
    "Keguguran":                ["AirSusu:mengandung kuman"],
    "Prolapsus Uteri":          ["Suhu:tinggi", "Nafsu:turun"],
    "Anthrax (varian 2)":       ["Suhu:meningkat", "AirSusu:kuning/kemerahan", "Nafas:sulit"],
    "Milk Fever":               ["Suhu:menurun", "Nafsu:menurun", "Mata:tidak peka cahaya", "Leher:melipat"],
    "Bloat":                    ["Mata:kebiruan", "Mulut:kebiruan", "Gelisah", "Nafas:sulit"]
}

# Buat hash table 
hash_table = {}
for penyakit, fitur in basis_kasus.items():
    biner = [1 if f in fitur else 0 for f in sub_features]
    hash_table[penyakit] = biner

# Input 
print("Masukkan gejala kasus baru (pisahkan dengan koma):")
print("Contoh: Suhu:demam, Nafsu:menurun, AirLiur:berlebihan")
input_str = input("Gejala: ")
input_features = [x.strip() for x in input_str.split(",")]
input_vector = [1 if f in input_features else 0 for f in sub_features]

print("\nHasil kemiripan dengan Jaccard Similarity:")
results = []
for penyakit, vektor in hash_table.items():
    sim = jaccard_similarity(input_vector, vektor)
    results.append((penyakit, sim))

results.sort(key=lambda x: x[1], reverse=True)
for penyakit, sim in results:
    print(f"- {penyakit}: {sim:.2f}")
