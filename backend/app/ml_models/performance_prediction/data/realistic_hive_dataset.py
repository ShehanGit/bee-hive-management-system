import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_realistic_hive_dataset(start_date_str, end_date_str, num_hives, time_interval_minutes):
    """
    Improved beehive monitoring dataset generator with:
    - Proper rainfall impact on weight increment
    - Balanced feature importance (not just min-sin, mon-cos dominant)
    - More realistic bee behavioral patterns
    - Better foraging conditions modeling
    """

    print(f"🐝 Generating realistic dataset for {num_hives} hive(s)")
    print(f"📅 Period: {start_date_str} to {end_date_str}")
    print(f"⏱️  Interval: {time_interval_minutes} minutes")

    # Validation
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
    except ValueError as e:
        print(f"❌ Date error: {e}")
        return None

    # Create timestamp range
    timestamps = pd.date_range(start=start_date, end=end_date, freq=f'{time_interval_minutes}T')
    print(f"📊 Total data points per hive: {len(timestamps):,}")

    final_df = pd.DataFrame()

    for hive_id in range(1, num_hives + 1):
        print(f"  🏠 Processing Hive {hive_id}...")

        df = pd.DataFrame({'collection_timestamp': timestamps})
        df['hive_id'] = hive_id
        num_records = len(df)

        # Extract time components for better feature balance
        hours = df['collection_timestamp'].dt.hour
        day_of_year = df['collection_timestamp'].dt.dayofyear
        month = df['collection_timestamp'].dt.month
        day_of_week = df['collection_timestamp'].dt.dayofweek

        # ==========================================
        # BALANCED WEATHER SIMULATION
        # ==========================================

        # Temperature - Multiple influencing factors
        base_temp = 20 + np.random.normal(0, 2)  # Base varies by hive location

        # Daily cycle (reduced dominance)
        daily_temp_cycle = 4 * np.sin(2 * np.pi * (hours - 6) / 24)

        # Seasonal cycle (reduced dominance)
        seasonal_temp_cycle = 3 * np.sin(2 * np.pi * (day_of_year - 80) / 365)

        # Weekly patterns (new important factor)
        weekly_temp_pattern = 1.5 * np.sin(2 * np.pi * day_of_week / 7)

        # Random weather fronts (important factor)
        weather_front_days = np.random.choice(range(len(timestamps)),
                                            size=int(len(timestamps) * 0.15),
                                            replace=False)
        weather_front_effect = np.zeros(num_records)
        for day in weather_front_days:
            start_idx = max(0, day - 48)  # 2-day weather systems
            end_idx = min(num_records, day + 48)
            weather_front_effect[start_idx:end_idx] += np.random.uniform(-3, 3)

        # Altitude/microclimate effect (hive-specific)
        microclimate_effect = np.random.uniform(-2, 2) * np.sin(2 * np.pi * hours / 24)

        df['weather_temperature'] = (
            base_temp
            + daily_temp_cycle * 0.6  # Reduced importance
            + seasonal_temp_cycle * 0.5  # Reduced importance
            + weekly_temp_pattern  # New important factor
            + weather_front_effect  # Important random factor
            + microclimate_effect  # Hive-specific factor
            + np.random.normal(0, 1.2, num_records)  # Increased noise
        )

        # Humidity - More complex interactions
        base_humidity = 75 + np.random.normal(0, 5)

        # Temperature relationship (non-linear)
        temp_humidity_relationship = -1.5 * (df['weather_temperature'] - 25) + \
                                   0.05 * (df['weather_temperature'] - 25) ** 2

        # Time-based patterns
        daily_humidity_cycle = 8 * np.cos(2 * np.pi * (hours - 14) / 24)  # Peak afternoon dryness
        seasonal_humidity = 10 * np.sin(2 * np.pi * (day_of_year - 100) / 365)

        # Pressure system effects
        pressure_humidity_effect = np.random.normal(0, 3, num_records)

        df['weather_humidity'] = (
            base_humidity
            + temp_humidity_relationship * 0.7
            + daily_humidity_cycle * 0.6
            + seasonal_humidity * 0.4
            + pressure_humidity_effect
            + np.random.normal(0, 4, num_records)
        )
        df['weather_humidity'] = np.clip(df['weather_humidity'], 40, 99)

        # Wind Speed - More realistic patterns
        base_wind = 8 + np.random.normal(0, 2)

        # Daily wind patterns (thermal winds)
        thermal_winds = 6 * np.sin(2 * np.pi * (hours - 12) / 24).clip(0, 1)

        # Seasonal wind patterns (monsoons)
        monsoon_winds = np.where(month.isin([5, 6, 10, 11]),
                                np.random.uniform(3, 8, num_records), 0)

        # Weather system winds
        system_winds = np.random.exponential(2, num_records)

        # Topographic effects
        topo_winds = np.random.uniform(0, 3) * np.sin(2 * np.pi * hours / 24)

        df['weather_wind_speed'] = (
            base_wind
            + thermal_winds
            + monsoon_winds
            + system_winds
            + topo_winds
        )
        df['weather_wind_speed'] = np.clip(df['weather_wind_speed'], 0, 40)

        # Light Intensity - More nuanced
        sunrise_hour = 6 + np.random.uniform(-0.5, 0.5)
        sunset_hour = 18 + np.random.uniform(-0.5, 0.5)

        # Cloud cover effects (major factor)
        cloud_cover = np.random.uniform(0, 1, num_records)
        cloud_factor = 1 - (cloud_cover ** 1.5)

        # Seasonal light variation
        seasonal_light_factor = 0.8 + 0.2 * np.sin(2 * np.pi * (day_of_year - 172) / 365)

        # Calculate daylight
        daylight_hours = hours - sunrise_hour
        is_daylight = (daylight_hours >= 0) & (daylight_hours <= (sunset_hour - sunrise_hour))
        daylight_intensity = np.where(
            is_daylight,
            np.sin(np.pi * daylight_hours / (sunset_hour - sunrise_hour)),
            0
        )

        max_light = 55000 * seasonal_light_factor
        df['weather_light_intensity'] = (
            daylight_intensity * max_light * cloud_factor +
            np.random.uniform(0, 2000, num_records)  # Scattered light
        )
        df['weather_light_intensity'] = np.clip(df['weather_light_intensity'], 0, 70000)

        # Enhanced Rainfall Model - CRITICAL for weight impact
        # Monsoon probabilities
        rain_prob_base = np.where(month.isin([5, 6]), 0.20,      # Heavy monsoon
                         np.where(month.isin([10, 11]), 0.18,    # Secondary monsoon
                         np.where(month.isin([7, 8, 12, 1]), 0.12, # Moderate
                                  0.06)))                         # Dry season

        # Daily rain probability variation
        afternoon_rain_boost = np.where((hours >= 14) & (hours <= 18), 1.8, 1.0)
        rain_probability = rain_prob_base * afternoon_rain_boost

        # Generate rain events
        is_raining = np.random.rand(num_records) < rain_probability

        # Rain intensity (exponential distribution)
        rain_intensity = np.where(is_raining,
                                np.random.exponential(3.5, num_records), 0)

        # Multi-day rain events (important for weight impact)
        rain_event_continuation = np.zeros(num_records, dtype=bool)
        for i in range(1, num_records):
            if is_raining[i-1] and np.random.rand() < 0.4:  # 40% chance rain continues
                rain_event_continuation[i] = True
                rain_intensity[i] = max(rain_intensity[i],
                                      rain_intensity[i-1] * np.random.uniform(0.6, 1.2))

        df['weather_rainfall'] = np.where(is_raining | rain_event_continuation,
                                        rain_intensity, 0)

        # Weather interactions during rain
        rain_mask = df['weather_rainfall'] > 0
        df.loc[rain_mask, 'weather_humidity'] = np.clip(
            df.loc[rain_mask, 'weather_humidity'] + np.random.uniform(10, 20, rain_mask.sum()),
            40, 99
        )
        df.loc[rain_mask, 'weather_light_intensity'] *= np.random.uniform(0.1, 0.5, rain_mask.sum())
        df.loc[rain_mask, 'weather_temperature'] -= np.random.uniform(1, 5, rain_mask.sum())

        # ==========================================
        # HIVE SENSOR SIMULATION
        # ==========================================

        # Internal temperature (precise regulation)
        target_temp = 34.5 + np.random.normal(0, 0.1)  # Slight hive variation
        regulation_efficiency = 0.95  # Very good regulation

        external_influence = (1 - regulation_efficiency) * \
                           (df['weather_temperature'] - 25) * 0.08

        df['sensor_temperature'] = (
            target_temp +
            external_influence +
            np.random.normal(0, 0.3, num_records)
        )

        # Internal humidity (bee-controlled)
        target_humidity = 85 + np.random.normal(0, 2)
        external_humidity_influence = (df['weather_humidity'] - 75) * 0.1

        df['sensor_humidity'] = (
            target_humidity +
            external_humidity_influence +
            np.random.normal(0, 2, num_records)
        )
        df['sensor_humidity'] = np.clip(df['sensor_humidity'], 70, 95)

        # Sound levels - Activity based
        base_sound = 55 + np.random.normal(0, 2)

        # Foraging activity sound (multi-factor)
        is_foraging_time = (hours >= 6) & (hours <= 18)
        good_weather = (df['weather_temperature'] > 16) & \
                      (df['weather_temperature'] < 32) & \
                      (df['weather_rainfall'] < 1) & \
                      (df['weather_wind_speed'] < 25) & \
                      (df['weather_light_intensity'] > 8000)

        foraging_activity = is_foraging_time & good_weather
        activity_sound = np.where(foraging_activity,
                                np.random.uniform(4, 10, num_records), 0)

        # Circadian rhythm
        daily_activity = 3 * np.sin(2 * np.pi * (hours - 8) / 12).clip(0, 1)

        # Seasonal activity
        seasonal_activity = 0.5 + 0.5 * np.sin(2 * np.pi * (day_of_year - 80) / 365)

        df['sensor_sound'] = (
            base_sound +
            activity_sound +
            daily_activity * seasonal_activity +
            np.random.normal(0, 1.5, num_records)
        )

        # ==========================================
        # REALISTIC WEIGHT SIMULATION - KEY IMPROVEMENT
        # ==========================================

        hive_vigor = np.random.uniform(0.8, 1.3)  # Hive strength factor
        start_weight = 3.0 + np.random.uniform(0, 0.8)

        weights = [start_weight]

        # Track consecutive rain days for cumulative effect
        consecutive_rain_days = 0

        for i in range(1, num_records):
            current_time = df['collection_timestamp'].iloc[i]
            prev_weight = weights[-1]

            # Time factors
            hour = current_time.hour
            days_from_start = (current_time - start_date).days

            # Growth phase determination
            if days_from_start < 20:
                growth_multiplier = 0.3
            elif days_from_start < 60:
                growth_multiplier = 0.8
            elif days_from_start < 100:  # Peak season
                growth_multiplier = 1.2
            elif days_from_start < 130:
                growth_multiplier = 0.9
            else:
                growth_multiplier = 0.4

            # CRITICAL: Rainfall impact on foraging
            current_rain = df['weather_rainfall'].iloc[i]
            recent_rain_impact = 0

            if current_rain > 0:
                consecutive_rain_days += 1
                # Heavy rain completely stops foraging
                if current_rain > 5:
                    foraging_possible = False
                    recent_rain_impact = -0.8  # Negative impact
                elif current_rain > 1:
                    foraging_possible = np.random.rand() < 0.2  # 20% chance
                    recent_rain_impact = -0.6
                else:
                    foraging_possible = np.random.rand() < 0.6  # 60% chance
                    recent_rain_impact = -0.3
            else:
                consecutive_rain_days = 0
                foraging_possible = True

            # Cumulative rain effect (bees stay inside, consume stores)
            if consecutive_rain_days > 0:
                rain_consumption_penalty = -0.0003 * min(consecutive_rain_days, 10)
            else:
                rain_consumption_penalty = 0

            # Foraging conditions assessment
            temp = df['weather_temperature'].iloc[i]
            wind = df['weather_wind_speed'].iloc[i]
            light = df['weather_light_intensity'].iloc[i]

            optimal_foraging = (
                foraging_possible and
                temp > 18 and temp < 30 and
                wind < 20 and
                light > 10000 and
                hour >= 7 and hour <= 17
            )

            moderate_foraging = (
                foraging_possible and
                temp > 15 and temp < 33 and
                wind < 30 and
                light > 5000 and
                hour >= 6 and hour <= 18
            ) and not optimal_foraging

            # Weight change calculation
            if optimal_foraging:
                # Good conditions - significant weight gain
                base_gain = np.random.uniform(0.002, 0.006) * growth_multiplier * hive_vigor
                daily_change = base_gain + recent_rain_impact * 0.1  # Reduce rain penalty in good conditions
            elif moderate_foraging:
                # Moderate conditions - small weight gain
                base_gain = np.random.uniform(0.0005, 0.002) * growth_multiplier * hive_vigor
                daily_change = base_gain + recent_rain_impact * 0.2
            else:
                # Poor/no foraging - consumption only
                if hour in range(20, 24) or hour in range(0, 6):
                    # Nighttime consumption
                    daily_change = -np.random.uniform(0.0002, 0.0008)
                else:
                    # Daytime no-foraging (rain/bad weather)
                    daily_change = -np.random.uniform(0.0001, 0.0004)

                # Apply full rain impact
                daily_change += recent_rain_impact * 0.0003

            # Add rain consumption penalty
            daily_change += rain_consumption_penalty

            # Seasonal nectar flow bonus (only when foraging possible)
            if foraging_possible and current_time.month in [7, 8]:
                daily_change *= np.random.uniform(1.3, 2.2)

            # Apply change
            new_weight = prev_weight + daily_change
            weights.append(max(new_weight, start_weight * 0.9))  # Prevent excessive loss

        df['sensor_weight'] = weights

        # Add to final dataset
        final_df = pd.concat([final_df, df], ignore_index=True)

    # Final cleanup
    numeric_columns = final_df.select_dtypes(include=[np.number]).columns
    final_df[numeric_columns] = final_df[numeric_columns].round(4)

    print("✅ Realistic dataset generation complete!")
    print(f"📊 Features balanced - reduced min-sin/mon-cos dominance")
    print(f"🌧️  Rainfall impact on weight properly modeled")

    return final_df

