from Agent import Agent
from heuristics import furthestDistanceFromMeanAndClosestToUs
from sys import exit, argv
import traceback


if __name__ == "__main__":
    # Let's try and play
    if len(argv) > 2:
        fileName = argv[2]
    else:
        fileName = "effectiveness.csv"
    f = open(fileName, "w")
    print("trial, result, optimal, taken",file=f)
    print("trial, result, optimal, taken")
    # First argument is nuber of trials to run
    for i in range(int(argv[1])):
        try:
            agent = Agent("NetHackScore-v0", furthestDistanceFromMeanAndClosestToUs)
            result, optimal, moves = agent.play()
        except KeyboardInterrupt:
            f.close()
            exit(0)
        except Exception as e:
            newLine = "\n"
            result = f'Crashed {traceback.format_exc().replace(newLine, "")}'
            optimal = 0
            moves = 0
        print(f"{i},{result},{optimal},{moves}", file=f)
        print(f"{i},{result},{optimal},{moves}")
    f.close()