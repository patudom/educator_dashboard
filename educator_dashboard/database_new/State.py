
import warnings
warnings.filterwarnings('ignore') # ignore warnings
stage_name_list = ['introduction','spectra_&_velocity', 'distance_introduction', 'distance_measurements', 'explore_data', 'class_results_and_uncertainty', 'professional_data']
from .markers import stage_marker_counts

from numpy import nan, mean


class State:
    # markers = markers
    

    def __init__(self, story_state,):
        # list story keys
        self.name = story_state.get('name','') # string
        self.title = story_state.get('title','') # string
        self.stages = {k: v['state'] for k, v in story_state['stages'].items()}
        self.responses = story_state.get('responses',{})
        self.mc_scoring = story_state.get('mc_scoring',{}) # dict_keys(['1', '3', '4', '5', '6'])
        # self.stage_index = story_state.get('stage_index',nan) # int
        self.has_best_fit_galaxy = story_state.get('has_best_fit_galaxy',False) # bool
        self.student_id = story_state.get('student_id',None) # string
        
        
    
    def get_possible_score(self):
        possible_score = 0
        for key, value in self.mc_scoring.items():
            for v in value.values():
                possible_score += 10
        return possible_score
    
    def get_stage_score(self):
        score = 0
        possible_score = 0

        for key, value in self.mc_scoring['scores'].items():
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
        for k, v in self.stages.items():
            if v is not None:
                i+=1
        return i
    
    @property
    def how_far(self):

        if self.max_stage_index is nan:
            return {'string': 'No stage index', 'value':0.0}
        stage_name = stage_name_list[self.max_stage_index]
        
        frac = self.stage_fraction_completed(stage_name)
        string_fmt = f"{self.student_id} {frac:.0%} through Stage {stage_name}"
            
        return {'string': string_fmt, 'value':frac}
    
    @property
    def stage_index(self):
        return self.max_stage_index + 1
    
    def get_stage_index(self, s):
        return stage_name_list.index(s) if s in stage_name_list else None
    
    def stage_fraction_completed(self, stage_name):
        stage_index = self.get_stage_index(stage_name)
        if stage_index is None:
            return nan
        
        num_markers = stage_marker_counts[stage_index]
        
        if num_markers == 0:
            # print(f"{self.student_id} stage_fraction_completed: Stage {stage_name} has no markers")
            return nan
        if self.stages[stage_name] is None:
            print(f"{self.student_id} stage_fraction_completed: Stage {stage_name} has no state")
            if stage_marker_counts[stage_index] == 0:
                return nan
            else:
                return 0.0
        
        current_stage_index = self.stages[stage_name].get('current_step', None)
        
        if current_stage_index is None:
            return nan
        current = current_stage_index + 1
        frac = float(current) / float(num_markers)
        return frac
    
    def total_fraction_completed(self):
        total = []
        current = []
        for k, stage in self.stages.items():
            # stage_index = stage_name_list.index(k) if k in stage_name_list else None
            # if stage_index is not None and stage is not None:
            #     num_markers = stage_marker_counts[stage_index]
            #     total.append(num_markers)
            #     try:
            #         current.append(stage['current_step']+1)
            #     except KeyError:
            #         # print(f"{self.student_id} total_fraction_completed: Stage {k} has no current_marker", stage)
            #         current.append(num_markers)
            # else:
            #     # print(f"{self.student_id} total_fraction_completed: Stage {k} not in stage_name_list")
            #     pass
            frac = self.stage_fraction_completed(k)
            current.append(frac if frac is not nan else 1.0)
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
        score, _ = self.get_stage_score()
        return score
    
    @property
    def current_marker(self):
        key = stage_name_list[self.max_stage_index]
        if self.stages[key] is None:
            return nan
        return self.stages[key].get('current_step',0)
    
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

