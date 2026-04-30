import random
import matplotlib.pyplot as plt

# =========================================================
# DATA (SUDAH FIX)
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
    "DS": "D1"
}

POP_SIZE = 60
GENERATIONS = 200
MUTATION_RATE = 0.3
ELITE_SIZE = 3

# =========================================================
# INIT    
# =========================================================
def create_schedule():
    return [(c, lecturers[c], random.choice(rooms), random.choice(times)) for c in courses]

def init_population():
    return [create_schedule() for _ in range(POP_SIZE)]

# =========================================================
# KONFLIK
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
# =========================================================
def fitness(schedule):
    conflicts = conflict_details(schedule)
    score = 100 - len(conflicts) * 15
    return max(score, 0)

# =========================================================
# REPAIR (SMART)
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
# =========================================================
def selection(pop):
    return max(random.sample(pop, 3), key=fitness)

# =========================================================
# CROSSOVER
# =========================================================
def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

# =========================================================
# MUTATION
# =========================================================
def mutate(schedule):
    i = random.randint(0, len(schedule)-1)
    c, lec, _, _ = schedule[i]
    schedule[i] = (c, lec, random.choice(rooms), random.choice(times))
    return schedule

# =========================================================
# GA
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