from Agent import Agent


if __name__ == "__main__":
    # Let's try and play
    f = open("effectiveness.csv", "w")
    print("trial, result",file=f)
    print("trial, result")
    for i in range(5):
        try:
            agent = Agent("NetHackScore-v0")
            result = agent.play()
        except:
            result = False
        print(f"{i},{result}", file=f)
        print(f"{i},{result}")
    f.close()