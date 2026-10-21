// ---------------------- VALIDACIONES ---------------------------------

Funcion valido <- validar_dni(dni)
	Definir valido Como Logico
	Definir i Como Entero
	Definir c Como Caracter
	valido <- Verdadero
	Si Longitud(dni) <> 8 Entonces
		valido <- Falso
	SiNo
		Para i <- 1 Hasta 8 Hacer
			c <- Subcadena(dni, i, i)
			Si c < "0" O c > "9" Entonces
				valido <- Falso
			FinSi
		FinPara
	FinSi
FinFuncion

Funcion valido <- validar_texto(txt, maximo)
	Definir valido Como Logico
	valido <- Longitud(txt) > 0 Y Longitud(txt) <= maximo
FinFuncion

Funcion valido <- validar_folios(valor)
	Definir valido Como Logico
	Definir i Como Entero
	Definir c Como Caracter
	valido <- Verdadero
	Si Longitud(valor) = 0 O Longitud(valor) > 4 Entonces
		valido <- Falso
	SiNo
		Para i <- 1 Hasta Longitud(valor) Hacer
			c <- Subcadena(valor, i, i)
			Si c < "0" O c > "9" Entonces
				valido <- Falso
			FinSi
		FinPara
		Si valido Entonces
			Si ConvertirANumero(valor) <= 0 Entonces
				valido <- Falso
			FinSi
		FinSi
	FinSi
FinFuncion

Funcion valido <- validar_tipo(tipo)
	Definir valido Como Logico
	valido <- tipo = "SOLICITUD" O tipo = "CARTA" O tipo = "RECLAMO" O tipo = "RECURSO" O tipo = "OFICIO"
FinFuncion

Funcion valido <- validar_area(area)
	Definir valido Como Logico
	valido <- area = "LICENCIAS" O area = "RENTAS" O area = "OBRAS" O area = "SECRETARIA GENERAL" O area = "SERVICIOS A LA CIUDAD"
FinFuncion

// ---------------------- UTILIDADES -----------------------------------

// Quita espacios al inicio y al final y convierte a mayúsculas
Funcion r <- normalizar(s)
	Definir r Como Cadena
	Definir ini, fin Como Entero
	Definir seguir Como Logico
	ini <- 1
	fin <- Longitud(s)
	seguir <- Verdadero
	Mientras seguir Hacer
		Si ini > fin Entonces
			seguir <- Falso
		SiNo
			Si Subcadena(s, ini, ini) = " " Entonces
				ini <- ini + 1
			SiNo
				seguir <- Falso
			FinSi
		FinSi
	FinMientras
	seguir <- Verdadero
	Mientras seguir Hacer
		Si fin < ini Entonces
			seguir <- Falso
		SiNo
			Si Subcadena(s, fin, fin) = " " Entonces
				fin <- fin - 1
			SiNo
				seguir <- Falso
			FinSi
		FinSi
	FinMientras
	Si ini > fin Entonces
		r <- ""
	SiNo
		r <- Mayusculas(Subcadena(s, ini, fin))
	FinSi
FinFuncion

Funcion r <- dos_digitos(x)
	Definir r Como Cadena
	r <- ConvertirATexto(x)
	Si x < 10 Entonces
		r <- "0" + r
	FinSi
FinFuncion

Funcion f <- fecha_actual()
	Definir f Como Cadena
	Definir fe, ho, d, m, a, hh, mi Como Entero
	fe <- FechaActual()
	ho <- HoraActual()
	a <- trunc(fe / 10000)
	m <- trunc(fe / 100) MOD 100
	d <- fe MOD 100
	hh <- trunc(ho / 10000)
	mi <- trunc(ho / 100) MOD 100
	f <- dos_digitos(d) + "/" + dos_digitos(m) + "/" + ConvertirATexto(a) + " " + dos_digitos(hh) + ":" + dos_digitos(mi)
FinFuncion

// Genera EXP-AAAA-NNNNN con el siguiente correlativo
Funcion codigo <- generar_codigo(n)
	Definir codigo, numero Como Cadena
	Definir anio Como Entero
	anio <- trunc(FechaActual() / 10000)
	numero <- ConvertirATexto(n + 1)
	Mientras Longitud(numero) < 5 Hacer
		numero <- "0" + numero
	FinMientras
	codigo <- "EXP-" + ConvertirATexto(anio) + "-" + numero
FinFuncion

// ---------------------- ARCHIVOS (simulados) -------------------------