# ==========================================
# USAGE EXAMPLE
# ==========================================

def generate_realistic_dataset():
    """Generate balanced, realistic dataset"""

    START_DATE = '2025-04-01'
    END_DATE = '2025-09-30'
    NUM_HIVES = 3
    INTERVAL_MINUTES = 1

    dataset = create_realistic_hive_dataset(
        start_date_str=START_DATE,
        end_date_str=END_DATE,
        num_hives=NUM_HIVES,
        time_interval_minutes=INTERVAL_MINUTES
    )

    if dataset is None:
        return

    # Save dataset
    filename = f'realistic_hive_data_{NUM_HIVES}hives.csv'
    dataset.to_csv(filename, index=False)
    print(f"💾 Dataset saved as '{filename}'")

    # Analysis
    print(f"\n📊 Dataset Summary:")
    print(f"Total records: {len(dataset):,}")
    print(f"Hives: {dataset['hive_id'].nunique()}")

    # Weight analysis by weather
    print(f"\n🌧️ Weight Change Analysis:")

    # Group by rain conditions
    dataset['rain_category'] = pd.cut(dataset['weather_rainfall'],
                                    bins=[0, 0.1, 2, 10, float('inf')],
                                    labels=['No Rain', 'Light', 'Moderate', 'Heavy'])

    rain_weight_analysis = dataset.groupby('rain_category').agg({
        'sensor_weight': ['count', 'mean'],
        'weather_rainfall': 'mean'
    }).round(4)
    print(rain_weight_analysis)

    # Sample output format
    print(f"\n📋 Sample Output Format:")
    sample = dataset.head(3)[['collection_timestamp', 'hive_id', 'weather_temperature',
                             'weather_humidity', 'weather_wind_speed', 'weather_light_intensity',
                             'weather_rainfall', 'sensor_temperature', 'sensor_humidity',
                             'sensor_sound', 'sensor_weight']]

    for _, row in sample.iterrows():
        print(f"{row['collection_timestamp']} {row['hive_id']} {row['weather_temperature']} "
              f"{row['weather_humidity']} {row['weather_wind_speed']} {row['weather_light_intensity']} "
              f"{row['weather_rainfall']} {row['sensor_temperature']} {row['sensor_humidity']} "
              f"{row['sensor_sound']} {row['sensor_weight']}")

    return dataset

# Run the generator
if __name__ == "__main__":
    data = generate_realistic_dataset()