# scores/models.py

import csv
import os
from django.conf import settings
from encron.tools import find_file

#CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'scores_data.csv')
CSV_FILE_PATH=find_file('live_data.csv')

class Score:
    def __init__(self, id, teams_status, score1, score2):
        self.id = str(id)
        self.teams_status = teams_status
        self.score1 = int(score1)
        self.score2 = int(score2)

    @classmethod
    def get_all_scores(cls):
        scores = []
        if not os.path.exists(CSV_FILE_PATH):
            return scores
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    continue  # Skip malformed rows
                scores.append(cls(*row))
        return scores

    @classmethod
    def get_score_by_id(cls, score_id):
        scores = cls.get_all_scores()
        for score in scores:
            if score.id == str(score_id):
                return score
        return None

    @classmethod
    def save_all_scores(cls, scores):
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for score in scores:
                writer.writerow([score.id, score.teams_status, score.score1, score.score2])

    def to_list(self):
        return [self.id, self.teams_status, self.score1, self.score2]
