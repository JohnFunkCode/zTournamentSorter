import pandas as pd
import numpy as np

#index = ['a', 'b']
#columns = ['one', 'two', 'three']
#data = [(1,2.,'Hello'), (2,3.,"World")]
#print data

columns=['index','First Name','Last Name','Gender','Dojo','Age','Rank','Feet','Inches','Height','Weight','BMI','Events','Weapons']
data=[(255,'Lucas','May','Male','CO- Parker',10,'Yellow',4,3,'4 ft. 3 in.',52,154,'2 Events - Forms & Sparring ($75)','None'),
      (194,'jake','coleson','Male','CO- Cheyenne Mountain',10,'Yellow',4,0,'4',60,156,'2 Events - Forms & Sparring ($75)','Weapons ($35)'),
      (195,'katie','coleson','Female','CO- Cheyenne Mountain',12,'Yellow',4,0,'4',65.161,'2 Events - Forms & Sparring ($75)','Weapons ($35)')]
df=pd.DataFrame(data,columns=columns)
print df

# create a test data frame
#index = ['a', 'b', 'c', 'd']
#columns = ['one', 'two', 'three', 'four']
#df = pd.DataFrame(np.random.randn(4, 4), index=index, columns=columns)
#data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

