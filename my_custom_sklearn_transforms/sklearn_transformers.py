from sklearn.base import BaseEstimator, TransformerMixin


# All sklearn Transforms must have the `transform` and `fit` methods
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        # Retornamos um novo dataframe sem as colunas indesejadas
        return data.drop(labels=self.columns, axis='columns')

class TratamentoNulos(BaseEstimator, TransformerMixin):
    def __init__(self, desvio=1):
        # Recebe o numero de vezes que vai ser aplicado no desvio padrao, para somar a media
        self.desvio = desvio
        self.variavies_com_nulos = 0
        
    def fit(self, df, y=None):
        df_analise_nulos = df.isna().sum()
        self.variaveis_com_nulos = df_analise_nulos[df_analise_nulos > 0].index
        return self

    def transform(self, df):
        if len(self.variaveis_com_nulos) > 0:
            i = 0
            while i < len(self.variaveis_com_nulos):
                media = (df[self.variaveis_com_nulos[i]].mean() + 
                         df[self.variaveis_com_nulos[i]].std()*(self.desvio))
                print("\n\nSubstituindo nulos na variável: ", self.variaveis_com_nulos[i], " por: ", media, "\n\n")
                df = df.apply(self.SubValue_const, args=(media, self.variaveis_com_nulos[i]), axis=1)
                i += 1
        return df
    
    def SubValue_const(self, x, const, var_nula):
        if pd.isna(x[var_nula]):
            x[var_nula] = const
        return x