Funcion cargar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n Por Referencia)
	codigos[1] <- "EXP-2026-00003"
	dnis[1] <- "71234567"
	nombres[1] <- "ROSA MENDOZA CHAVEZ"
	asuntos[1] <- "SOLICITUD DE CONSTANCIA DE POSESION"
	tipos[1] <- "SOLICITUD"
	folios[1] <- 4
	areas[1] <- "OBRAS"
	fechas[1] <- "20/10/2026 10:05"

	codigos[2] <- "EXP-2026-00001"
	dnis[2] <- "45678912"
	nombres[2] <- "ANA TORRES QUISPE"
	asuntos[2] <- "SOLICITUD DE LICENCIA DE FUNCIONAMIENTO"
	tipos[2] <- "SOLICITUD"
	folios[2] <- 3
	areas[2] <- "LICENCIAS"
	fechas[2] <- "20/10/2026 09:15"

	codigos[3] <- "EXP-2026-00002"
	dnis[3] <- "70123456"
	nombres[3] <- "LUIS RAMOS DIAZ"
	asuntos[3] <- "RECLAMO POR ARBITRIOS"
	tipos[3] <- "RECLAMO"
	folios[3] <- 2
	areas[3] <- "RENTAS"
	fechas[3] <- "20/10/2026 09:40"
	n <- 3
	Escribir "Se cargaron ", n, " expedientes desde data/expedientes.txt"
FinFuncion

Funcion guardar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n, detalle)
	Definir i Como Entero
	Si detalle Entonces
		Escribir "----- Contenido de data/expedientes.txt -----"
		Para i <- 1 Hasta n Hacer
			Escribir codigos[i], "|", dnis[i], "|", nombres[i], "|", asuntos[i], "|", tipos[i], "|", folios[i], "|", areas[i], "|", fechas[i]
		FinPara
		Escribir "---------------------------------------------"
	SiNo
		Escribir "[Archivo data/expedientes.txt actualizado: ", n, " expedientes]"
	FinSi
FinFuncion

// ---------------------- EXPEDIENTES ----------------------------------

Funcion mostrar_expediente(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, i)
	Escribir "Código   : ", codigos[i]
	Escribir "DNI      : ", dnis[i]
	Escribir "Nombre   : ", nombres[i]
	Escribir "Asunto   : ", asuntos[i]
	Escribir "Tipo     : ", tipos[i]
	Escribir "Folios   : ", folios[i]
	Escribir "Área     : ", areas[i]
	Escribir "Recibido : ", fechas[i]
FinFuncion

Funcion registrar_expediente(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n Por Referencia)
	Definir dni, nombre, asunto, tipo, nfol, area, codigo Como Cadena
	Definir ok Como Logico

	Si n >= 100 Entonces
		Escribir "No hay espacio para más expedientes."
	SiNo
		Escribir "=== REGISTRAR EXPEDIENTE ==="
		Repetir
			Escribir "DNI (8 dígitos): " Sin Saltar
			Leer dni
			dni <- normalizar(dni)
			ok <- validar_dni(dni)
			Si NO ok Entonces
				Escribir "  Dato inválido: el DNI debe tener exactamente 8 dígitos numéricos."
			FinSi
		Hasta Que ok

		Repetir
			Escribir "Nombres y apellidos: " Sin Saltar
			Leer nombre
			nombre <- normalizar(nombre)
			ok <- validar_texto(nombre, 60)
			Si NO ok Entonces
				Escribir "  Dato inválido: el nombre no puede estar vacío (máx. 60 caracteres)."
			FinSi
		Hasta Que ok

		Repetir
			Escribir "Asunto: " Sin Saltar
			Leer asunto
			asunto <- normalizar(asunto)
			ok <- validar_texto(asunto, 100)
			Si NO ok Entonces
				Escribir "  Dato inválido: el asunto no puede estar vacío (máx. 100 caracteres)."
			FinSi
		Hasta Que ok

		Repetir
			Escribir "Tipo (SOLICITUD, CARTA, RECLAMO, RECURSO, OFICIO): " Sin Saltar
			Leer tipo
			tipo <- normalizar(tipo)
			ok <- validar_tipo(tipo)
			Si NO ok Entonces
				Escribir "  Dato inválido: elija un tipo de la lista."
			FinSi
		Hasta Que ok

		Repetir
			Escribir "Número de folios: " Sin Saltar
			Leer nfol
			nfol <- normalizar(nfol)
			ok <- validar_folios(nfol)
			Si NO ok Entonces
				Escribir "  Dato inválido: los folios deben ser un número entero mayor que 0."
			FinSi
		Hasta Que ok

		Repetir
			Escribir "Área (LICENCIAS, RENTAS, OBRAS, SECRETARIA GENERAL, SERVICIOS A LA CIUDAD): " Sin Saltar
			Leer area
			area <- normalizar(area)
			ok <- validar_area(area)
			Si NO ok Entonces
				Escribir "  Dato inválido: elija un área de la lista."
			FinSi
		Hasta Que ok

		codigo <- generar_codigo(n)
		n <- n + 1
		codigos[n] <- codigo
		dnis[n] <- dni
		nombres[n] <- nombre
		asuntos[n] <- asunto
		tipos[n] <- tipo
		folios[n] <- ConvertirANumero(nfol)
		areas[n] <- area
		fechas[n] <- fecha_actual()

		guardar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n, Falso)
		Escribir ""
		Escribir "*** CARGO DE RECEPCIÓN ***"
		mostrar_expediente(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
	FinSi
FinFuncion

// Búsqueda lineal: devuelve la posición o -1 si no existe
Funcion pos <- buscar_expediente(codigos, n, codigo)
	Definir pos, i Como Entero
	codigo <- normalizar(codigo)
	pos <- -1
	i <- 1
	Mientras i <= n Y pos = -1 Hacer
		Si codigos[i] = codigo Entonces
			pos <- i
		FinSi
		i <- i + 1
	FinMientras
FinFuncion

// Intercambia las posiciones i y j en TODOS los arreglos
Funcion intercambiar(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, i, j)
	Definir aux Como Cadena
	Definir auxNum Como Entero
	aux <- codigos[i]
	codigos[i] <- codigos[j]
	codigos[j] <- aux
	aux <- dnis[i]
	dnis[i] <- dnis[j]
	dnis[j] <- aux
	aux <- nombres[i]
	nombres[i] <- nombres[j]
	nombres[j] <- aux
	aux <- asuntos[i]
	asuntos[i] <- asuntos[j]
	asuntos[j] <- aux
	aux <- tipos[i]
	tipos[i] <- tipos[j]
	tipos[j] <- aux
	auxNum <- folios[i]
	folios[i] <- folios[j]
	folios[j] <- auxNum
	aux <- areas[i]
	areas[i] <- areas[j]
	areas[j] <- aux
	aux <- fechas[i]
	fechas[i] <- fechas[j]
	fechas[j] <- aux
FinFuncion

Funcion listar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
	Definir i Como Entero
	Si n = 0 Entonces
		Escribir "No hay expedientes registrados."
	SiNo
		Escribir "=== LISTADO DE EXPEDIENTES (", n, ") ==="
		Escribir "CÓDIGO          | DNI      | NOMBRE | TIPO | FOLIOS | ÁREA | FECHA"
		Para i <- 1 Hasta n Hacer
			Escribir codigos[i], "  | ", dnis[i], " | ", nombres[i], " | ", tipos[i], " | ", folios[i], " | ", areas[i], " | ", fechas[i]
		FinPara
	FinSi
FinFuncion

// Ordenamiento por código: método burbuja
Funcion ordenar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
	Definir j, k Como Entero
	Para j <- 1 Hasta n - 1 Hacer
		Para k <- 1 Hasta n - j Hacer
			Si codigos[k] > codigos[k + 1] Entonces
				intercambiar(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, k, k + 1)
			FinSi
		FinPara
	FinPara
	Escribir "Expedientes ordenados por código."
	guardar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n, Falso)
	listar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
