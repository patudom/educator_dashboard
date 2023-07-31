
import warnings
warnings.filterwarnings('ignore') # ignore warnings

from markers import markers

class State:
    markers = markers
    

    def __init__(self, story_state):
        # list story keys
        self.name = story_state['name'] # string
        self.title = story_state['title'] # string
        self.stages = {k:v['state'] for k,v in story_state['stages'].items()} #  dict_keys(['0', '1', '2', '3', '4', '5', '6'])
        self.classroom = story_state['classroom'] # dict_keys(['id', 'code', 'name', 'active', 'created', 'updated', 'educator_id', 'asynchronous'])
        self.responses = story_state['responses']
        self.mc_scoring = story_state['mc_scoring'] # dict_keys(['1', '3', '4', '5', '6'])
        self.stage_index = story_state['stage_index'] # int
        self.total_score = story_state['total_score'] #int
        self.student_user = story_state['student_user'] # dict_keys(['id', 'ip', 'age', 'lat', 'lon', 'seed', 'dummy', 'email', 'gender', 'visits', 'password', 'username', 'verified', 'last_visit', 'institution', 'team_member', 'last_visit_ip', 'profile_created', 'verification_code'])
        self.teacher_user = story_state['teacher_user'] # None
        self.max_stage_index = story_state['max_stage_index'] # int
        self.has_best_fit_galaxy = story_state['has_best_fit_galaxy'] # bool
        
    
    def get_possible_score(self):
        possible_score = 0
        for key, value in self.mc_scoring.items():
            for v in value.values():
                possible_score += 10
        return possible_score
    
    def stage_score(self, stage):
        score = 0
        possible_score = 0
        for key, value in self.mc_scoring[str(stage)].items():
            score += value['score']
            possible_score += 10
        return score, possible_score
    

    @property
    def how_far(self):
        stage_index = self.max_stage_index
        stage_markers = self.markers[str(stage_index)]
        
        frac = self.stage_fraction_completed(stage_index)
        # are we in slideshow stage
        if stage_markers is None:
            string_fmt =  "In Stage {} slideshow".format(stage_index)
        else:
            string_fmt = f"{frac:.0%} through Stage {stage_index}"
            
        return {'string': string_fmt, 'value':frac}
    
    def stage_fraction_completed(self, stage):
        markers = self.markers[str(stage)]
        
        if markers is None:
            return 1.0
        current_stage_marker = self.stages[str(stage)]['marker']
        total = len(markers)
        current = markers.index(current_stage_marker) + 1
        frac = float(current) / float(total)
        return frac
    
    def total_fraction_completed(self):
        total = []
        current = []
        for key, stage in self.stages.items():
            markers = self.markers[key]
            if markers is not None:
                total.append(len(markers))
                if self.stage_index == int(key):
                    val = markers.index(self.current_marker) + 1
                elif self.max_stage_index > int(key):
                    # if true, then stage key is complete
                    val = len(markers)
                elif self.stage_index < int(key):
                    # if false, then stage key is not complete
                    val = 0 #markers.index(stage['marker']) + 1
                current.append(val)
        # print(total, current)
        frac = int(100 * float(sum(current)) / float(sum(total)))
        return {'percent':frac, 'total':sum(total), 'current':sum(current)}
    
    @property
    def possible_score(self):
        return self.get_possible_score()
    
    @property
    def score(self):
        return self.total_score / self.possible_score
    
    
    @property
    def current_marker(self):
        return self.stages[str(self.stage_index)].get('marker')
    
    @property
    def max_marker(self):
        return self.stages[str(self.max_stage_index)].get('marker')
    
    @property
    def percent_completion(self):
        return self.total_fraction_completed()['percent']
    
    
# create a wrapper class StateList that can be used to create a list of State objects
# and getattr to get the attributes of the State object
class StateList():
    
    def __init__(self, list_of_states):
        self.states = [State(state) for state in list_of_states]
    
    def __getattribute__(self, __name):
        try:
            return object.__getattribute__(self, __name)
        except AttributeError:
            if __name == 'student_id' or __name == 'id':
                return [state.student_user['id'] for state in self.states]
            return [getattr(state, __name) for state in self.states]

