import pandas as pd
from sqlalchemy import create_engine

CUI = pd.read_csv('xml_data_map.csv', encoding='base')

print len(CUI)
engine = create_engine('mysql+mysqldb://sherlock:z00mrxr0cks!@69.164.196.100:3306/dailymed?charset=utf8', encoding='utf-8', echo=False)
con = engine.connect()
print "Converting to SQL"
CUI.to_sql(con=con, name='dailymed_records', if_exists='replace', index=False)
con.close()

'''
SELECT B.STY, B.STY2, A.CUI, A.LUI, A.SUI, A.STT, A.TS, A.ISPREF, A.SAB, A.STR FROM
MRCONSO AS A INNER JOIN Disorders AS B
WHERE A.CUI = B.CUI
GROUP BY A.SUI
ORDER BY A.CUI;

SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
GRANT ALL PRIVILEGES ON dailymed.* TO 'sherlock'@'%';
FLUSH PRIVILEGES;
'''
