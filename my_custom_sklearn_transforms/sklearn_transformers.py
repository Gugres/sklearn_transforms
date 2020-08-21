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
        
    def fit(self, df, y=None):
        df_analise_nulos = df.isna().sum()
        self.variaveis_com_nulos = df_analise_nulos[df_analise_nulos > 0].index
        return self.variaveis_com_nulos
    
    def SubValue_const(self, x, const, argumento, var_nula):
        if pd.isna(x[var_nula]) and x["PERFIL"] == argumento:
            x[var_nula] = const
        return x
    
    def transform(self, df):
        perfis = ["EXATAS", "HUMANAS", "DIFICULDADE", "MUITO_BOM", "EXCELENTE"]
        if len(self.variaveis_com_nulos) > 0:
            i = 0
            while i < len(self.variaveis_com_nulos):
                print("\n\nSubstituindo nulos na variável: ", self.variaveis_com_nulos[i], "\n\n")
                for k in perfis:
                    media = (df[df.PERFIL == k][self.variaveis_com_nulos[i]].mean() + 
                             df[df.PERFIL == k][self.variaveis_com_nulos[i]].std()*(self.desvio))
                    print("\n Substituindo nulos por: ", media, " no perfil: ", k)
                    df = df.apply(self.SubValue_const, args=(media, k, self.variaveis_com_nulos[i]), axis=1)
                i += 1
        return df