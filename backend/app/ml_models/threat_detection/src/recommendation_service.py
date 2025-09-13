def get_recommendations(threat_type: str):
    """
    Return a structured recommendation object for a given threat type.
    Structure:
    {
      "priority": "High" | "Medium" | "Low" | "Critical",
      "actions": [ "action 1", "action 2", ... ],
      "notes": "short guidance"
    }
    """
    recs = {
        "Wax_Moth": {
            "priority": "High",
            "actions": [
                "Close hive entrance at dusk and dawn to prevent moth entry.",
                "Inspect frames for larvae/galleries and remove heavily infested combs.",
                "Freeze infested combs (−18°C for 24–48 hrs) or replace them.",
                "Improve hive cleanliness and maintain strong colony population."
            ],
            "notes": "Wax moths favour warm, humid, weak colonies; reduce humidity and strengthen colonies."
        },
        "Predator": {
            "priority": "Critical",
            "actions": [
                "Narrow or close the hive entrance at night immediately.",
                "Install entrance guards (mesh/metal) to stop predators.",
                "Use physical barriers (fencing, elevated stands) to deter mammals.",
                "Consider temporary ultrasonic deterrent devices (test first)."
            ],
            "notes": "Predator attacks are urgent — take physical measures immediately."
        },
        "Environmental": {
            "priority": "Medium",
            "actions": [
                "Provide shade or relocate hive away from direct sun.",
                "Ensure water source is nearby and accessible for bees.",
                "Increase hive ventilation (e.g., screened bottom, vents).",
                "Monitor local weather alerts and move hives before extreme events if possible."
            ],
            "notes": "Environmental stress (heat/humidity/rain) can reduce foraging and increase disease risk."
        },
        "No_Threat": {
            "priority": "Low",
            "actions": [
                "No immediate action required — continue monitoring."
            ],
            "notes": "Maintain routine checks and sensor monitoring."
        }
    }
    return recs.get(threat_type, {
        "priority": "Unknown",
        "actions": ["No specific recommendation available."],
        "notes": ""
    })
