import dill
import pandas as pd
import warnings
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC


warnings.filterwarnings("ignore")


def filter_data(columns_to_drop):
    """Удаление столбцов из списка"""
    def wrapper(df):
        return df.drop(columns_to_drop, axis=1)
    
    return wrapper

def remove_outliers(data):
    """Замена выбросов столбца year"""
    new_data = data.copy()
    
    col = 'year'
    q25 = data[col].quantile(0.25)
    q75 = data[col].quantile(0.75)
    iqr = q75 - q25
    boundaries = [round(q25 - 1.5 * iqr), round(q75 + 1.5 * iqr)]
    boundaries[0] = max(data[col].min(), boundaries[0])
    boundaries[1] = min(data[col].max(), boundaries[1])
    
    new_data.loc[new_data[col] < boundaries[0], col] = boundaries[0]
    new_data.loc[new_data[col] > boundaries[1], col] = boundaries[1]
    return new_data

def short_model(x):
    if not pd.isna(x.model):
        return x.model.lower().split(' ')[0]
    else:
        return x.model

def age_category(x):
    if x.year > 2013:
        return 'new'
    elif x.year < 2006:
        return 'old'
    
    return 'average'

def add_column(name, f):
    """Добавление столбца name из преобразования f над строками data"""
    def wrapper(data):
        new_data = data.copy()
        new_data[name] = new_data.apply(f, axis=1)
        return new_data
    
    return wrapper


def main():
    df = pd.read_csv('data/homework.csv')
    
    columns_to_drop = [
        'id',
        'url',
        'region',
        'region_url',
        'price',
        'manufacturer',
        'image_url',
        'description',
        'posting_date',
        'lat',
        'long'
    ]
    
    # Вспомогательные пайплайны для заполнения пропусков и нормализации данных
    nums_transform = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])
    cats_transform = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    data_transform = ColumnTransformer(transformers=[
        ('numerical', nums_transform, make_column_selector(dtype_include='number')),
        ('categorical', cats_transform,
         make_column_selector(dtype_include=['object', 'category']))
    ])
    
    # Основной пайплайн предобработки данных
    preprocessor = Pipeline(steps=[
        ('prefilter', FunctionTransformer(filter_data(columns_to_drop))),
        ('outliers_remover', FunctionTransformer(remove_outliers)),
        ('add_age_category', FunctionTransformer(
            add_column('age_category', age_category))),
        ('add_short_model', FunctionTransformer(
            add_column('short_model', short_model))),
        ('transform_data', data_transform)
    ])
    
    X = df.drop(['price_category'], axis=1)
    y = df['price_category']
    
    # Инициализируем модели
    models = (
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        SVC()
    )
    
    best_score = 0
    best_pipe = None
    for model in models:
        pipe = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        score = cross_val_score(pipe, X, y, cv=4, scoring='accuracy', n_jobs=-1)
        print(f'Model {type(model).__name__}. '
              f'Score_mean: {score.mean():.4f}. '
              f'Score_std: {score.std():.4f}')
        
        if score.mean() > best_score:
            best_score = score.mean()
            best_pipe = pipe
    
    print(f'Model {type(best_pipe.named_steps["classifier"]).__name__}. '
          f'Score_mean: {best_score:.4f}.')
    with open('pipe.pkl', 'wb') as f:
        best_pipe.fit(X, y)
        dill.dump(best_pipe, f)
    
if __name__ == '__main__':
    main()
