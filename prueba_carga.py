# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
Spyder Editor

This is a temporary script file.
"""
#cerrar los plots que hayan quedado abiertos
plt.close('all')

#cargar los datos
data_set = np.loadtxt("datoscovidRIV.csv",delimiter=',')
data_x = data_set[:,0]
data_y = data_set[:,1]
numpoints = len(data_y)

#calcular los promedios
prom= np.zeros([6,numpoints])
for j in range(6):
#los días anteriores hubo 0 casos, calculamos los promedios de
#los primeros n-1 días.
    for i in range(j+1):
        suma = 0
        for k in range(i+1):
            suma +=data_y[k]
        prom[j][i]=suma/(j+2.0)
#calculo de los promedios desde el día n en adelante
    for i in range(j+1,numpoints):
        suma = 0
        for k in range(j+2):
            suma +=data_y[i-k]
        prom[j][i] =suma/(j+2.0)
        
#calcular los acumulados
acum = np.zeros(numpoints)
acum[0]=13
for i in range(1,numpoints):
    acum[i]=acum[i-1]+data_y[i]

#calcular los tiempos de duplicación
log_data = np.log2(acum)
fit=np.poly1d(np.polyfit(data_x[60:], log_data[60:], 1))
fit_data_log= fit(data_x)
fit_data=2**fit_data_log
print(fit)
print(1.0/(fit(1)-fit(0)))

#Hacer los gráficos
plt.figure('promedios')
plt.plot(data_x,data_y,'-bo',label="Casos Diarios")
plt.plot(data_x,prom[5],'--k',label="Promedio de 7 días")
plt.legend()
ejes=plt.gca()
ejes.set_title("Promedios casos diarios CoViD 19",size =22, weight='bold')
ejes.set_xlabel("Días desde el 31/7")
ejes.set_ylabel("Casos diarios")
plt.savefig("extremos.jpg")
plt.semilogy()
plt.savefig("extremos_log.jpg")
plt.close('promedios')
plt.figure('acumulados')
plt.plot(data_x,acum,'-bo', label="Casos totales")
plt.plot(data_x,fit_data,'-r',label="Ajuste exponencial")
plt.legend()
ejes=plt.gca()
ejes.set_title("Casos acumulados de CoViD 19",size =22, weight='bold')
ejes.set_xlabel("Días desde el 31/7")
ejes.set_ylabel("Casos acumulados")
plt.savefig("acum.jpg")
plt.semilogy()
plt.savefig("acum_log.jpg")
plt.close('acumulados')
