from geopy.geocoders import Nominatim
from geopy import Point
from geopy import distance
from sklearn.cluster import KMeans
import numpy as np
import visualization
import time
import colors


class Optimizer:
    def __init__(self):
        # center location
        self.MAP_CENTER = "Maslak, Istanbul"
        
        # basket settings
        self.BASKET_COUNT = 20
        self.BASKET_RADIUS = 1
        self.baskets = []
        
        # area limitations
        self.RADIUS = 0.05  # 5km
        
        # number of points for test 
        self.POINT_COUNT = 501
        
        # geocode provider
        self.geolocator = Nominatim(user_agent="paket_mutfak")
        self.center = self.geocode_to_coordinates(self.MAP_CENTER)
        self.points = []
        
    def generate_points(self):
        print("Random points are being generated.")
        for i in range(self.POINT_COUNT):
            lat = np.random.uniform(
                self.center.latitude - self.RADIUS, self.center.latitude + self.RADIUS)
            lon = np.random.uniform(
                self.center.longitude - self.RADIUS, self.center.longitude + self.RADIUS)
            self.points.append((lat, lon))
        print("Random points have been generated.")
            
    def geocode_to_coordinates(self, address):
        location = self.geolocator.geocode(address)
        lat, lon = location.latitude, location.longitude
        return Point(latitude=lat, longitude=lon)
    
    def coordinates_to_geocode(self, lat, lon):
        return self.geolocator.reverse(f"{lat}, {lon}")
    
    def optimize(self):
        print("K-Means clustering has been executed.")
        start_time = time.time()
        kmeans = KMeans(n_clusters=self.BASKET_COUNT, random_state=0).fit(self.points)
        self.baskets = [[] for i in range(self.BASKET_COUNT)]
        for i, point in enumerate(self.points):
            basket_index = kmeans.predict(np.array([point]))[0]
            basket = self.baskets[basket_index]
            if not basket:
                basket.append(point)
            else:
                valid_basket = False
                for p in basket:
                    if distance.distance(point, p).km <= 1:
                        valid_basket = True
                        break
                if valid_basket:
                    basket.append(point)
                else:
                    self.baskets.append([point])
        end_time = time.time()
        print(f"{colors.bcolors.OKGREEN}K-Means clustering is completed. Clustering time = {end_time - start_time} {colors.bcolors.ENDC}")
        self.verbose()
            
    def verbose(self):
        print("Log file is being created.")
        with open("log.txt", "w", encoding="utf-8") as log_file:
            for i, basket in enumerate(self.baskets):
                print(f"SEPETNO#{i+1}")
                log_file.write(f"SEPETNO#{i+1}")
                for j, point in enumerate(basket):
                    address = self.coordinates_to_geocode(point[0],point[1])
                    map_link = f"https://www.google.com/maps/search/?api=1&query={point[0]},{point[1]}"
                    print(f"item#{j+1} {point[0],point[1]}, {address}, {map_link}")
                    log_file.write(f"\n \t item#{j+1} {point[0],point[1]}, {address}, {map_link} \n")
                
        print("Log file has been created.")
        visualization.visualizer(self.baskets)
                
if __name__ == "__main__":
    
    optimization = Optimizer()
    optimization.generate_points()
    optimization.optimize()
    