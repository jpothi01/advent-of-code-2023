RED = 0
GREEN = 1
BLUE = 2

Game = list[tuple[int, int, int]]


def parse_game(line: str) -> tuple[int, Game]:
    def parse_color(color: str) -> int:
        if color == "red":
            return RED
        if color == "green":
            return GREEN
        if color == "blue":
            return BLUE
        raise ValueError()
        
    def parse_round_component(component: str) -> tuple[int, int]:
        split = component.split(" ")
        return (int(split[0]), parse_color(split[1]))
    
    def parse_round(round: str) -> tuple[int, int, int]:
        components = [parse_round_component(s.strip()) for s in round.split(",")]

        result = [0, 0, 0]
        for component in components:
            result[component[1]] = component[0]

        return (result[0], result[1], result[2])
        
    game_description, game_content = line.split(":")
    game_id = int(game_description[5:])
    rounds = game_content.split(";")
        
    return (game_id, [
        parse_round(round) for round in rounds
    ])


def min_bag_contents(game: Game) -> tuple[int, int, int]:
    return tuple(max(round[color] for round in game) for color in range(3))

def power(bag_contents: tuple[int, int, int]) -> int:
    return bag_contents[0] * bag_contents[1] * bag_contents[2]

sum = 0
bag_contents = (12, 13, 14)

assert parse_game("Game 10: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == (10, [
    (4, 0, 3),
    (1, 2, 6),
    (0, 2, 0)
])

assert min_bag_contents(parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")[1]) == (4, 2, 6)

with open("2/input.txt") as f:
    for line in f.readlines():
        game_id, game = parse_game(line)
        sum += power(min_bag_contents(game))

print(sum)