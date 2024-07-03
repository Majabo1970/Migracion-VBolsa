import csv
import random
import string

def generate_random_string(length):
    """Genera una cadena aleatoria alfanumérica de una longitud dada."""
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def load_relationships(csv_file):
    """Carga las relaciones desde el archivo CSV y las devuelve como un diccionario."""
    relationships = {}
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Verificar si las columnas necesarias están presentes
            if 'COMITENTE_BMA' not in row or 'CUENTA_MS' not in row:
                print(f"Encabezados encontrados: {row.keys()}")
                raise KeyError("El archivo CSV no contiene las columnas 'COMITENTE_BMA' y 'CUENTA_MS'")
            comitente_bma = row['COMITENTE_BMA'].strip()
            cuenta_ms = row['CUENTA_MS'].strip()
            relationships[comitente_bma] = cuenta_ms
    return relationships

def format_quantity(quantity, decimal_positions):
    """Formatea el campo Quantity según las posiciones decimales especificadas."""
    quantity = quantity.lstrip('0')
    if not quantity:
        quantity = '0'
    if decimal_positions == '0':
        return f"{quantity}.0"
    else:
        decimal_positions = int(decimal_positions)
        if len(quantity) <= decimal_positions:
            quantity = quantity.zfill(decimal_positions + 1)
        return f"{quantity[:-decimal_positions]}.{quantity[-decimal_positions:]}"

def process_line(line, relationships):
    """Procesa una línea del archivo de entrada y devuelve un diccionario con los valores correspondientes."""
    comitente_bma = line[10:19].strip().lstrip('0')
    quantity = line[41:59].strip().lstrip('0')
    decimal_positions = line[60:61]
    formatted_quantity = format_quantity(quantity, decimal_positions)
    return {
        'InstructingParty': '171',
        'SettlementParty': '171',
        'SecuritiesAccount': '171/' + comitente_bma,
        'Instrument': line[20:25].strip().lstrip('0'),
        'InstrumentIdentifierType': 'LOCAL_CODE',
        'CSDOfCounterparty': 'CVSA',
        'SettlementCounterparty': '33',
        'SecuritiesAccountOfCounterparty': '33/' + relationships.get(comitente_bma, 'Sin Cuenta'),
        'InstructionReference': generate_random_string(16),
        'Instrument(MovementOfSecurities)': 'DELIVER',
        'Quantity': formatted_quantity,
        'QuantityType': '',
        'TransactionType': 'TRAD',
        'SettlementMethod': 'RTGS',
        'TradeDate': line[31:39].strip(),
        'IntendedSettlementDate': line[31:39].strip(),
        'PaymentType': 'NOTHING'
    }

def main():
    input_file = 'input.txt'
    output_file_macro1 = 'destino_BMA.si1'
    relationship_file = 'relacion.csv'

    # Cargar relaciones desde el archivo CSV
    relationships = load_relationships(relationship_file)
    # Encabezado del archivo de salida
    header = ('InstructingParty;SettlementParty;SecuritiesAccount;Instrument;InstrumentIdentifierType;'
              'CSDOfCounterparty;SettlementCounterparty;SecuritiesAccountOfCounterparty;InstructionReference;'
              'Instrument(MovementOfSecurities);Quantity;QuantityType;TransactionType;SettlementMethod;'
              'TradeDate;IntendedSettlementDate;PaymentType\n')
    
    destino_macro1 = []

    with open(input_file, 'r') as infile:
        lines = infile.readlines()[1:]  # Saltar la primera línea del archivo de entrada
        for line in lines:
            data = process_line(line, relationships)
            instrument = line[20:25].strip()
            posicion = line[28:30]

            if instrument in ["06000", "07000", "08000", "09000", "10000", "20000"]:
                continue  # Excluir de destino_MACRO1.si1
            elif posicion == "02":
                continue  # Excluir de destino_MACRO1.si1
            else:
                destino_macro1.append(data)

    with open(output_file_macro1, 'w') as outfile:
        outfile.write(header)
        for data in destino_macro1:
            outfile.write(';'.join(data.values()) + '\n')

if __name__ == "__main__":
    main()
