from Agent import Agent


if __name__ == "__main__":
    # Let's try and play
    f = open("effectiveness.csv", "w")
    print("trial, result",file=f)
    print("trial, result")
    for i in range(2):
        try:
            agent = Agent("NetHackScore-v0")
            result, optimal, moves = agent.play()
        except Exception as e:
            result = f'Crashed {e}'
            optimal = 0
            moves = 0
        print(f"{i},{result},{optimal},{moves}", file=f)
        print(f"{i},{result},{optimal},{moves}")
    f.close()