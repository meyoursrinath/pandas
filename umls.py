import pandas as pd
from sqlalchemy import create_engine


umls_main_1 = pd.read_csv('SemanticType_LastCHD1.csv')
umls_main_2 = pd.read_csv('SemanticType_LastCHD2.csv')
umls_main_full = pd.concat([umls_main_1, umls_main_2])
disorders = pd.read_csv('Disorders.csv')
chem_drugs = pd.read_csv('Chemicals and Drugs.csv')

# merged_with_disorders = pd.merge(left=umls_main_full, right=disorders, left_on='STY', right_on='Type 1')
merged_with_chem_drugs = pd.merge(left=umls_main_full, right=chem_drugs, left_on='STY', right_on='Type 1')
# print len(merged_with_disorders)
# print len(merged_with_chem_drugs)
engine = create_engine('mysql+mysqldb://sherlock:z00mrxr0cks!@69.164.196.100:3306/metathesaurus', echo=False)
con = engine.connect()
print "Converting to SQL"
merged_with_chem_drugs.to_sql(con=con, name='Chemicals and Drugs', if_exists='replace')
con.close()

'''
SELECT B.STY, B.STY2, A.CUI, A.LUI, A.SUI, A.STT, A.TS, A.ISPREF, A.SAB, A.STR FROM
MRCONSO AS A INNER JOIN Disorders AS B
WHERE A.CUI = B.CUI
GROUP BY A.SUI
ORDER BY A.CUI;

SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
'''
