from django.shortcuts import render
import pygad
import numpy
import heapq

# Create your views here.
def index(request):
    if request.method == "POST":
        truckWeight = int(request.POST.get("TruckCapcity"))
        numberOfTrucks = int(request.POST.get("TruckCount"))
        GoodsNumber = int(request.POST.get("GoodsNumber"))
        AddressesNumber = int(request.POST.get("AddressesNumber"))
        packages = [[]]
        packagesWeight = [[]]
        Addresses = [[]]
        packages.clear()
        packagesWeight.clear()
        Addresses.clear()
        for i in range(1,GoodsNumber+1):
            packages.append([
                i,
                request.POST.get("GoodAddress_" + str(i)),
            ])
            packagesWeight.append([
                i,
                int(request.POST.get("GoodWeight_" + str(i))),
            ])
        for i in range(1,AddressesNumber+1):
            Addresses.append([i,[
                request.POST.get("AddressCurr_" + str(i)),
                request.POST.get("AddressPre_" + str(i)),
                int(request.POST.get("AddressTime_" + str(i))),
            ]])
        packages = dict(packages)
        packagesWeight = dict(packagesWeight)
        graph = {}

        for item in Addresses:
            key = item[1][0]
            graph[key] = {"preaddress": item[1][1], "Time": item[1][2]}

        def transform_data(data):
            keys = list(data.keys())
            result = {key: {} for key in keys}
            
            for key in keys:
                total_time = 0
                current_key = key
                while data[current_key]["preaddress"] != "startpoint":
                    total_time += data[current_key]["Time"]
                    current_key = data[current_key]["preaddress"]
                    result[key][current_key] = total_time
                    
                # Adding the reverse times
                for k, v in result[key].items():
                    result[k][key] = v
            
            return result
        transformed_data = transform_data(graph)

        total_weight = 0
        
        for item in list(packagesWeight.values()):
            total_weight += item
        
        def dijkstra(graph, start):
            distances = {node: float('inf') for node in graph}
            distances[start] = 0
            pq = [(0, start)]

            while pq:
                current_distance, current_node = heapq.heappop(pq)

                if current_distance > distances[current_node]:
                    continue

                for neighbor, weight in graph[current_node].items():
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(pq, (distance, neighbor))

            return distances


        def find_all_pairs_shortest_paths(graph):
            all_pairs_shortest_paths = {}
            for node in graph:
                all_pairs_shortest_paths[node] = dijkstra(graph, node)
            return all_pairs_shortest_paths


        def tsp_dp(distances, items):
            n = len(items)
            all_visited = (1 << n) - 1
            memo = {}

            def dp(pos, mask):
                if mask == all_visited:
                    return distances[items[pos]][items[0]]

                if (pos, mask) in memo:
                    return memo[(pos, mask)]

                min_cost = float('inf')
                for next_pos in range(n):
                    if mask & (1 << next_pos) == 0:
                        new_cost = distances[items[pos]][items[next_pos]] + dp(next_pos, mask | (1 << next_pos))
                        min_cost = min(min_cost, new_cost)

                memo[(pos, mask)] = min_cost
                return min_cost

            return dp(0, 1)

        def buildDict(list1, list2):
            dict_result = {}
            TrucksList = []
            i = 0
            total_number_of_item_added = 0
            tatal_carried_items_weight = 0
            for item in range(1, numberOfTrucks+1):
                TrucksList.append(truckWeight)
            for key, value in zip(list1, list2):
                if key in dict_result and (TrucksList[int(key) - 1] - list(packagesWeight.values())[i]) > 0:
                    dict_result[key].append(value)
                    TrucksList[int(key) - 1] -= list(packagesWeight.values())[i]
                    tatal_carried_items_weight += list(packagesWeight.values())[i]
                    total_number_of_item_added += 1
                elif (TrucksList[int(key) - 1] - list(packagesWeight.values())[i]) > 0:
                    dict_result[key] = [value]
                    TrucksList[int(key) - 1] -= list(packagesWeight.values())[i]
                    tatal_carried_items_weight += list(packagesWeight.values())[i]
                    total_number_of_item_added += 1
                i += 1

            return dict_result, tatal_carried_items_weight, total_number_of_item_added

        def dist_matrix(items):
            distances = {item: {} for item in items}
            for item in items:
                for target in items:
                    distances[item][target] = all_pairs_shortest_paths[item][target]
            return distances

        def fitness_func(ga_instance, solution, solution_idx):
            total_distance = 0
            comdict, final_weigth, items_carried = buildDict(solution, packages.values())
            for list in comdict.values():
                distances = {item: {} for item in list}
                for item in list:
                    for target in list:
                        distances[item][target] = all_pairs_shortest_paths[item][target]
                shortest_path_length = tsp_dp(distances, list)
                if shortest_path_length == 0:
                    total_distance = 0
                    break
                total_distance += shortest_path_length

            if total_distance == 0 or items_carried < len(packagesWeight)*0.75 :
                fitness = 0
            else:
                fitness = (1 / total_distance) * len(comdict)**2
            return fitness

        def recursive_shortest_path_finder(path):
            if(len(path[1]) == 1):
                return path[0], [path[1][0]], all_pairs_shortest_paths[path[0]][path[1][0]]
            subpaths = []
            subpaths_with_source = []
            shortest_id = -1
            shortest = float('inf')
            for i in range(0, len(path[1])):
                rest = path[1].copy()
                rest.pop(i)
                source, subpath, distance = recursive_shortest_path_finder([path[1][i], rest])
                subpaths.append(subpath)
                subpaths_with_source.append([])
                subpaths_with_source[i].append(source)
                subpaths_with_source[i].append(subpaths[i])
                subpaths_with_source[i].append(distance)
                newdist = all_pairs_shortest_paths[path[0]][source] + distance
                if newdist < shortest:
                    shortest = newdist
                    shortest_id = i
            shortest_path = subpaths_with_source[shortest_id]
            return path[0], shortest_path, shortest

        def fillRecursive(item):
            li.append(item[0])
            if(len(item) != 1):
                fillRecursive(item[1:][0])


                
        all_pairs_shortest_paths = find_all_pairs_shortest_paths(transformed_data)
        
        num_genes = len(packages)
        gene_space = range(1, numberOfTrucks + 1)
        
        num_generations = 100  # Number of generations.
        num_parents_mating = 20  # Number of solutions to be selected as parents in the mating pool.

        sol_per_pop = 50  # Number of solutions in the population.

        last_fitness = 0
        
        def on_generation(ga_instance):
             pass
        ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            sol_per_pop=sol_per_pop,
                            num_genes=num_genes,
                            fitness_func=fitness_func,
                            on_generation=on_generation,
                            gene_space=gene_space,
                            mutation_type="random",
                            mutation_percent_genes=20)

        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)


        realpath = buildDict(solution, list(packages.values()))[0]
        realpathA = dict()

        for i in realpath:
            realpathA[i] = (['A', realpath[i]])
        
        shortestPath = []
        for i in range(0, len(realpathA)):
            path = recursive_shortest_path_finder(list(realpathA.values())[i])
            shortestPath.append([list(realpathA.keys())[i], path[2], path])

        TrucksPathsFinal = dict()
        for i in shortestPath:
            li = []
            TrucksPathsFinal[i[0]] = []
            fillRecursive(i[2:][0])
            TrucksPathsFinal[i[0]].append(i[1])
            TrucksPathsFinal[i[0]].append(li[1:])
        context = {'TrucksPathsFinal': TrucksPathsFinal}
        return render(request, 'result.html', context)

    return render(request, 'index.html')




