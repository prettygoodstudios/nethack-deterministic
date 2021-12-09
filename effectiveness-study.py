from Agent import Agent
from heuristics import furthestDistanceFromMeanAndClosestToUs
import traceback

if __name__ == "__main__":
    # Let's try and play
    f = open("effectiveness.csv", "w")
    print("trial, result, optimal, taken",file=f)
    print("trial, result, optimal, taken")
    for i in range(2):
        try:
            agent = Agent("NetHackScore-v0", furthestDistanceFromMeanAndClosestToUs)
            result, optimal, moves = agent.play()
        except Exception as e:
            newLine = "\n"
            result = f'Crashed {traceback.format_exc().replace(newLine, "")}'
            optimal = 0
            moves = 0
        print(f"{i},{result},{optimal},{moves}", file=f)
        print(f"{i},{result},{optimal},{moves}")
    f.close()