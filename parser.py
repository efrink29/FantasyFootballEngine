import json
import pandas as pd

class Player:
    def __init__(self, name, team, position, opponent, result, projected, actual):
        self.name = name
        self.team = team
        self.position = position
        self.opponent = opponent
        self.result = result
        self.projected = float(projected)
        self.actual = float(actual)

    def __str__(self):
        return f'{self.position}: {self.name}\tProj: {self.projected} Score: {self.actual}'


class Roster:
    def __init__(self):
        self.starters = []
        self.bench = []


def print_player(player):
    print(str(player))


def parse_player(lines, index):
    """
    Parse a player's data from the given lines starting from the given index.
    """
    # The data format based on the input:
    
    name = lines[index + 2].strip()  # Name (repeated twice, only need once)
    if name == 'Empty':
        return Player('Empty', 'Empty', 'Empty', 'Empty', 'Empty', 0, 0), index + 9
    team = lines[index + 3].strip()  # Team
    position = lines[index + 4].strip()  # Position (e.g., QB)
    if team == 'FA':
        opponent = '*BYE*'
    else:
        opponent = lines[index + 5].strip()  # Opponent
    #print(opponent)
    if opponent == '*BYE*':
        #print('BYE detected')
        result = 'BYE'
        projected = 0
        actual = 0
        return Player(name, team, position, opponent, result, projected, actual), index + 9
    result = lines[index + 6].strip()  # Result
    projected = lines[index + 7].strip()  # Projected score
    actual = lines[index + 8].strip()  # Actual score

    return Player(name, team, position, opponent, result, projected, actual), index + 9


def find_best(players):
    return max(players, key=lambda p: p.actual)


def print_player_list(players):
    for player in players:
        print_player(player)


def get_index(players, target_player):
    for index, player in enumerate(players):
        if player.name == target_player.name:
            return index
    return -1


def get_all_pos(roster, pos):
    players = [p for p in roster.starters if p.position == pos] + \
              [p for p in roster.bench if p.position == pos]
    return players


def get_score(players):
    return round(sum(p.actual for p in players),2)


def get_proj(players):
    return round(sum(p.projected for p in players),2)


def merge_lists(a, b):
    return a + b


def find_boom_bust(players):
    return sum(p.actual - p.projected for p in players)


def find_ideal(roster):
    qb = get_all_pos(roster, "QB")
    rb = get_all_pos(roster, "RB")
    wr = get_all_pos(roster, "WR")
    te = get_all_pos(roster, "TE")
    dst = get_all_pos(roster, "D/ST")
    k = get_all_pos(roster, "K")

    ideal = Roster()

    # Find best players by position
    QB1 = find_best(qb)
    qb.pop(get_index(qb, QB1))

    RB1 = find_best(rb)
    rb.pop(get_index(rb, RB1))

    RB2 = find_best(rb)
    rb.pop(get_index(rb, RB2))

    WR1 = find_best(wr)
    wr.pop(get_index(wr, WR1))

    WR2 = find_best(wr)
    wr.pop(get_index(wr, WR2))

    TE = find_best(te)
    te.pop(get_index(te, TE))

    # Handle FLEX (RB, WR, or TE)
    flex = merge_lists(rb, wr)
    flex = merge_lists(flex, te)

    FLEX = find_best(flex)
    flex.pop(get_index(flex, FLEX))

    DST = find_best(dst)
    dst.pop(get_index(dst, DST))

    K = find_best(k)
    k.pop(get_index(k, K))

    # Add the best players to the ideal roster
    ideal.starters = [QB1, RB1, RB2, WR1, WR2, TE, FLEX, DST, K]
    ideal.bench = qb + flex + dst + k

    return ideal


def parse_roster(filename):
    roster = Roster()

    with open(filename, 'r') as file:
        lines = file.readlines()

    index = 0

    # Parse starters (first 9 players)
    for _ in range(9):
        player, index = parse_player(lines, index)
        roster.starters.append(player)

    # Skip lines until the bench section (finding "Bench")
    while "Bench" not in lines[index]:
        index += 1
    

    # Parse bench (next 7 players)
    for _ in range(7):
        player, index = parse_player(lines, index)
        roster.bench.append(player)

    return roster


def print_roster(roster):
    print(f'Starters: {get_score(roster.starters)}')
    print_player_list(roster.starters)
    print(f'\nBench: {get_score(roster.bench)}')
    print_player_list(roster.bench)

def get_player_json(player):
    return {
        'name': player.name,
        'team': player.team,
        'position': player.position,
        'opponent': player.opponent,
        'result': player.result,
        'projected': player.projected,
        'actual': player.actual
    }

def convert_to_json(roster):
    return {
        'score': get_score(roster.starters),
        'starters': [get_player_json(p) for p in roster.starters],
        'bench': [get_player_json(p) for p in roster.bench]
    }

def save_to_json(roster, filename):
    data = {}
    data['Score'] = get_score(roster.starters)
    data['Projected'] = get_proj(roster.starters)
    data['PlusMinus'] = round(data['Score'] - data['Projected'], 2)
    data['BenchPoints'] = get_score(roster.bench)
    data['Unused'] = get_score(find_ideal(roster).starters) - data['Score']
    data['Actual'] = convert_to_json(roster)
    data['Ideal'] = convert_to_json(find_ideal(roster))
    
    with open(filename, 'w') as file:
        json.dump(data, file)
        
