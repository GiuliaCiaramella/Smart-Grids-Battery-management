import pandas
import numpy as np
import matplotlib.pyplot as plt
# import xlrd
pNom = 1000
eNom=1000
eff=0.9
time=0.25
socMax = 0.9
socMin=0.1
socInit = 0.5

p1=[]
col_names = ["Load", "generation"]
data = pandas.read_excel('Load_Gen_Profiles.xlsx', skiprows=1, names=col_names)

load = data.Load.tolist()
pv = data.generation.tolist()

for generated, used in zip(pv,load):
    p1.append(generated-used)

# ------------------------- STEP 1 ------------------------
# se p1>0 carico la batteria senno la scarico
p2 = []
for element in p1:
    if element>0:
        if element> pNom:
            p2.append(pNom)
        else:
            p2.append(element)
    else:
        if abs(element)>pNom:
            p2.append(-pNom)
        else:
            p2.append(element)

# -----------STEP 2: CHECKING THE SOC-------------------------
soc = [0]*(len(p1)+1)
soc[0]=0.5

current_soc = soc[0]
for i in range(len(p1)):
    current_soc=soc[i]
    if current_soc > socMax and p1[i]>0:
        p2[i]=0
        next_soc = current_soc

    elif current_soc < socMin and p1[i] < 0:
        p2[i] = 0
        next_soc = current_soc
    else:
        if p1[i]>0:
            next_soc = current_soc + (abs(p2[i]) * eff * time) / eNom
        else:
            next_soc = current_soc - (abs(p2[i]) * time) / eNom * eff

        if next_soc>socMax:
            next_soc=socMax
        elif next_soc<socMin:
            next_soc=socMin

    soc[i] = current_soc
    soc[i + 1] = next_soc

x = np.arange(len(p1)+1)
state_of_charge=[]
for element in soc:
    state_of_charge.append(element*100)

label = (np.arange(0,100,4))
x_label=[]
for element in label:
    x_label.append(element/4)

plt.plot(x, state_of_charge)
# plt.xticks(label, rotation='vertical')
plt.yticks(np.arange(0,100,10))
plt.xticks(label,x_label, rotation='vertical')

plt.grid(b = True,which='major', axis='both')
plt.title("Battery state of charge vs time")
plt.xlabel("Day time")
plt.ylabel("Charge (%)")
plt.show()