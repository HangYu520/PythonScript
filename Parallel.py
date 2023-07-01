"""
Parallel is a class for parallel computation.
function_name: the function for parallel computation
variable: the list of list of parameter of functions
"""
import concurrent.futures

class Parallel:

    def __init__(self, variable, function_name) -> None:
        self.variable = variable
        self.function = function_name
    
    def setVariable(self, variable):
        self.variable = variable
    
    def setFunction(self, function_name):
        self.function = function_name
    
    def launch(self):
        # results is in order
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(lambda params: self.function(*params), self.variable)
        return results
    
    def lauchBeta(self):
        # results is out of order
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.function, *var) for var in self.variable]

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Exception occurred: {e}")
        return results

if __name__ == "__main__":
    def add(x,y):
        return x + y
    
    def multiply(x,y,z):
        return x * y * z
    
    var1 = [[1,1],[2,2],[3,3]]
    var2 = [[1,1,1],[2,2,2],[3,3,3]]
    parallel = Parallel(var1,add)
    results = parallel.launch()
    #results = parallel.lauchBeta()
    print("add:", end=" ")
    for result in results:
        print(result, end=" ")
    print()

    parallel.setVariable(var2)
    parallel.setFunction(multiply)
    results = parallel.launch()
    #results = parallel.lauchBeta()
    print("multiply:", end=" ")
    for result in results:
        print(result, end=" ")