FinFuncion

Funcion opcion <- mostrar_menu()
	Definir opcion Como Cadena
	Escribir ""
	Escribir "========== MESA DE PARTES DIGITAL =========="
	Escribir "1. Registrar expediente"
	Escribir "2. Buscar expediente por código"
	Escribir "3. Ordenar expedientes por código"
	Escribir "4. Listar expedientes"
	Escribir "5. Guardar y salir"
	Escribir "Elija una opción: " Sin Saltar
	Leer opcion
	opcion <- normalizar(opcion)
FinFuncion

// ---------------------- PROGRAMA PRINCIPAL ---------------------------

Algoritmo MesaPartesDigital
	Definir codigos, dnis, nombres, asuntos, tipos, areas, fechas Como Cadena
	Definir folios Como Entero
	Dimension codigos[100], dnis[100], nombres[100], asuntos[100], tipos[100], folios[100], areas[100], fechas[100]
	Definir n, pos Como Entero
	Definir opcion, codigo Como Cadena

	n <- 0
	cargar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)

	Repetir
		opcion <- mostrar_menu()
		Si opcion = "1" Entonces
			registrar_expediente(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
		SiNo
			Si opcion = "2" Entonces
				Escribir "Código a buscar (ej. EXP-2026-00001): " Sin Saltar
				Leer codigo
				pos <- buscar_expediente(codigos, n, codigo)
				Si pos = -1 Entonces
					Escribir "Expediente no encontrado."
				SiNo
					Escribir "=== EXPEDIENTE ENCONTRADO ==="
					mostrar_expediente(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, pos)
				FinSi
			SiNo
				Si opcion = "3" Entonces
					ordenar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
				SiNo
					Si opcion = "4" Entonces
						listar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n)
					SiNo
						Si opcion = "5" Entonces
							guardar_expedientes(codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas, n, Verdadero)
							Escribir "Datos guardados. Hasta luego."
						SiNo
							Escribir "Opción inválida. Intente de nuevo."
						FinSi
					FinSi
				FinSi
			FinSi
		FinSi
	Hasta Que opcion = "5"
FinAlgoritmo
