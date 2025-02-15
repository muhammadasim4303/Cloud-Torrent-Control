import psutil

def get_battery_status():
    battery = psutil.sensors_battery()
    if not battery:
        return {"error": "Battery information not available"}
    
    return {
        "battery_percentage": f"{battery.percent}%",
        "status": "Charging" if battery.power_plugged else "Not Charging"
    }
