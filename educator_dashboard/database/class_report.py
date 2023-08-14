

import pandas as pd
from .nested_dataframe import flatten
from .State import State, StateList
from .Query import QueryCosmicDSApi

HUBBLE_ROUTE_PATH = "hubbles_law"

import astropy.units as u
from math import nan
class Roster():
    
    def __init__(self, class_id = None):
        
        self._mc_questions = None
        self._fr_questions = None
        self._data = None
        self._report = None
        self._short_report = None
        
        self._refresh = False
        
        self.class_id = class_id
        self.query = QueryCosmicDSApi(class_id = class_id, story=HUBBLE_ROUTE_PATH)
        self.data = None
        self.class_summary = None
        self.grab_data()
        
    def grab_data(self):
        print('Getting roster')
        self.roster = self.query.get_roster()
        self.data = None
        
        if len(self.roster) == 0:
            self.student_id = []
            self.story_name = ''
            self.story_state = {}
            self.stages = []
            self.new_story_state = StateList([])
            self.last_modified = ''
            self.stage_index = 0
            return
        keys = self.roster[0].keys()
        new_out = self.l2d(self.roster)
        keys = new_out.keys()
        for key in keys:
            if isinstance(new_out[key][0],dict):
                new_out[key] = self.l2d(new_out[key])
            elif isinstance(new_out[key],list):
                new_out[key] = {key:new_out[key]}
            else:
                print(key, type(new_out[key][0]))
        
        self.student_id = new_out['student_id']
        self.story_name = new_out['story_name']
        self.story_state = new_out['story_state']
        
        
        keys = self.l2d(self.story_state['stages']).keys()
        self.stages = []
        def getstate(stage):
            if isinstance(stage, dict) and ('state' in stage.keys()):
                return stage['state']
            else:
                print(f'no state in class {self.class_id}')
                return {'stage':{}, 'marker':None, 'responses':[], 'mc_scores':[], 'total_score':0, 'state':{}, 'title': None}
        for key in sorted(keys):
            self.stages.append([getstate(s)  for s in self.l2d(self.story_state['stages'])[key]])
        
        
        self.new_story_state = StateList([student['story_state'] for student in self.roster])
        self.last_modified = new_out['last_modified']
        self.stage_index = self.new_story_state.stage_index
        
        
        
        
        
        
        
        # mc_scores = self.l2d(self.story_state['mc_scores'])
        
        # df = pd.DataFrame.from_dict(self.students).set_index('student_id')
    

    @staticmethod
    def list_of_dicts_to_dict_of_lists(list_of_dicts, fill_val = None):
        keys = list_of_dicts[0].keys()
        dict_of_lists = {k: [o[k] if k in o.keys() else fill_val for o in list_of_dicts] for k in keys}
        return dict_of_lists
    
    def l2d(self, list_of_dicts, fill_val = None):
        return self.list_of_dicts_to_dict_of_lists(list_of_dicts, fill_val)
    
    def get_class_data(self, refresh = False):
        if self.data is None or self._refresh or refresh:
            self.data = self.query.get_class_data(class_id = self.class_id)
        return self.data

    def get_class_summary(self, refresh = False):
        if self.class_summary is None or self._refresh or refresh:
            measurements = self.measurements(refresh = refresh) 
            def get_slope(x, y):
                # slope through origin
                return nan if (sum(x**2) == 0) else (sum(x*y)/sum(x**2))
            def slope2age(h0):
                return (1/(h0 * u.km/u.s/u.Mpc)).to(u.Gyr).value
            H0 = []
            Age = []
            for student in self.student_ids:
                student_data = measurements[measurements['student_id'] == student]
                if len(student_data) == 5:
                    H0.append(get_slope(student_data['est_dist_value'], student_data['velocity_value']))
                    Age.append(slope2age(H0[-1]))
                else:
                    H0.append(nan)
                    Age.append(nan)
            self.class_summary = self.make_dataframe(pd.DataFrame({'H0':H0, 'age':Age}))

        return self.class_summary
    
    def get_student_by_id(self, student_id):
        if student_id not in self.student_ids:
            print(f'{student_id} not in roster')
            return None
        return [student for student in self.roster if student['student_id'] == student_id][0]
    
    def make_dataframe(self, dictionary, include_student_id = True, include_class_id = True, include_username = True):
        # take the dictionary and make a dataframe
        # add self.student_ids as a column
        
        if 'student_id' not in dictionary.keys() and include_student_id:
            dictionary['student_id'] = self.student_ids
        if 'class_id' not in dictionary.keys() and include_class_id:
            dictionary['class_id'] = self.class_id
        if 'username' not in dictionary.keys() and include_username:
            dictionary['username'] = self.students['username'].values
        # if isinstance(dictionary, pd.DataFrame):
        #     return dictionary.set_index('student_id')
        
        # add cols conditionally on inclusion
        first_cols = []
        if include_student_id:
            first_cols.append('student_id')
        if include_class_id:
            first_cols.append('class_id')
        if include_username:
            first_cols.append('username')
        
        cols = first_cols + [col for col in dictionary.keys() if col not in first_cols]
        dictionary = {k:dictionary[k] for k in cols}
        # df = pd.DataFrame(dictionary).set_index('student_id')
        return pd.DataFrame(dictionary)
    

    def measurements(self, refresh = False):
        if len(self.roster) > 0:
            if self.data is None or refresh:
                out = self.get_class_data(refresh = refresh)
            else: 
                out = self.data
            return pd.DataFrame(out)
    
    
    def multiple_choice_questions(self):
        if (self._mc_questions is not None) and (not self._refresh):
            return self._mc_questions
        if len(self.roster) > 0:
            out = self.l2d(self.story_state['mc_scoring'])
            out.update({'student_id':self.student_ids})
            self._mc_questions = out
            return out
        else:
            return {'student_id': self.student_ids}
    
    def free_response_questions(self):
        if (self._fr_questions) is not None and (not self._refresh):
            return self._fr_questions
        
        if len(self.roster) > 0:
            out = self.l2d(self.story_state['responses'])
            out.update({'student_id':self.student_ids})
            self._fr_questions = out
            return out
        else:
            return {'student_id': self.student_ids}
    
    def questions(self):
        fr = self.free_response_questions()
        mc = self.multiple_choice_questions()
        df_fr = flatten(self.make_dataframe(fr, include_class_id=False, include_username=False))
        df_mc = flatten(self.make_dataframe(mc, include_class_id=False, include_username=False))
        return pd.merge(df_mc, df_fr, how='left', on='student_id')
    
    
    @property
    def student_ids(self):
        if len(self.roster) > 0:
            return [student['student_id'] for student in self.roster]
        else:
            return []
    
    @property
    def responses(self):
        if len(self.roster) > 0:
            df = pd.DataFrame([student['story_state']['responses'] for student in self.roster])
            return self.make_dataframe(flatten(df))
        else:
            return self.make_dataframe(pd.DataFrame())
    
    
    @property
    def students(self):
        if len(self.roster) > 0:
            students = self.l2d([student['student'] for student in self.roster])
            return self.make_dataframe(students)
        else:
            return pd.DataFrame({'student_id':[], 'username':[], 'class_id':[]})
    
    @property
    def out_of(self):
        if len(self.roster) == 0:
            return
        out_of = []
        for mc_score in self.story_state['mc_scoring']:
            if mc_score is None or (len(mc_score) == 0):
                out_of.append(0)
                continue
            num = 0
            for key, val in mc_score.items():
                num += len(val)
            out_of.append(num * 10)
        return out_of
    
    def fraction_completed(self):
        # for each stage, create a state object using their story_state
        how_far = []
        tot_perc = []
        for student in self.roster:
            state = State(student['story_state'])
            how_far.append(state.how_far)
            tot_perc.append(state.percent_completion)
        return self.l2d(how_far)['string'], tot_perc
    
    def report(self):
        "refreshing data"
        
        if self._report is not None and not self._refresh:
            return self._report
        
        if self._refresh:
            self.grab_data()

        roster = self
        if len(roster.roster) == 0:
            return None
        if hasattr(roster,'stages'):
            data = [[s.get('marker',None) for s in stage] for stage in roster.stages]
            cols = ['Stage 1 marker', 'Stage 3 marker', 'Stage 4 marker', 'Stage 5 marker', 'Stage 6 marker']
            c1 = {k:v for k,v in zip(cols, data)}
            df = pd.DataFrame(c1)
            df['student_id'] = roster.student_id['student_id']
        else:
            df = pd.DataFrame({'student_id':roster.student_id['student_id']})
       
        data = [[s.get('marker',None) for s in stage] for stage in roster.stages]
        cols = ['Stage 1 marker', 'Stage 3 marker', 'Stage 4 marker', 'Stage 5 marker', 'Stage 6 marker']
        c1 = {k:v for k,v in zip(cols, data)}
        
        df = pd.DataFrame(c1)
        df['student_id'] = roster.student_id['student_id']
        # add a string column containing roster.students['username']
        df['username'] = roster.students['username'].values
        df['class_id'] = roster.class_id
        completion_string, completion_percent = roster.fraction_completed()
        df['progress'] = completion_string
        df['percent_story_complete'] = completion_percent
        # df['percent_story_complete'] = df['percent_story_complete'].apply(lambda x: int(x))
        df['max_stage_index'] = roster.new_story_state.max_stage_index
        df['max_stage_marker'] = roster.new_story_state.max_marker
        df['stage_index'] = roster.stage_index
        df['total_score'] = roster.story_state['total_score']
        df['out_of_possible'] = roster.out_of
        summ = roster.get_class_summary()
        df['Hubble_Constant'] = summ['H0'].apply(lambda x: round(x,2))
        df['Age'] = summ['age'].apply(lambda x: round(x,2))
        
        response = flatten(pd.DataFrame(roster.story_state['responses']))
        response['student_id'] = roster.student_id['student_id']
        df = df.merge(response, on='student_id', how='left')
        last_modified = pd.to_datetime(roster.last_modified['last_modified']).tz_convert('US/Eastern').strftime("%Y-%m-%d %H:%M:%S (Eastern)") # in Easterm time
        df['last_modified'] = last_modified
        
        self._report = df
        
        return df
    
    def short_report(self):
        if self._short_report is not None and not self._refresh:
            return self._short_report
        
        if self._refresh:
            self.grab_data()
        
        roster = self
        if len(roster.roster) == 0:
            return None
        if hasattr(roster,'stages'):
            data = [[s.get('marker',None) for s in stage] for stage in roster.stages]
            cols = ['Stage 1 marker', 'Stage 3 marker', 'Stage 4 marker', 'Stage 5 marker', 'Stage 6 marker']
            c1 = {k:v for k,v in zip(cols, data)}
            df = pd.DataFrame(c1)
            df['student_id'] = roster.student_id['student_id']
        else:
            df = pd.DataFrame({'student_id':roster.student_id['student_id']})

        # add a string column containing roster.students['username']
        df['username'] = roster.students['username'].values
        df['class_id'] = roster.class_id
        completion_string, completion_percent = roster.fraction_completed()
        df['progress'] = completion_string
        df['percent_story_complete'] = completion_percent
        # df['percent_story_complete'] = df['percent_story_complete'].apply(lambda x: int(x))
        df['max_stage_index'] = roster.new_story_state.max_stage_index
        df['max_stage_marker'] = roster.new_story_state.max_marker
        df['stage_index'] = roster.stage_index
        df['total_score'] = roster.story_state['total_score']
        df['out_of_possible'] = roster.out_of
        summ = roster.get_class_summary()
        df['Hubble_Constant'] = summ['H0'].apply(lambda x: round(x,2))
        df['Age'] = summ['age'].apply(lambda x: round(x,2))

        last_modified = pd.to_datetime(roster.last_modified['last_modified']).tz_convert('US/Eastern').strftime("%Y-%m-%d %H:%M:%S (Eastern)") # in Easterm time
        df['last_modified'] = last_modified
        
        self._short_report = df
        
        return df
    
    def refresh_data(self):
        self._refresh = True
        print('****** Refreshing data ******')
        print(' >>> Grabbing class states')
        self.grab_data()
        print(' >>> Getting free response questions')
        self.free_response_questions()
        print(' >>> Getting multiple choice questions')
        self.multiple_choice_questions()
        print(' >>> Getting class data')
        self.get_class_data()
        self._refresh = False



## create a cli so that will take the class_id as an argument, pass it to create report and export 
# an excel fill called class_id_class_progress.xlsx

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create a report for a class')
    parser.add_argument('class_id', type=int, help='The class id')
    # if there are multiple arguments given then loop over them 
    args = parser.parse_args()
    
    if args.class_id is None:
        print('Please provide a class id')
        exit()
    
    roster = Roster(class_id = args.class_id)
    df = roster.report()#rgs.class_id)
    df.to_excel(f'{args.class_id}_class_progress.xlsx')