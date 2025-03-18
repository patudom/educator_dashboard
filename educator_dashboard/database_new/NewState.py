import warnings
warnings.filterwarnings('ignore') # ignore warnings
from .markers import stage_marker_counts

from numpy import nan, mean
from typing import Dict, List, Optional, Union, Any

from .types import ProcessedStage, ProcessedMCScore

from ..logger_setup import logger

class State:
    # markers = markers
    

    def __init__(self, story_state):
        # list story keys
        self.story_state = story_state
        self.title = story_state.get('title','') # string
        self.stages: Dict[str, ProcessedStage] = {k: v['state'] for k, v in story_state['stages'].items()}
        self.responses: Dict[str, Dict[str, str]] = story_state.get('responses',{})
        self.mc_scoring: Dict[str, Dict[str, ProcessedMCScore]] = story_state.get('mc_scoring',{}) # dict_keys(['1', '3', '4', '5', '6'])
        self.has_best_fit_galaxy = story_state.get('has_best_fit_galaxy',False) # bool
        self.student_id = story_state.get('student_id',None) # string
        self.stage_map: Dict[int, str] = {v['index']: k for k, v in self.stages.items()}
        self.last_route = story_state.get('last_route','')  
    
    def get_possible_score(self) -> int:
        possible_score = 0
        for key, value in self.mc_scoring.items():
            for v in value.values():
                possible_score += 10
        return possible_score
    
    def get_stage_score(self, stage) -> tuple[int, int]:
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
    def stage_names(self) -> List[str]:
        # 
        return list(self.stages.keys())
    
    def stage_name_to_index(self, name: str) -> Optional[int]:
        # 
        d = {v:k for k, v in self.stage_map.items()}
        return d.get(name, None)
    
    # furthest stage reached by student
    @property
    def max_stage_index(self) -> int:
        i = 0
        names = list(self.stages.keys())
        for k in names:
            if len(self.stages[k].keys()) == 1:
                continue
            i = max(i, self.stages[k].get('index',0))
        # logger.debug(f"Max stage index: {i}")
        # logger.debug(names)
        return i
    
    
    
    @property
    def how_far(self) -> Dict[str, Union[str, float]]:
        # 
        if self.max_stage_index is nan:
            return {'string': 'No stage index', 'value':0.0}
        if self.max_stage_index in self.stage_map.keys():
            stage_name = self.stage_map[self.max_stage_index]
        else:
            stage_name = self.stage_map[1] # 1 is the key name
        
        frac = self.stage_fraction_completed(stage_name)
        string_fmt = f"{frac:.0%} through Stage {stage_name}"
            
        return {'string': string_fmt, 'value':frac or nan}
    
    @property
    def stage_index(self) -> int:
        return self.max_stage_index + 1
    
    
    
    def stage_fraction_completed(self, stage_name: str) -> Optional[float]:
        if stage_name is None:
            return None
        
        if stage_name not in self.stages:
            logger.debug(f"Stage {stage_name} not in stages")
            return None
        
        if stage_name in self.stages.keys():
            if 'progress' in self.stages[stage_name]:
                return self.stages[stage_name]['progress']
            else:
                return 0.0
        
    def total_fraction_completed(self) -> Dict[str, Union[float, int]]:
        # 
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
    def possible_score(self) -> int:
        return self.get_possible_score()
    
    @property
    def story_score(self) -> int:
        total = 0
        for key in self.stages.keys():
            score, _ = self.get_stage_score(key)
            total += score
        return total
    
    # current stage student is in
    @property
    def current_stage_index(self) -> int:
        if self.last_route is None or self.last_route == '' or self.last_route == '/':    
            return 0
        else:
            val = ''.join([c for c in self.last_route if c.isdigit()])
            try:
                return int(val)    
            except:
                raise ValueError(f"Could not convert {val} to an integer")    
    
    # the current location of the student
    @property
    def current_marker(self) -> Union[str, float]:
        if self.current_stage_index in self.stage_map.keys():
            key = self.stage_map[self.current_stage_index]
            if key not in self.stages or 'current_step' not in self.stages[key]:
                return nan
            return self.stages[key].get('current_step',None) or 0
        else:
            return nan
    
    # the maximum position reached by the student
    @property
    def max_marker(self) -> Union[str, float, int]:
        if self.max_stage_index in self.stage_map.keys():
            key = self.stage_map[self.max_stage_index]
            if key not in self.stages or 'max_step' not in self.stages[key]:
                return nan
            return self.stages[key].get('max_step',None) or 0
        elif self.max_stage_index == 0:
            return 1
        else:
            return nan
    
    @property
    def percent_completion(self) -> float:
        return self.total_fraction_completed()['percent']
