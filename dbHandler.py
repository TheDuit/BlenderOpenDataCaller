from DBConnection import connect_to_db
from blenderApi import get_all_devices
from datetime import datetime
conn, cur = connect_to_db()


def get_device_id_by_name(name):
    # Consultar o ID do dispositivo pelo nome
    cur.execute("SELECT id FROM devices WHERE name = %s", (name,))
    result = cur.fetchone()

    if result:
        return result[0]
    else:
        return None


def write_device(device):
    # Verificar se o dispositivo já existe no banco de dados
    cur.execute("SELECT id FROM devices WHERE name = %s AND type = %s", (device.name, device.type))
    result = cur.fetchone()

    if result:
        device_id = result[0]
        print(f"Dispositivo {device.name} já existe com ID {device_id}")
    else:
        # Inserir o dispositivo se não existir
        cur.execute("""
            INSERT INTO devices (name, type)
            VALUES (%s, %s)
            RETURNING id;
        """, (device.name, device.type))
        device_id = cur.fetchone()[0]
        conn.commit()
        print(f"Adicionado {device.name} com ID {device_id}")

    return device_id


def write_benchmarks(device_name, score, benchmarks):
    device_id = get_device_id_by_name(device_name)

    if device_id:
        cur.execute("""
            INSERT INTO benchmarks (device_id, score, benchmark_count, date)
            VALUES (%s, %s, %s, %s)
        """, (device_id, score, benchmarks, datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")))
        conn.commit()
        print(f"Benchmarks para o dispositivo {device_name} foram adicionados")
    else:
        print(f"Dispositivo {device_name} não encontrado.")


def process_devices_and_benchmarks():
    devices = get_all_devices()

    for device in devices.devices:
        if device.name != '':
            write_device(device)
            write_benchmarks(device.name, device.score, device.benchmarks)

    cur.close()
    conn.close()


process_devices_and_benchmarks()
