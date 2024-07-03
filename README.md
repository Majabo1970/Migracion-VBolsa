DETALLE DE PROCEDIMIENTO

1 - Archivos necesarios

    1.1 - imput.txt --> Archivo con los datos para migrar de las cuentas BMA. Se debe cambiar el nombre
                        a imput.txt

    "0"20240612"092013"Z20SDO"
    "1"0171"0"000000003"07000"0"00"20240611" 000000000000003346"2"00"
    "1"0171"0"000000053"05405"0"00"20240611" 000000000213829000"0"00"
    "1"0171"0"000000053"09234"0"00"20240611" 000000000000533900"0"00"

    1.2 - relacion.csv --> Archivo que contiene la relacion entra las cuentas BMA - MACRO
                           Debe contener este formato con esos nombres de cabecera en la primera fila

    COMITENTE_BMA;CUENTA_MS
    2;Sin cuenta
    4;Sin cuenta
    5;Sin cuenta
    6;Sin cuenta
    7;4646
    8;4645

2 - Archivos de salida

    2.1 - destino_MACRO.si1     --> Archivo RECEIVE sin las especies de efectivo ni saldos bloqueados
    
    2.2 - destino_BMA.si1       --> Archivo DELIVER sin las especies de efectivo ni saldos bloqueados
    
    2.3 - efectivo.si1          --> Archivo con las especies de efectivo solamente. No contempla las especies 
    
                                    "06000,07000,08000,09000,10000,20000" del archivo input.txt
                                    
    2.4 - saldos_bloqueados.si1 --> Archivo, con indicación en el archivo input.txt, de saldos bloqueados "02"

3 - Archivos Python

    3.1 - transforma_MACRO.py   --> Genera el archivo RECEIVE sin las especies de efectivo ni saldos bloqueados
    
                                --> Genera el archivo efectivo.si1
                                
                                --> Genera el archivo saldos_bloqueados.si1
                                
    3.2 - transforma_BMA.py     --> Genera el archivo DELIVER sin las especies de efectivo ni saldos bloqueados
