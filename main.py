import json

def syarat_terpenuhi(r, memori):
    ada = [s in memori for s in r["jika"]]
    return all(ada) if r["mode"] == "dan" else any(ada)

def forward_chaining(kb, fakta_awal):
    memori = set(fakta_awal)
    asal = {}
    siklus = 0
    while True:
        cocok = [r for r in kb["aturan"] if r["maka"] not in memori and syarat_terpenuhi(r, memori)]
        if not cocok:
            print(f"Siklus {siklus + 1}: tidak ada aturan baru, berhenti")
            break
        r = cocok[0]
        siklus += 1
        memori.add(r["maka"])
        asal[r["maka"]] = r
        print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, asal

def tampilkan_alasan(fakta, asal, memori, tingkat=0):
    r = asal.get(fakta)
    if r is None:
        return
    syarat = [s for s in r["jika"] if s in memori]
    print("  " * tingkat + f"{fakta} <- {r['id']} ({', '.join(syarat)}) [{', '.join(r['sumber'])}]")
    for s in syarat:
        tampilkan_alasan(s, asal, memori, tingkat + 1)

def main():
    with open("kb_baterai.json", encoding="utf-8") as f:
        kb = json.load(f)
    for r in kb["aturan"]:
        if isinstance(r["sumber"], str):
            r["sumber"] = [r["sumber"]]

    hasil = {r["maka"] for r in kb["aturan"]}
    fakta_dasar = []
    for r in kb["aturan"]:
        for s in r["jika"]:
            if s not in hasil and s not in fakta_dasar:
                fakta_dasar.append(s)

    print(kb["judul"])
    print("Jawab y/t.")
    fakta_awal = []
    for i, s in enumerate(fakta_dasar, 1):
        if input(f"{i}. Apakah {s}? (y/t) > ").strip().lower() == "y":
            fakta_awal.append(s)

    print("\nFakta awal:", ", ".join(fakta_awal) if fakta_awal else "-")
    memori, asal = forward_chaining(kb, fakta_awal)

    kesimpulan = [k for k in kb["kesimpulan"] if k in memori]
    if kesimpulan:
        print("\nKesimpulan:", ", ".join(kesimpulan))
        print("Alasan:")
        for k in kesimpulan:
            tampilkan_alasan(k, asal, memori, 1)
    else:
        print("\nKesimpulan: tidak ada kesimpulan dari fakta yang diberikan")
    print("\nCatatan:", kb["batas"])

main()