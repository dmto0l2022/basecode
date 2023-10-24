

      '''
      class MakeApiCall():
      
          def get_data(self, api):
              response = requests.get(f"{api}")
              if response.status_code == 200:
                  print("sucessfully fetched the data")
                  self.formatted_print(response.json())
              else:
                  print(
                      f"Hello person, there's a {response.status_code} error with your request")
                  
          def formatted_print(self, obj):
              text = json.dumps(obj, sort_keys=True, indent=4)
              print(text)
      '''
      
      
      '''
      class Person:
        def __init__(self, name, age):
          self.name = name
          self.age = age
      
        def myfunc(self):
          print("Hello my name is " + self.name)
      '''  
