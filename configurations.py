############### SCHEMA ###############
TARGET = 'is_engaged'

CATEGORICAL_FEATRUES = [
   'campaign_id',
   'part_of_day',
   'part_of_week',
   'part_of_month',
   'seniority',
   'country',
   'state',
   'managment_level',
   'company_size',
   'linkedin_industry'
]


FEATRURES_TO_IGNORE_WHILE_TRAIN = [
    'company_id',
    'contact_id',
    'event'
]


EXPLODE_FEATURES_ENGINEERING = [
    'function'
]

############### TRAIN TEST SPLIT ###############
TEST_DATASET_SHARE = 0.2
RANDOM_STATE = 0 
CROSS_VALIDATION_FOLDS = 3 
HYPERPARAM_ROUNDS = 30
MODEL_PARAMS = {
    'n_estimators': [150, 250, 350],
    'learning_rate': [0.05,0.1,0.2],
    'max_depth': [5,7],
    'subsample': [0.5,0.65,0.8],
    'colsample_bytree': [0.75,0.85],
    'colsample_bylevel': [0.85, 1],
    'alpha': [0.3,0.5,1,1.5],
    'random_state': [0],
    'objective': ['binary:logistic']#,
}

FIT_PARAMS = {
    "early_stopping_rounds": 30, 
    "eval_metric" : ['logloss', 'aucpr']
}