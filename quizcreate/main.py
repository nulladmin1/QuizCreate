import yaml
from os import path
import random
from typing import Optional

class QuizCreate:
    def __init__(self, configpath: Optional[str] = None, config: Optional[dict] = None ):
        if isinstance(configpath, str):
            ROOT_DIR = path.dirname(path.abspath(__file__))
            config_path = path.join(ROOT_DIR, configpath)
            with open(config_path, 'r') as c:
                self.config = yaml.safe_load(c)
        elif isinstance(config, dict):
            self.config = config
        else:
            raise ValueError("Either configpath or config should be provided")
        
        self.scores = {outcome: 0 for outcome in self.config['outcomes']}
    def run(self):
        print(f"Welcome to the {self.config['title']}")
        print(f"{self.config['description']}")
        
        for n, question in enumerate(self.config['questions']):
            print(question['question'])
            for m, choice in enumerate(self.config['questions'][n]['choices']):
                print(f"{m+1}) {choice['choice']}")
            print("\n")
            answer = input("Please enter which number choice you want to do: ")
            answer = int(answer) - 1

            for outcome, score in self.config['questions'][n]['choices'][answer]['impact'].items():
                self.scores[outcome] += score

        winner = self.evaluate_outcomes()

        print(f"You most closely resemble to: {winner['title']}")
        print(winner['description'])
        
    def evaluate_outcomes(self) -> str:
        max_score = max(self.scores.values())
        winning_outcomes = [outcome for outcome, score in self.scores.items() if score == max_score]

        if len(winning_outcomes) > 1:
            match self.config['tiebreaker']['tiebreaker_method']:
                case 'tiebreaker':
                    print(self.config['tiebreaker']['question'])
                    necessary_choices = [x for x in self.config['tiebreaker']['choices'] if list(x['impact'])[0] in winning_outcomes]
                    for n, choice in enumerate(necessary_choices):
                        print(f"{n+1}) {choice['choice']}")
                    print("\n")
                    answer = input("Please enter which number choice you want to do: ")
                    answer = int(answer) - 1

                    impact = necessary_choices[answer]['impact'].items()
                    outcome, score = next(iter(impact))

                    self.scores[outcome] += score
                    max_score =  max(self.scores.values())
                    winning_outcomes = [outcome for outcome, score in self.scores.items() if score == max_score]
                    
                    return self.config['outcomes'][winning_outcomes[0]]
                case 'random':
                    return random.choice(winning_outcomes) 
        return self.config['outcomes'][winning_outcomes[0]]
def main():
    quizcreate = QuizCreate(input('Enter config file: '))
    quizcreate.run()

if __name__ == "__main__":
    main()
