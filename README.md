import random
import matplotlib.pyplot as plt

# =========================================================
# DATA (SUDAH FIX)
    Tentu, mari kita bedah variabel-variabel ini dalam konteks pembuatan jadwal otomatis menggunakan Algoritma Genetika. Intinya, kamu sedang mensimulasikan proses evolusi untuk mencari kombinasi jadwal yang paling "pas" tanpa ada bentrok.
# =========================================================
courses = ["AI", "DB", "WEB", "ML", "IOT", "SE", "DS"]

rooms = ["R1", "R2"]
times = ["P1", "P2", "P3", "P4"]  # 🔥 FIX: tambah slot

lecturers = {
    "AI": "D1",
    "DB": "D1",
    "WEB": "D2",
    "ML": "D2",
    "IOT": "D3",
    "SE": "D3",
    "DS": "D1"d
}

POP_SIZE = 60
GENERATIONS = 200
MUTATION_RATE = 0.3
ELITE_SIZE = 3

# =========================================================
# INIT    
    Fungsi create_schedule dan init_population bertugas untuk menciptakan "generasi awal" dengan cara memasangkan setiap mata kuliah ke ruangan dan waktu secara acak sebanyak 60 variasi jadwal. Karena prosesnya acak, sangat besar kemungkinan terjadi bentrok, misalnya dua mata kuliah berbeda dijadwalkan di ruangan dan waktu yang sama.

Di sinilah fungsi repair berperan sebagai "petugas perbaikan" otomatis. Fungsi ini akan menyisir setiap jadwal dan mengecek apakah ada ruangan yang dipakai bersamaan; jika ditemukan bentrok, sistem akan langsung mencarikan slot ruangan atau waktu lain yang masih kosong untuk memindahkan jadwal tersebut. Hasil akhirnya adalah sekumpulan draf jadwal awal yang sudah dirapikan secara logis sehingga tidak ada lagi perebutan ruangan, sebelum nantinya divalidasi lebih lanjut oleh algoritma utama.
# =========================================================
def create_schedule():
    return [(c, lecturers[c], random.choice(rooms), random.choice(times)) for c in courses]

def init_population():
    return [create_schedule() for _ in range(POP_SIZE)]

# =========================================================
# KONFLIK
    Kode tersebut berfungsi untuk memperbaiki jadwal yang bentrok dengan memastikan setiap kegiatan memiliki kombinasi ruang (room) dan waktu (time) yang unik. Program ini menelusuri daftar jadwal dan mencatat pasangan ruang-waktu yang sudah terpakai ke dalam sebuah himpunan (set). Jika ditemukan jadwal yang menempati ruang dan waktu yang sudah digunakan sebelumnya, sistem akan mencari ruang dan waktu alternatif yang masih tersedia dari daftar referensi yang ada. Setelah menemukan slot yang kosong, jadwal tersebut akan diperbarui dan ditandai sebagai slot yang sudah terpakai agar tidak digunakan oleh kegiatan lain, sehingga hasil akhirnya adalah jadwal yang bersih dari konflik duplikasi tempat dan waktu.
# =========================================================
def conflict_details(schedule):
    room_time = {}
    lecturer_time = {}
    details = []

    for course, lec, room, time in schedule:

        if (room, time) in room_time:
            details.append(f"{course} bentrok RUANG dengan {room_time[(room,time)]} di {room}-{time}")
        else:
            room_time[(room, time)] = course

        if (lec, time) in lecturer_time:
            details.append(f"{course} bentrok DOSEN dengan {lecturer_time[(lec,time)]} di {time}")
        else:
            lecturer_time[(lec, time)] = course

    return details

# =========================================================
# FITNESS
    Fungsi fitness ini bertujuan untuk memberikan nilai evaluasi terhadap kualitas sebuah jadwal berdasarkan jumlah konflik yang ditemukan. Prosesnya dimulai dengan memanggil fungsi conflict_details untuk menghitung berapa banyak pelanggaran aturan yang terjadi, di mana setiap satu konflik akan mengurangi skor dasar 100 poin sebesar 15 poin. Hasil akhirnya dipastikan tidak akan bernilai negatif berkat penggunaan fungsi max(score, 0), sehingga semakin sedikit konflik yang ada, semakin tinggi skor "kebugaran" (fitness) jadwal tersebut mendekati angka 100.
