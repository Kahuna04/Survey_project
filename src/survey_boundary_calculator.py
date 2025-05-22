import math
import numpy as np

def calculate_boundary_coordinates(origin_easting, origin_northing, distances, bearings):
    """
    Calculate coordinates of boundary pillars given origin coordinates and 
    distances and bearings of boundary lines.
    
    Parameters:
    origin_easting (float): Easting coordinate of the origin
    origin_northing (float): Northing coordinate of the origin
    distances (list): List of distances for each boundary line
    bearings (list): List of bearings for each boundary line in degrees
    
    Returns:
    list: List of tuples containing (easting, northing) coordinates for each boundary pillar
    """
    coordinates = [(origin_easting, origin_northing)]
    
    current_easting = origin_easting
    current_northing = origin_northing
    
    for i in range(len(distances)):
        # Convert bearing from degrees to radians
        bearing_rad = math.radians(bearings[i])
        
        # Calculate the change in easting and northing
        delta_easting = distances[i] * math.sin(bearing_rad)
        delta_northing = distances[i] * math.cos(bearing_rad)
        
        # Calculate new coordinates
        current_easting += delta_easting
        current_northing += delta_northing
        
        coordinates.append((current_easting, current_northing))
    
    return coordinates

def calculate_area(coordinates):
    """
    Calculate the area of a parcel of land using the cross coordinate method.
    
    Parameters:
    coordinates (list): List of tuples containing (easting, northing) coordinates
    
    Returns:
    tuple: (area_square_meters, area_acres)
    """
    # Extract eastings and northings
    eastings = [coord[0] for coord in coordinates]
    northings = [coord[1] for coord in coordinates]
    
    # Ensure the polygon is closed
    if eastings[0] != eastings[-1] or northings[0] != northings[-1]:
        eastings.append(eastings[0])
        northings.append(northings[0])
    
    # Calculate area using cross coordinate formula
    area_sum1 = 0
    area_sum2 = 0
    
    for i in range(len(eastings) - 1):
        area_sum1 += eastings[i] * northings[i+1]
        area_sum2 += northings[i] * eastings[i+1]
    
    area_square_meters = abs(area_sum1 - area_sum2) / 2
    
    # Convert to acres (1 square meter = 0.000247105 acres)
    area_acres = area_square_meters * 0.000247105
    
    return area_square_meters, area_acres

def main():
    print("=== SURVEY BOUNDARY CALCULATOR ===")
    print("This program calculates boundary coordinates and land area.")
    
    # Get origin coordinates
    origin_easting = float(input("\nEnter origin easting coordinate: "))
    origin_northing = float(input("Enter origin northing coordinate: "))
    
    # Get number of boundary lines
    num_boundaries = int(input("\nEnter number of boundary lines: "))
    
    distances = []
    bearings = []
    
    # Get distances and bearings for each boundary line
    print("\nEnter distance and bearing for each boundary line:")
    for i in range(num_boundaries):
        distance = float(input(f"Distance for line {i+1} (meters): "))
        bearing = float(input(f"Bearing for line {i+1} (degrees): "))
        
        distances.append(distance)
        bearings.append(bearing)
    
    # Calculate boundary coordinates
    coordinates = calculate_boundary_coordinates(origin_easting, origin_northing, distances, bearings)
    
    # Print coordinates
    print("\n=== BOUNDARY COORDINATES ===")
    print("Pillar\tEasting\t\tNorthing")
    for i, (easting, northing) in enumerate(coordinates):
        print(f"{i+1}\t{easting:.3f}\t\t{northing:.3f}")
    
    # Calculate area
    area_square_meters, area_acres = calculate_area(coordinates)
    
    # Print area
    print("\n=== LAND AREA ===")
    print(f"Area in square meters: {area_square_meters:.3f} m²")
    print(f"Area in acres: {area_acres:.5f} acres")
    
    return coordinates, area_square_meters, area_acres

if __name__ == "__main__":
    main()