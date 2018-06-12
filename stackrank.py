import math
import random


class Voter(object):
    def __init__(self, choices):
        self.current_index = 0
        self.choices = choices

    def get_current_choice(self):
        return self.choices[self.current_index]

    def increment(self):
        assert(self.current_index + 1 < len(self.choices))
        self.current_index += 1
        return self.get_current_choice()

    def __str__(self):
        choices_cp = self.choices[:]
        choices_cp[self.current_index] = "<"+choices_cp[self.current_index]+">"
        return str(choices_cp)

    def __repr__(self):
        return self.__str__()


def read_votes(filename):
    voters = []
    for line in open(filename):
        line = line.strip()
        votes = line.split(" ")
        voters.append(Voter(votes))
    return voters


def least_votes(candidate_scores):
    """
    Returns a candidate with the least votes. Ideally you should shuffle
    the candidates so that they're in a random order, in the case of a tie.
    """
    return min(candidate_scores.items(), key=lambda t: t[1])[0]


def calculate_winners(candidates, voters):
    """
    Calculate the winners, based on the list of voters and who they voted for.
    :param candidates: List of candidate names.
    :param voters: List of voter objects.
    :return: List of winners (List will be one item if one person leads).
    """
    random.shuffle(candidates)
    num_voters = len(voters)
    vote_counts = {candidate: 0 for candidate in candidates}
    # Store the objects of people that voted for a certain candidate,
    # so that recounting is easy.
    voter_map = {candidate: [] for candidate in candidates}
    # Initialize the votes
    for voter in voters:
        current = voter.get_current_choice()
        vote_counts[current] += 1
        voter_map[current].append(voter)

    losers = set()
    current_winners = winners(vote_counts, num_voters)
    while not current_winners:
        print(vote_counts)
        loser = least_votes(vote_counts)
        losers.add(loser)
        del vote_counts[loser]
        # Recount the votes for each person who voted for the loser.
        for loser_voter in voter_map[loser]:
            while loser_voter.get_current_choice() in losers:
                loser_voter.increment()
            new_candidate = loser_voter.get_current_choice()
            vote_counts[new_candidate] += 1
            voter_map[new_candidate].append(loser_voter)
        del voter_map[loser]
        # See if there's any winners after the recount.
        current_winners = winners(vote_counts, num_voters)
    return current_winners, vote_counts


def winners(candidate_scores, num_voters):
    """
    Returns a list of all people who have 50% or more of the vote.
    Returns an empty list if nobody has 50% or more of the vote.
    """
    winners = []
    for candidate, score in candidate_scores.items():
        if score >= math.ceil(num_voters/2):
            winners.append(candidate)
    return winners


if __name__ == "__main__":
    # Assumption - all voters can fit in memory.
    # Assumption - lots of voters, few candidates.
    # Assumption - everyone has to rank every candidate.
    candidates = ["A", "B", "C", "D"]
    voters = read_votes("votes.txt")
    winners, counts = calculate_winners(candidates, voters)
    if len(winners) > 1:
        print("There is a tie! Winners are: " + str(winners))
    else:
        print("Winner: " + winners[0])
    print(counts)