# =========================================================
def fitness(schedule):
    conflicts = conflict_details(schedule)
    score = 100 - len(conflicts) * 15
    return max(score, 0)

# =========================================================
# REPAIR (SMART)
    Fungsi repair ini berfungsi untuk memperbaiki jadwal yang bentrok dengan cara memastikan setiap pasangan ruangan dan waktu (room, time) bersifat unik. Algoritma ini memindai seluruh jadwal dan menggunakan sebuah himpunan (set) bernama used untuk mencatat slot yang sudah terisi; jika ditemukan entri yang menggunakan slot yang sudah ada, fungsi akan mencari kombinasi ruangan dan waktu lain yang masih tersedia di dalam daftar rooms dan times. Setelah menemukan slot kosong, fungsi akan memperbarui jadwal tersebut dan menandai slot baru sebagai "terpakai", sehingga pada akhirnya fungsi mengembalikan jadwal yang telah bersih dari konflik duplikasi ruang dan waktu.
# =========================================================
def repair(schedule):
    used = set()

    for i in range(len(schedule)):
        c, lec, room, time = schedule[i]

        if (room, time) in used:
            for r in rooms:
                for t in times:
                    if (r, t) not in used:
                        schedule[i] = (c, lec, r, t)
                        used.add((r, t))
                        break
                else:
                    continue
                break
        else:
            used.add((room, time))

    return schedule

# =========================================================
# SELECTION
    Fungsi selection ini menerapkan mekanisme Tournament Selection sederhana untuk memilih individu terbaik dari populasi guna dilanjutkan ke tahap evolusi berikutnya. Cara kerjanya adalah dengan mengambil tiga kandidat secara acak dari populasi menggunakan random.sample, lalu membandingkan nilai kualitas mereka melalui fungsi fitness yang telah didefinisikan sebelumnya. Hasil akhirnya adalah satu individu dengan skor tertinggi di antara ketiganya yang terpilih sebagai "pemenang", memastikan bahwa proses seleksi tetap memberikan peluang bagi variasi genetik sambil tetap memprioritaskan individu yang memiliki jadwal paling optimal.
# =========================================================
def selection(pop):
    return max(random.sample(pop, 3), key=fitness)

# =========================================================
# CROSSOVER
    Fungsi crossover ini mengimplementasikan teknik Single-Point Crossover untuk menghasilkan individu baru (anak) dengan mengombinasikan materi genetik dari dua induk, p1 dan p2. Prosesnya dimulai dengan menentukan satu titik potong secara acak di sepanjang panjang jadwal, kemudian menyambungkan bagian awal dari induk pertama hingga titik tersebut dengan bagian akhir dari induk kedua mulai dari titik tersebut. Hasil penggabungan ini menciptakan variasi jadwal baru yang mewarisi sebagian karakteristik dari masing-masing induk, yang merupakan langkah krusial dalam algoritma genetika untuk mengeksplorasi solusi-solusi potensial yang lebih baik.
# =========================================================
def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

# =========================================================
# MUTATION
    Fungsi mutate ini bertujuan untuk memperkenalkan variasi genetik ke dalam populasi dengan cara mengubah satu elemen jadwal secara acak guna mencegah algoritma terjebak pada solusi yang kurang optimal (local optima). Prosesnya dilakukan dengan memilih satu indeks kegiatan dalam jadwal secara acak, mempertahankan data kursus dan dosennya, namun mengganti slot ruangan dan waktunya dengan pilihan baru yang diambil secara acak dari daftar rooms dan times. Melalui perubahan kecil yang spontan ini, fungsi mutasi memungkinkan algoritma untuk mengeksplorasi kemungkinan kombinasi jadwal lain yang mungkin belum muncul melalui proses persilangan (crossover).
# =========================================================
def mutate(schedule):
    i = random.randint(0, len(schedule)-1)
    c, lec, _, _ = schedule[i]
    schedule[i] = (c, lec, random.choice(rooms), random.choice(times))
    return schedule

