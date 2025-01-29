
import warnings
warnings.filterwarnings('ignore') # ignore warnings
from .markers import stage_marker_counts

from numpy import nan, mean

class State:
    # markers = markers
    

    def __init__(self, story_state):
        # list story keys
        self.story_state = story_state
        self.title = story_state.get('title','') # string
        self.stages = {k: v['state'] for k, v in story_state['stages'].items()}
        self.responses = story_state.get('responses',{})
        self.mc_scoring = story_state.get('mc_scoring',{}) # dict_keys(['1', '3', '4', '5', '6'])
        self.has_best_fit_galaxy = story_state.get('has_best_fit_galaxy',False) # bool
        self.student_id = story_state.get('student_id',None) # string
        self.stage_map = {v['index']: k for k, v in self.stages.items()}
        self.last_route = story_state.get('last_route','')  
    
    def get_possible_score(self):
        possible_score = 0
        for key, value in self.mc_scoring.items():
            for v in value.values():
                possible_score += 10
        return possible_score
    
    def get_stage_score(self, stage):
        score = 0
        possible_score = 0
        if str(stage) not in self.mc_scoring:
            return score, possible_score
        
        for key, value in self.mc_scoring[str(stage)].items():
            if value is None:
                score += 0
            else:
                v = value.get('score',0)
                if v is None:
                    score += 0
                else:
                    score += v
            # score += (value.get('score',0) or 0)
            
            possible_score += 10
        return score, possible_score
    
    @property
    def max_stage_index(self):
        i = 0
        names = list(self.stages.keys())
        for k in names:
            if len(self.stages[k].keys()) == 1:
                continue
            i = max(i, self.stages[k].get('index',0))
        print(f"Max stage index: {i}")
        print(names)
        return i
    
    @property
    def how_far(self):

        if self.max_stage_index is nan:
            return {'string': 'No stage index', 'value':0.0}
        stage_name = self.stage_map[self.max_stage_index]
        
        frac = self.stage_fraction_completed(stage_name)
        string_fmt = f"{frac:.0%} through Stage {stage_name}"
            
        return {'string': string_fmt, 'value':frac}
    
    @property
    def stage_index(self):
        return self.max_stage_index + 1
    
    
    
    def stage_fraction_completed(self, stage_name):
        if stage_name is None:
            return None
        
        if stage_name not in self.stages:
            print(f"Stage {stage_name} not in stages")
            return None
        
        if stage_name in self.stages.keys():
            if 'progress' in self.stages[stage_name]:
                return self.stages[stage_name]['progress']
            else:
                return 0.0
        
    def total_fraction_completed(self):
        total = []
        current = []
        for k, _ in self.stages.items():
            frac = self.stage_fraction_completed(k)
            if frac is None:
                frac = 1.0
            current.append(frac)
            total.append(1.0)
        
        if float(sum(total)) == 0.0:
            frac = nan
        else:
            frac = int(100 * float(sum(current)) / float(sum(total)))
        return {'percent':frac, 'total':sum(total), 'current':sum(current)}
    
    @property
    def possible_score(self):
        return self.get_possible_score()
    
    @property
    def story_score(self):
        total = 0
        for key in self.stages.keys():
            score, _ = self.get_stage_score(key)
            total += score
        return total
    
    @property
    def current_stage_index(self):
        if self.last_route is None or self.last_route == '':    
            return 0
        else:
            val = ''.join([c for c in self.last_route if c.isdigit()])
            try:
                return int(val)    
            except:
                raise ValueError(f"Could not convert {val} to an integer")    
    
    @property
    def current_marker(self):
        if self.current_stage_index in self.stage_map.keys():
            key = self.stage_map[self.current_stage_index]
            if key not in self.stages or 'current_step' not in self.stages[key]:
                return nan
            return self.stages[key].get('current_step',0)
        else:
            return nan
    
    @property
    def max_marker(self):
        return self.current_marker
        # return self.stages.get(str(self.max_stage_index),{}).get('marker','none')
    
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

