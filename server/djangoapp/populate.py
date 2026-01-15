from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
      car_make, created = CarMake.objects.get_or_create(
        name=data['name'], defaults={'description': data.get('description', '')}
      )
      car_make_instances.append(car_make)


    # Create CarModel instances with the corresponding CarMake instances
    car_model_data = [
      {"name":"Pathfinder", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
      {"name":"Qashqai", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
      {"name":"XTRAIL", "type":"SUV", "year": 2023, "car_make":car_make_instances[0]},
      {"name":"A-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
      {"name":"C-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
      {"name":"E-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1]},
      {"name":"A4", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
      {"name":"A5", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
      {"name":"A6", "type":"SUV", "year": 2023, "car_make":car_make_instances[2]},
      {"name":"Sorrento", "type":"SUV", "year": 2023, "car_make":car_make_instances[3]},
      {"name":"Carnival", "type":"SUV", "year": 2023, "car_make":car_make_instances[3]},
      {"name":"Cerato", "type":"Sedan", "year": 2023, "car_make":car_make_instances[3]},
      {"name":"Corolla", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4]},
      {"name":"Camry", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4]},
      {"name":"Kluger", "type":"SUV", "year": 2023, "car_make":car_make_instances[4]},
        # Add more CarModel instances as needed
    ]

    for data in car_model_data:
      # avoid duplicate car models with same name and car_make
      if not CarModel.objects.filter(name=data['name'], car_make=data['car_make']).exists():
        # normalize type to match choices (SEDAN, SUV, WAGON)
        t = data.get('type', '')
        t_upper = ''
        if isinstance(t, str):
          if t.lower().startswith('sed'):
            t_upper = 'SEDAN'
          elif t.lower().startswith('suv'):
            t_upper = 'SUV'
          elif t.lower().startswith('wag'):
            t_upper = 'WAGON'
          else:
            t_upper = t.upper()
        else:
          t_upper = ''
        # provide a default dealer_id (required field)
        CarModel.objects.create(name=data['name'], car_make=data['car_make'], type=t_upper, year=data['year'], dealer_id=0)