# =========================================================
# GA
    Fungsi GA (Genetic Algorithm) ini merupakan inti dari proses evolusi yang mengoordinasikan seluruh tahapan algoritma genetika untuk mencari jadwal yang paling optimal. Dalam setiap generasinya, fungsi ini mengurutkan populasi berdasarkan nilai fitness, menyimpan individu terbaik melalui mekanisme elitism (ELITE_SIZE), serta memantau perkembangan skor rata-rata populasi. Melalui siklus iterasi, individu-individu baru dibentuk menggunakan proses seleksi, persilangan (crossover), mutasi, dan perbaikan jadwal (repair) hingga mencapai kriteria penghentian, yaitu ditemukannya solusi sempurna (skor 100) setelah melewati jumlah generasi tertentu.
# =========================================================
def GA():
    pop = init_population()

    best_hist = []
    avg_hist = []

    print("\n===== PROSES EVOLUSI =====\n")

    for gen in range(GENERATIONS):

        pop = sorted(pop, key=fitness, reverse=True)

        best = pop[0]
        best_fit = fitness(best)
        avg_fit = sum(fitness(p) for p in pop) / POP_SIZE

        best_hist.append(best_fit)
        avg_hist.append(avg_fit)

        if gen % 5 == 0:
            print(f"Gen {gen:3d} | Fitness: {best_fit} | Avg: {avg_fit:.2f}")

        # 🔥 jangan terlalu cepat stop
        if best_fit == 100 and gen > 20:
            print("\n🎯 SOLUSI OPTIMAL DITEMUKAN!")
            break

        new_pop = pop[:ELITE_SIZE]

        while len(new_pop) < POP_SIZE:
            p1 = selection(pop)
            p2 = selection(pop)

            child = crossover(p1, p2)

            if random.random() < MUTATION_RATE:
                child = mutate(child)

            # tidak selalu repair → biar evolusi terlihat
            if random.random() < 0.7:
                child = repair(child)

            new_pop.append(child)

        pop = new_pop

    # =====================================================
    # HASIL AKHIR
        Bagian kode ini berfungsi untuk menampilkan ringkasan hasil akhir dari proses algoritma genetika dengan mengidentifikasi individu terbaik dalam populasi. Setelah populasi diurutkan berdasarkan skor kebugaran tertinggi, program akan mencetak nilai fitness akhir dan rincian jadwal yang terpilih secara terstruktur. Selain itu, kode ini memberikan transparansi dengan melakukan pengecekan ulang melalui fungsi conflict_details; jika solusi belum sempurna, sistem akan merinci setiap konflik yang tersisa, sedangkan jika tidak ada masalah, sistem akan mengonfirmasi bahwa solusi optimal telah berhasil dicapai.
    # =====================================================
    best = sorted(pop, key=fitness, reverse=True)[0]
    conflicts = conflict_details(best)

    print("\n===== HASIL AKHIR =====")
    print("Fitness akhir :", fitness(best))

    print("\nJadwal Final:")
    for s in best:
        print(" -", s)

    if not conflicts:
        print("\nPenjelasan:")
        print("Tidak ada konflik → solusi optimal.")
    else:
        print("\nPenjelasan:")
        print(f"Terdapat {len(conflicts)} konflik:")
        for c in conflicts:
            print(" -", c)

    # =====================================================
    # VISUAL
       Bagian kode ini berfungsi untuk memvisualisasikan performa algoritma genetika selama proses evolusi berlangsung menggunakan pustaka Matplotlib. Dengan membuat grafik garis, Anda dapat memantau perbandingan antara skor fitness terbaik (best_hist) dan rata-rata populasi (avg_hist) di setiap generasinya. Grafik ini memudahkan analisis untuk melihat apakah algoritma berhasil mengalami peningkatan kualitas (konvergensi) seiring bertambahnya generasi, serta membantu mendeteksi apakah populasi masih memiliki variasi yang cukup atau sudah terjebak dalam kondisi stagnan. 
    # =====================================================
    plt.figure()
    plt.plot(best_hist)
    plt.plot(avg_hist)
    plt.title("Perkembangan Fitness")
    plt.xlabel("Generasi")
    plt.ylabel("Fitness")
    plt.legend(["Best", "Average"])
    plt.grid()
    plt.show()


# RUN
if __name__ == "__main__":
    GA()
