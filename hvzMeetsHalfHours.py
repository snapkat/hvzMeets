def findAvailOnDay(day, slot):
    player_ids = []
    for num, avail in enumerate(day):
        if avail[slot] == 'OK': #ignores final count line cuz theres no "OK"
            player_ids.append(num)
    return player_ids

def findAvail(schedule):
    # Find available hours
    # schedule is [day]x[players]x[time]
    avail_mx = [[None]*len(schedule[0][0])]*len(schedule) #[day]x[time]
    for dayNum, day in enumerate(schedule): #each day
        for slot in range(len(day[0])):  #each timeslot
            avail_mx[dayNum][slot]=findAvailOnDay(day,slot)

    return avail_mx

def findBetweenHours(avail):
    # Find the players that would be available for each two hour slot.
    # avail is [day]x[time]x[players]
    halfHours = [[None]*6]*5 #[day]x[half-hour]x[players]
    for dayNum, day in enumerate(avail):
        for time in range(len(day)):
            if time == len(day)-1: # skip the last one
                continue
            halfHours[dayNum][time] = set(day[time]).intersection(set(day[time+1]))
    return halfHours

def findCrossDays(day1, day2):
    # Find the best 2 day timeslot combination that would involve the most unique players
    # days are [time]xset([players])
    max_player_set = []
    bestTimes = (-1.-1)
    for i1, h1 in enumerate(day1):
        if i1 == 1: # This one is not a valid hour
            continue
        for i2, h2 in enumerate(day2):
            if i2 == 1: # This one isn't a valid half hour
                continue
            players = h1.union(h2)
            if len(players)>len(max_player_set):
                bestTimes = (i1,i2)
                max_player_set = players
    return bestTimes, max_player_set

def main():
    with open('/tmp/Doodle.csv') as file:
        times = ["10:30AM", "INVALID", "1:30PM", "2:30PM", "3:30PM", "4:30PM"]
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

    week = [mon, tue, wed, thur, fri]
    avail = findBetweenHours(findAvail(week))

    times_m_t, players_m_t = findCrossDays(avail[0], avail[1])
    times_w_t, players_w_t = findCrossDays(avail[2], avail[3])
    fri_players = []
    fri_time = -1
    for i1, h1 in enumerate(avail[4]):
        if i1 == 1:
            continue
        if len(h1) > len(fri_players):
            fri_time = i1
            fri_players = h1

    print("Total # Players: %d" % (len(mon)-1))
    print("Mon: %s Tues: %s" % (times[times_m_t[0]], times[times_m_t[1]]))
    print("Unique players: %s" % len(players_m_t))
    print("Wed: %s Thurs: %s" % (times[times_w_t[0]], times[times_w_t[1]]))
    print("Unique players: %s" % len(players_w_t))
    print("Fri: %s" % times[fri_time])
    print("Unique players: %d" % len(fri_players))
    attend_all = players_m_t.intersection(players_w_t, set(fri_players))
    attend_one = players_m_t.union(players_w_t, set(fri_players))
    print("Number players that can attend all: %d" % len(attend_all)) #all being one of mon/tue, one of wed/thur and one fri
    print("Number players that can attend one: %d" % len(attend_one))


if __name__ == "__main__":
    main()