def main():
    
    managers = ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player9', 'Player10', 'Player11','Player12']
    
    week = input('Enter the week number: ')
    week = int(week)
    print(f'Week {week}')
    recalc = True
    
    if not recalc:
        for manager in managers:
            filename = f'Inputs/{manager}.txt'
            actual_roster = parse_roster(filename)
            save_to_json(actual_roster, f'Outputs/Week{week}/{manager}.json')
    
    schedule = json.load(open('schedule.json'))
    df = pd.DataFrame(columns=['Manager', 'Score', 'Projected', 'Boom/Bust', 'Bench Points', 'Unused Points', 'Wins', 'Losses', 'Total PF', 'Ranking', 'Trend'])
    df['Manager'] = managers
    if week == 1:   
        df['Wins'] = 0
        df['Losses'] = 0
        df['Total PF'] = 0
        df['Ranking'] = 0
        df['Trend'] = 0
        
    else:
        df = pd.read_csv(f'Outputs/Week{week-1}/summary.csv')
    
    for manager in managers:
        manager_data = json.load(open(f'Outputs/Week{week}/{manager}.json'))
        df.loc[df['Manager'] == manager, 'Score'] = manager_data['Score']
        df.loc[df['Manager'] == manager, 'Projected'] = manager_data['Projected']
        df.loc[df['Manager'] == manager, 'Boom/Bust'] = manager_data['PlusMinus']
        df.loc[df['Manager'] == manager, 'Bench Points'] = manager_data['BenchPoints']
        df.loc[df['Manager'] == manager, 'Unused Points'] = manager_data['Unused']
        
    #print(df)
    for match in schedule[week - 1]:
        team1 = match['home']
        team2 = match['away']
        team1_data = json.load(open(f'Outputs/Week{week}/{team1}.json'))
        team2_data = json.load(open(f'Outputs/Week{week}/{team2}.json'))
        df.loc[df['Manager'] == team1, 'Total PF'] += team1_data['Score']
        df.loc[df['Manager'] == team2, 'Total PF'] += team2_data['Score']
        if team1_data['Score'] > team2_data['Score']:
            df.loc[df['Manager'] == team1, 'Wins'] += 1
            df.loc[df['Manager'] == team2, 'Losses'] += 1
        else:
            df.loc[df['Manager'] == team2, 'Wins'] += 1
            df.loc[df['Manager'] == team1, 'Losses'] += 1
    
    df = df.sort_values(by=['Wins', 'Total PF'], ascending=False, ignore_index=True)
    for index, row in df.iterrows():
        previous_rank = df.loc[index, 'Ranking']
        
        df.loc[index, 'Ranking'] = index + 1
        df.loc[index, 'Trend'] = previous_rank - (index + 1)
        
    # ---- Print Results ---- #
    df = df.round(3)
    print(df)
    
    pd.DataFrame.to_csv(round(df,2), f'Outputs/Week{week}/summary.csv', index=False)

    #print(previous_week_df)
    #previous_week_df.loc[previous_week_df['Manager'] == 'Connor', 'Wins'] += 1
    #print(previous_week_df)
    schedule = json.load(open('schedule.json'))
    
    manager_records = {}
    for manager in managers:
        manager_records[manager] = {'Wins': 0, 'Losses': 0, 'Total Bench Points': 0}
    for w in range(1, week + 1):
        df = pd.read_csv(f'Outputs/Week{w}/summary.csv')
        week_schedule = schedule[w-1]
        for match in week_schedule:
            home = match['home']
            away = match['away']
            home_score = df.loc[df['Manager'] == home, 'Bench Points'].values[0]
            away_score = df.loc[df['Manager'] == away, 'Bench Points'].values[0]
            if home_score > away_score:
                manager_records[home]['Wins'] += 1
                manager_records[away]['Losses'] += 1
            else:
                manager_records[away]['Wins'] += 1
                manager_records[home]['Losses'] += 1
            manager_records[home]['Total Bench Points'] += home_score
            manager_records[away]['Total Bench Points'] += away_score
    for manager in managers:
        manager_records[manager]['Total Bench Points'] = round(manager_records[manager]['Total Bench Points'], 2)
    
    sorted_records = sorted(manager_records.items(), key=lambda x: (x[1]['Wins'], x[1]['Total Bench Points']), reverse=True)
    #print(sorted_records)
    # Initialize an empty list to store the rows
    data = []

# Iterate over the managers and their records
    for manager in managers:
        data.append({
            'Manager': manager,
            'Wins': manager_records[manager]['Wins'],
            'Losses': manager_records[manager]['Losses'],
            'Total Bench Points': manager_records[manager]['Total Bench Points']
        })

    # Create the DataFrame from the list of dictionaries
    records_df = pd.DataFrame(data)

    records_df = records_df.sort_values(by=['Wins', 'Total Bench Points'], ascending=False, ignore_index=True)
    # Display the DataFrame
    #print(records_df)

    
    pd.DataFrame.to_csv(records_df, f'Outputs/Week{week}/bench_summary.csv', index=False)
        
    
    

if __name__ == '__main__':
    main()
