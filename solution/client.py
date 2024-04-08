import requests

url="http://localhost:8000/"

compra_new={
    "client":"Juan Perez",
    "status":"Pendiente",
    "payment":"Tarjeta de Credito",
    "shipping":10.0,
    "products":["Camiseta","Pantalon","Zapatos"],
    "order_type":"Fisica"
}
response_new=requests.post(url+"orders",json=compra_new)
#print("--añadido--")
print(response_new.text)

#segundi post

compra_new={
    "client":"Maria Rodriguez",
    "status":"Pendiente",
    "payment":"Paypal",
    "code":"ABC123",
    "expiration":"2022-12-31",
    "order_type":"Digital"
}

response_new=requests.post(url+"orders",json=compra_new)
#print("--añadido--")
print(response_new.text)

#mostrar todo
response=requests.get(url+"orders")
#print("---lilsta de ordenes---")
print(response.text)

#filtrar por estado
response_est=requests.get(url+"orders/?status=Pendiente")
#print("---filtrando por estado---")
print(response_est.text)

#actualizar por id
status_a={"status":"En proceso"}
response_a=requests.put(url+"orders/1",json=status_a)
#print("---actualizar por id---")
print(response_a.text)

#borrar por id
response_del=requests.delete(url+"orders/1")
#print("---eliminado por id---")
print(response_del.text)

#agregar una nueva orden
compra_new={
    "client":"Ana Gutierrez",
    "status":"Pendiente",
    "payment":"Tarjeta de Debito",
    "shipping":20.0,
    "products":["Licuadora","Refrigeradora","Lavadora"],
    "order_type":"Fisica"
}
response_new=requests.post(url+"orders",json=compra_new)
#print("---añadido---")
print(response_new.text)

#lista de ordenes
response=requests.get(url+"orders")
#print("---lilsta de ordenes---")
print(response.text)
