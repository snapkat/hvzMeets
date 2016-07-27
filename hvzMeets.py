def findAvailPlayers(sched, slot):
    player_ids = []
    for num, avail in enumerate(sched):
        if avail[slot] == 'OK': #ignores final count line cuz theres no "OK"
            player_ids.append(num)
    return player_ids


def findBestTimeSlots(day1, day2):
    """ day1 and day2 are matrices that represent player availabilities on different days. The first index is the player and the second is the time slot. Returns a tuple of times that would allow the maximum number of players to play at least once in the two days if there's one mission each day along with a list of the indices of those players. """
    avail_a = []
    avail_b = []
    best_set = []
    best_times = (-1, -1)
    max_peeps = 0
    for a in range(len(day1[0])):
        avail_a = findAvailPlayers(day1, a)
        for b in range(len(day2[0])):
            avail_b = findAvailPlayers(day2, b)
            avail = set(avail_a).union(set(avail_b))
            if len(avail) > max_peeps:
                max_peeps = len(avail)
                best_set = avail
                best_times = (a, b)

    return best_times, best_set


def main():
    with open('/tmp/Doodle.csv') as file:
        times = ["10AM", "11AM", "1PM", "2PM", "3PM", "4PM", "5PM"]
        players = []
        mon = []
        tue = []
        wed = []
        thur = []
        fri = []
        for line in file:
            line = line.strip().split(",")
            assert len(line) == 36, "Bad line length at for user %s" % line[0]
            players.append(line[0])
            mon.append(line[1:8])
            tue.append(line[8:15])
            wed.append(line[15:22])
            thur.append(line[22:29])
            fri.append(line[29:])

    times_m_t, players_m_t = findBestTimeSlots(mon, tue)
    times_w_t, players_w_t = findBestTimeSlots(wed, thur)

    fri_count = max(map(int, fri[-1]))
    slot = fri[-1].index(str(fri_count))
    friday_players = findAvailPlayers(fri, slot)

    print("Mon: %s Tues: %s" % (times[times_m_t[0]], times[times_m_t[1]]))
    print("Unique players: %s" % len(players_m_t))
    print("Wed: %s Thurs: %s" % (times[times_w_t[0]], times[times_w_t[1]]))
    print("Unique players: %s" % len(players_w_t))
    print("Fri: %s" % times[slot])
    print("Unique players: %d" % fri_count)
    attend_all = players_m_t.intersection(players_w_t, set(friday_players))
    attend_one = players_m_t.union(players_w_t, set(friday_players))
    print("Number players that can attend all: %d" % len(attend_all))
    print("Number players that can attend one: %d" % len(attend_one))

if __name__ == "__main__":
    main()
