import requests


def get_office_state(sensor_host, sensor_port):

    try:
        r = requests.get(f'{sensor_host}:{sensor_port}')
        answer = r.json()
        temp = answer.get('temp', 25)
        humidity = answer.get('hum', -1)
        return f"It's {temp}°C in office now, and {humidity}% air humidity."
    except Exception as e:
        temp = 25
        humidity = 26
        return f"It's {temp}°C in office now, and {humidity}% air humidity."
