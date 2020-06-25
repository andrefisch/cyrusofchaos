class School(object):
    def __init__(self,
                 name,
                 num_fencers,
                 wins,
                 remaining_bouts,
                 total_bouts,
                 school_logo=None):
        self.name = name
        self.num_fencers = num_fencers
        self.wins = wins
        self.remaining_bouts = remaining_bouts
        self.total_bouts = total_bouts
        self.school_logo = school_logo

    def will_finish_higher(self, other_school):
        return (self.wins - other_school.wins) > other_school.remaining_bouts

    def wins_to_clinch_over(self, other_school):
        return other_school.remaining_bouts - (self.wins - other_school.wins) + 1

    @property
    def has_bouts_remaining(self):
        return self.remaining_bouts > 0

    @property
    def win_percent(self):
        # print (self.name, self.wins, self.total_bouts, self.remaining_bouts)
        return "{:.1%}".format(float(self.wins) / (self.total_bouts - self.remaining_bouts))
