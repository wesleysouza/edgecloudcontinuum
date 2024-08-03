# 1 EdgeServer

Essa classe que representa um servidor de Edge.

## 1.1 Argumentos

- obj_id (int, optional): Object identifier.
- coordinates (tuple, optional): 2-tuple that represents the edge server coordinates.
- model_name (str, optional): Edge server model name. Defaults to "".
- **cpu (int, optional)**: Edge server's CPU capacity. Defaults to 0.
- **memory (int, optional)**: Edge server's memory capacity. Defaults to 0.
- **disk (int, optional)**: Edge server's disk capacity. Defaults to 0.
- power_model (typing.Callable, optional): Edge server power model. Defaults to None.

## 1.2 Principais Métodos

- `to_dict`: Método que substitui a forma como o objeto é formatado para JSON;
	- return: representação do objeto como um dicionário;
- `collect`: Coleta um conjunto de métricas de um objeto;
	- Métricas:
		- Instance ID;
		- Coordinates;
		- Available;
		- CPU;
		- RAM;
		- Disk": 
		- CPU Demand;
		- RAM Demand;
		- Disk Demand;
		- Ongoing Migrations;
		- Services;
		- Registries;
		- Layers;
		- Images;
		- Download Queue;
		- Waiting Queue;
		- Max. Concurrent Layer Downloads;
		- Power Consumption;
- `step`: Método que executa os eventos que envolvem o objeto em cada intervalo de tempo;
- `get_power_consumption`: Coleta o consumo de energia;
- `has_capacity_to_host`: Verifica se um servidor tem capacidade de hospedar um determinado serviço;
	- args: serviço (Objeto);
	- return: Booleano (tem capacidade ou não)

### Referência

https://github.com/EdgeSimPy/EdgeSimPy/blob/master/edge_sim_py/components/edge_server.py

# 2 