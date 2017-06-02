#	Librerias
import math
import pandas as pd

# 	Funciones

#	Metodo residual

def metodoResidual(tmax, tmin, tbase):
	gdd = 0.0
	if (tmax > umbralSuperior):
		tmax = umbralSuperior
	else:
		tmax = tmax
	if (tmin < umbralInferior):
		tmin = umbralInferior
	else:
		tmin = tmin
	gdd = ((tmax + tmin) / 2.0) - tbase

	if (gdd < 0):
		gdd = 0.0
	return gdd

# 	Metodo triangulo simple

def metodoTrianguloSimple(tmax, tmin):
	gdd = 0.0
	if (tmin > umbralSuperior and tmax > umbralSuperior):
		gdd = umbralSuperior - umbralInferior
	elif (tmax < umbralInferior and tmin < umbralInferior):
		gdd = 0.0
	elif (tmin >= umbralInferior and tmax <= umbralSuperior):
		gdd = ((6 * (tmax + tmin - 2.0 * umbralInferior)) / 12)
	elif (tmin < umbralInferior and tmax > umbralSuperior):
		dti = tmax - umbralInferior
		dts = tmax - umbralSuperior
		dt = tmax - tmin
		gdd = ((6 * pow(dti, 2.0) / dt) - ((6 * pow(dts, 2.0)) / dt)) / 12
	elif (tmin < umbralInferior and tmax > umbralInferior and tmax < umbralSuperior):
		dti = tmax - umbralInferior
		dt = tmax - tmin
		gdd = ((6 * (pow(dti, 2.0)) / dt)) / 12
	elif (tmin > umbralInferior and tmin < umbralSuperior and tmax > umbralSuperior):
		dt = tmax - tmin
		dts = tmax - umbralSuperior
		gddTS = ((6 * (tmax + tmin - 2.0 * umbralInferior)) / 12) - (((6 * pow(dts, 2.0)) / dt) / 12)
	return gdd

# 	Metodo seno simple

# 	Subrutina para metodo del seno simple
def sinec(suma, diff, fk1):
	twopi = 6.2834
	pihlf = 1.5708
	d2 = fk1 - suma
	d3 = diff * diff
	d4 = d2 * d2
	d5 = math.sqrt(d3 - d4)
	theta = math.atan2(d2, d5)
	if (d2 < 0 and theta > 0):
		theta = theta - 3.1416
	heat = (diff * math.cos(theta) - d2 * (pihlf - theta)) / twopi
	return heat

def metodoSenoSimple(tmax, tmin):
	gdd = 0.0
	if (tmin > umbralSuperior):
		gdd = umbralSuperior - umbralInferior
	else:
		if (tmax <= umbralInferior):
			gdd = 0.0
		else:
			fk1 = 2 * umbralInferior
			diff = tmax - tmin
			suma = tmax + tmin
			if (tmin >= umbralInferior):
				gdd = (suma - fk1) / 2
			else:
				gdd = sinec(suma, diff, fk1)
			if (tmax > umbralSuperior):
				fk1 = 2 * umbralSuperior
				gdd2 = gdd
				gdd = sinec(suma, diff, fk1)
				gdd = gdd2 - gdd
	return gdd

# 	Leer archivo .csv

data = pd.read_csv('datos.csv')

# 	Solicitar al usuario los umbrales del cultivo

print ("*************************************************************")
print ("*****      Programa para calcular grados-dias en Python *****")
print ("*****      Metodo Residual                              *****")
print ("*****      Metodo Triangulo Simple                      *****")
print ("*****      Metodo Seno Simple                           *****")
print ("*************************************************************")

# 	limites
umbralInferiorText = input("Introduce el umbral inferior: ")
umbralSuperiorText = input("Introduce el umbral superior: ")
tbaseText = input("Introduce la temperatura base: ")
umbralSuperior = float(umbralSuperiorText)
umbralInferior = float(umbralInferiorText)
tbase = int(tbaseText)

# 	variables

gddTS = 0.0
gddTD = 0.0
gddSS = 0.0

#	validacion de umbrales

if (umbralSuperior >= umbralInferior):
	data['GDDR'] = data.apply(lambda row: metodoResidual(row['tmax'], row['tmin'], tbase), axis=1)
	data['GDDTS'] = data.apply(lambda row: metodoTrianguloSimple(row['tmax'], row['tmin']), axis=1)
	data['GDDTSS'] = data.apply(lambda row: metodoSenoSimple(row['tmax'], row['tmin']), axis=1)
	data.to_csv('datos_procesados.csv', sep=',')
else:
	print ("Error \nLimite inferior mayor al superior")	